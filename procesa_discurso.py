import spacy
import json
import pandas as pd
from spacy.attrs import ORTH

nlp = spacy.load("es_core_news_sm")
# No sé por qué estas letras no cuentan como stop words
nlp.Defaults.stop_words.add('y')
nlp.Defaults.stop_words.add('o')
nlp.Defaults.stop_words.add('a')

json_file = '2020-03-19_Rueda_prensa_comite_tecnico.json'

with open(json_file) as f:
  data = json.load(f)

results_list = data['results'][0]['results']

big_str = str()
for sentence in results_list:
    big_str = big_str + sentence['alternatives'][0]['transcript']

doc = nlp(big_str)

#lematizamos (no me gusta el resultado, e.j, paramos -> parir, gracias->gracia)
#token = [token.lemma_ for token in doc]
# quitamos las stop words 
token = [token.text for token in doc if not token.is_stop]

filtered_data = ' '.join(token)
filtered_doc = nlp(filtered_data)

counts = filtered_doc.count_by(ORTH)
print(len(counts))
word_list = []
for word_id, count in sorted(counts.items(), reverse=True, key=lambda item: item[1]):
    print(count, nlp.vocab.strings[word_id])
    word_list.append({'Veces': count, 'Palabra': nlp.vocab.strings[word_id]})

df = pd.DataFrame(word_list)
csv_file = json_file.split('.json')[0] + '.csv'
df.to_csv(csv_file, index=False)