import numpy as np
import sklearn
import json
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification, AutoModelWithLMHead
from transformers import pipeline
import torch
from pysbd import Segmenter
import math
import pickle
from detector.lf_detector_deployment import preprocess, detect
from detector.dna_gpt_detector.dna_gpt import DNAGPT
import tiktoken
import os

class EnsembleDectector:
  def __init__(self):
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.gpt2tokenizer, self.gpt2model = self.create_tokenizer_and_model("gpt2")
    self.gpt1tokenizer, self.gpt1model = self.create_tokenizer_and_model("openai-gpt")
    self.lfdetectortokenizer = AutoTokenizer.from_pretrained("nealcly/detection-longformer")
    self.lfdetectormodel = AutoModelForSequenceClassification.from_pretrained("nealcly/detection-longformer").to(self.device)
    self.robertadetectorpipe = pipeline("text-classification", model="roberta-large-openai-detector", device=self.device)
    clf_path = os.path.dirname(__file__) + '/clf_new.pickle'
    with open(clf_path, 'rb') as f:
      self.clf = pickle.load(f)
    self.dnagptdetector = DNAGPT()
    self.enc = tiktoken.get_encoding("cl100k_base")

  def create_tokenizer_and_model(self, model_name):
    device = self.device
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelWithLMHead.from_pretrained(model_name).to(device)
    return tokenizer, model

  def gpt_analyse_text(self, text, tokenizer, model):
    try:
      max_length = model.config.n_positions
    except:
      max_length = 1024

    # Overall Perplexity
    perplexity = self.gpt_get_perplexity(tokenizer, model, text, max_length)

    # Perplexity for each sentence
    sentences_perplexity = []
    sentences = self.sentence_split(text)
    for sentence in sentences:
      try:
        sentence_perplexity = self.gpt_get_perplexity(tokenizer, model, sentence, max_length)
        sentences_perplexity.append(sentence_perplexity)
      except:
        print("Cannot detect")

    average_perplexity = sum(sentences_perplexity)/len(sentences_perplexity)
    burstiness = max(sentences_perplexity)

    return perplexity, average_perplexity, burstiness

  def gpt_get_perplexity(self, tokenizer, model, text, max_length):
    encodings = tokenizer(text, return_tensors="pt").to(self.device)
    seq_len = encodings.input_ids.size(1)
    stride = 512

    nlls = []
    likelihoods = []
    prev_end_loc = 0
    for begin_loc in range(0, seq_len, stride):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids.to(self.device), labels=target_ids.to(self.device))
            neg_log_likelihood = outputs.loss * trg_len
            likelihoods.append(neg_log_likelihood)

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_len:
            break
    perplexity = int(torch.exp(torch.stack(nlls).sum() / end_loc))
    return perplexity

  def sentence_split(self, text):
    segmenter = Segmenter(language='en', clean=False)
    sentences = segmenter.segment(text)
    return sentences

  def detect_text(self, text):
    chunks = self.text_split(text)
    chunks_predict_result = []
    overall_result = False
    total_token = len(self.enc.encode(text))
    token_is_AI = 0
    chunk_is_AI_probability = []
    for chunk in chunks:
      #print(chunk)
      gpt_perplexity, gpt_average_perplexity, gpt_burstiness = self.gpt_analyse_text(chunk, self.gpt1tokenizer, self.gpt1model)
      gpt2_perplexity, gpt2_average_perplexity, gpt2_burstiness = self.gpt_analyse_text(chunk, self.gpt2tokenizer, self.gpt2model)
      perplexity_predict_result = self.clf.predict([[gpt2_perplexity, gpt2_average_perplexity, gpt2_burstiness, gpt_perplexity, gpt_average_perplexity, gpt_burstiness]])
      roberta_detect = self.robertadetectorpipe(chunk)
      roberta_predict_result = 0 if roberta_detect[0]["label"] == "LABEL_1" else 1
      lf_predict_result = detect(chunk,self.lfdetectortokenizer,self.lfdetectormodel,self.device)
      dnagpt_predict_result =  self.dnagptdetector.dna_gpt_detect(chunk)
      results = [perplexity_predict_result[0],roberta_predict_result, lf_predict_result, dnagpt_predict_result]
      predict_result = []
      for result in results:
        if result is not None:
          predict_result.append(result)
      #print(results)
      chunks_info = {
         "text": chunk,
         "result": 1 if sum(predict_result)/len(predict_result) >= 0.5 else 0,
         "percentage": sum(predict_result)/len(predict_result),
         "token": len(self.enc.encode(chunk))
      }
      chunk_is_AI_probability.append(sum(predict_result)/len(predict_result))
      chunks_predict_result.append(chunks_info)
      if chunks_info["result"] == True:
        overall_result = True
        token_is_AI = token_is_AI + len(self.enc.encode(chunk))
    text_is_AI_percentage = token_is_AI / total_token
    #print(overall_result)
    #print(chunks_predict_result)
    #print(text_is_AI_percentage)
    #print(chunk_is_AI_probability)
    return overall_result, chunks_predict_result, text_is_AI_percentage, chunk_is_AI_probability

  def text_split(self, text):
    segmenter = Segmenter(language='en', clean=False)
    sentences = segmenter.segment(text)
    min_token = 150
    chunks = []
    current_chunk_tokens = 0
    current_chunk = None
    for i, sentence in enumerate(sentences):
      sentence_tokens = len(self.enc.encode(sentence))
      if (sentence == sentences[-1] and current_chunk_tokens + sentence_tokens < min_token and len(chunks)>0):
          current_chunk = chunks[-1] + current_chunk + sentence
          chunks.pop(-1)
          chunks.append(current_chunk)
          current_chunk = None
      elif (sentence == sentences[-1] and sentence_tokens < min_token and len(chunks)>0):
          current_chunk = current_chunk + sentence
          chunks.append(current_chunk)
          current_chunk = None
      elif current_chunk_tokens > min_token:
          chunks.append(current_chunk)
          current_chunk = sentence
          current_chunk_tokens = len(self.enc.encode(current_chunk))
      else:
          if current_chunk:
              current_chunk += sentence
              current_chunk_tokens += sentence_tokens
          else:
              current_chunk = sentence
              current_chunk_tokens = sentence_tokens
    if current_chunk != None:
      chunks.append(current_chunk)
    return chunks
