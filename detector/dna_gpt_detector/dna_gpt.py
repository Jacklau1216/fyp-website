import sklearn
import sklearn.preprocessing
import json
from transformers import AutoTokenizer
import requests
#import time
#import concurrent.futures
from dotenv import load_dotenv
import spacy, six
import numpy as np
import scipy
import sklearn
import sklearn.preprocessing
import re
from nltk.stem.porter import PorterStemmer
from rouge_score.rouge_scorer import _create_ngrams, _score_ngrams
import math



import os

class DNAGPT:
	def __init__(self):
		load_dotenv()
		self.token = os.getenv('HF_TOKEN')
		self.headers = {"Authorization": "Bearer "+self.token}
		self.gptneox_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b", token=self.token)
		self.gptneo_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B", token=self.token)
		self.gemma_tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", token=self.token)
		self.mistralai_tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", token=self.token)
		self.llama_tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", token=self.token)
		self.falcon_tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", token=self.token)
		self.gpt2_tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2", token=self.token)

		self.API_URL_gptneox = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b"
		self.API_URL_gptneo = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B" # will return more than 1
		self.API_URL_Mistral = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
		self.API_URL_gemma = "https://api-inference.huggingface.co/models/google/gemma-7b"
		self.API_URL_llama_7b = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-hf"
		self.API_URL_falcon = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
		self.API_URL_gpt2 = "https://api-inference.huggingface.co/models/openai-community/gpt2" # will return more than 1
		self.API_URL_llama_13b = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-hf"

		self.PorterStemmer = PorterStemmer()
		self.nlp = spacy.load('en_core_web_sm')
		self.stopwords = self.nlp.Defaults.stop_words

	def query(self, api, payload):
		response = requests.post(api, headers=self.headers, json=payload)
		return response.json()


	def call_api(self, data):
		payload = {
			"inputs": data[1],
			"parameters": {
				"max_new_tokens": 100,
				"num_return_sequences": 5,
				"return_full_text": False,
				"temperature": 0.7,
			},
			"options": {
				"wait_for_model": True,
				"use_cache": False
			}
		}
		try:
			payload["inputs"] = data[1]
			result_data = {
				"text": data[0],
				"origin_1st_half": data[1],
				"origin_2nd_half": data[2]
			}
			outputs = []
			

			payload["parameters"]["max_new_tokens"] = len(self.gptneox_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_gptneox, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.gptneox_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("gptneox: ", output)

			payload["parameters"]["max_new_tokens"] = len(self.mistralai_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_Mistral, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.mistralai_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("mistralai: ", output)

			output = self.query(self.API_URL_Mistral, payload)
			try:
				for out in output:
				#print("falcon:", out)
					if (len(self.mistralai_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("mistralai: ", output)

			payload["parameters"]["max_new_tokens"] = len(self.gemma_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_gemma, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.gemma_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("gemma: ", output)

			payload["parameters"]["max_new_tokens"] = len(self.llama_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_llama_7b, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.llama_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("llama_7b: ", output)

			output = self.query(self.API_URL_llama_7b, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.llama_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("llama_7b: ", output)

			output = self.query(self.API_URL_llama_13b, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.llama_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("llama_13b: ", output)

			output = self.query(self.API_URL_llama_13b, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.llama_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("llama_13b: ", output)

			payload["parameters"]["max_new_tokens"] = len(self.falcon_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_falcon, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.falcon_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("falcon: ", output)

			payload["parameters"]["max_new_tokens"] = len(self.falcon_tokenizer(data[2])["input_ids"])
			output = self.query(self.API_URL_falcon, payload)
			try:
				for out in output:
					#print("falcon:", out)
					if (len(self.falcon_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("falcon: ", output)

			new_token = len(self.gpt2_tokenizer(data[2])["input_ids"])
			payload["parameters"]["max_new_tokens"] = new_token if new_token <= 250 else 250
			output = self.query(self.API_URL_gpt2, payload)
			try:
				for out in output:
					#print("gpt2:", out)
					if (len(self.gpt2_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("gpt2: ", output)

			new_token = len(self.gptneo_tokenizer(data[2])["input_ids"])
			payload["parameters"]["max_new_tokens"] = new_token if new_token <= 250 else 250
			output = self.query(self.API_URL_gptneo, payload)
			try:
				for out in output:
					#print("gpt2:", out)
					if (len(self.gptneo_tokenizer(out['generated_text'])["input_ids"]) > 5):
						outputs.append(out['generated_text'])
					else:
						print(out['generated_text'])
			except:
				print("gptneo: ", output)

			idx = 1
			assert(len(outputs) >= 10)
			for out in outputs:
				result_data["regen_2nd_half_{}".format(idx)] = out
				idx = idx + 1
			#result_data["source"] = 0 if data[3] == "Human" else 1
			return result_data
		except:
			print("fail regen")
			return None
		

	def get_score_ngrams(self, target_ngrams, prediction_ngrams):
		intersection_ngrams_count = 0
		ngram_dict = {}
		for ngram in six.iterkeys(target_ngrams):
			#print(min(target_ngrams[ngram],prediction_ngrams[ngram]))
			intersection_ngrams_count += min(target_ngrams[ngram],prediction_ngrams[ngram])
			ngram_dict[ngram] = min(target_ngrams[ngram], prediction_ngrams[ngram])
		target_ngrams_count = sum(target_ngrams.values()) # prediction_ngrams
		#print(target_ngrams_count)
		#print(sum(target_ngrams.values()))
		return intersection_ngrams_count / max(target_ngrams_count, 1), ngram_dict

	def get_ngram_info(self, article_tokens, summary_tokens, _ngram):
		article_ngram = _create_ngrams( article_tokens , _ngram)
		summary_ngram = _create_ngrams( summary_tokens , _ngram)
		ngram_score, ngram_dict = self.get_score_ngrams( article_ngram, summary_ngram)
		return ngram_score, ngram_dict, sum( ngram_dict.values() )

	def tokenize(self, text, stemmer, stopwords=[]):
		"""Tokenize input text into a list of tokens.

		This approach aims to replicate the approach taken by Chin-Yew Lin in
		the original ROUGE implementation.

		Args:
		text: A text blob to tokenize.
		stemmer: An optional stemmer.

		Returns:
		A list of string tokens extracted from input text.
		"""

		# Convert everything to lowercase.

		text = text.lower()
		# Replace any non-alpha-numeric characters with spaces.
		text = re.sub(r"[^a-z0-9]+", " ", six.ensure_str(text))

		tokens = re.split(r"\s+", text)
		if stemmer:
			# Only stem words more than 3 characters long.
			tokens = [stemmer.stem(x) if len(x) > 3 else x for x in tokens if x not in stopwords]

		# One final check to drop any empty or invalid tokens.
		tokens = [x for x in tokens if re.match(r"^[a-z0-9]+$", six.ensure_str(x))]

		return tokens


	def N_gram_detector(self, ngram_n_ratio):
		score = 0
		non_zero = []

		for idx, key in enumerate(ngram_n_ratio):
			if idx in range(3) and 'score' in key or 'ratio' in key:
				score += 0. * ngram_n_ratio[ key ]
				continue
			if 'score' in key or 'ratio' in key:
				score += (idx+1) * np.log((idx+1))   * ngram_n_ratio[ key ]
				if ngram_n_ratio[ key ] != 0:
					non_zero.append( idx+1 )
			#print(ngram_n_ratio[ key ])
		return score/ (sum( non_zero ) + 1e-8)
	
	def dna_gpt_score(self, data):
		temp = []
		received_tokens = self.tokenize( data["origin_2nd_half"], stemmer=self.PorterStemmer)
		for idx in range(1,len(data)-4):
      
			temp1 = {}
			
			if data["regen_2nd_half_{}".format(idx)] == None:
				continue
			generate_tokens = self.tokenize(data["regen_2nd_half_{}".format(idx)], stemmer=self.PorterStemmer)
			if len(generate_tokens) == 0:
				continue
			for _ngram in range(1, 26):
				ngram_score, ngram_dict, overlap_count = self.get_ngram_info(received_tokens, generate_tokens, _ngram)
				temp1['human_truncate_ngram_{}_score'.format(_ngram)] = ngram_score / len(generate_tokens)
				temp1['human_truncate_ngram_{}_count'.format(_ngram)] = overlap_count

			temp.append({'human':temp1})
			
		result = self.N_gram_detector(temp[0]["human"]) * 100
		return result

	def dna_gpt_detect(self, text):
		input_id = self.mistralai_tokenizer(text)["input_ids"]
		n = math.ceil(len(input_id) / 2)
		res = [input_id[:n], input_id[n:]]
		origin_1st_half = self.mistralai_tokenizer.decode(res[0],skip_special_tokens=True)
		origin_2nd_half = self.mistralai_tokenizer.decode(res[1],skip_special_tokens=True)
		data = [text, origin_1st_half, origin_2nd_half]
		regen_result = self.call_api(data)
		try:
			score = self.dna_gpt_score(regen_result)
		except:
			return None
		return 0 if score < 0.018 else 1

















