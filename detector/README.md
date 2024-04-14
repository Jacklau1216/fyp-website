Install en_core_web_sm for DNA-GPT :

```bash
python -m spacy download en_core_web_sm
```

Example using DNAGPT detect text:
```python
from dna_gpt_detector.dna_gpt import DNAGPT

detector = DNAGPT()
text_to_detect = "The Norman community spread across western France and on to the English Channel Islands and the east coast of England. The Kingdom of Normandy was founded in Normandy in 1078, and was ruled by a series of dukes since the end of the 11th century. The Normans were divided into various kingdoms, including the Kingdom of Brittany, the Kingdom of Normandy, the Kingdom of Meuse, and the Kingdom of Poitou. In 1180, William I, King of England, invaded Normandy and seized Normandy, but he was defeated and driven out by the Normans. This was the beginning of the English Civil War. In 1185, King Stephen died without a male heir, and his cousin, Henry II, was crowned king. Henry II became the regent for his half-brother, Richard II, King of England, against Henry's wife, Catherine of Aragon. Richard, however, died in 1189, and his younger brother, John I, was installed as king."

result = detector.dna_gpt_detect(text_to_detect)
print(result)
```

Example using Ensemble Detector detect text:
```python
from ensemble_detector import EnsembleDectector

detector = EnsembleDectector()
text_to_detect = "The Norman community spread across western France and on to the English Channel Islands and the east coast of England. The Kingdom of Normandy was founded in Normandy in 1078, and was ruled by a series of dukes since the end of the 11th century. The Normans were divided into various kingdoms, including the Kingdom of Brittany, the Kingdom of Normandy, the Kingdom of Meuse, and the Kingdom of Poitou. In 1180, William I, King of England, invaded Normandy and seized Normandy, but he was defeated and driven out by the Normans. This was the beginning of the English Civil War. In 1185, King Stephen died without a male heir, and his cousin, Henry II, was crowned king. Henry II became the regent for his half-brother, Richard II, King of England, against Henry's wife, Catherine of Aragon. Richard, however, died in 1189, and his younger brother, John I, was installed as king."

overall_result, chunks_predict_result, text_is_AI_percentage, chunk_is_AI_probability = detector.detect_text(text_to_detect)
print(overall_result)
```