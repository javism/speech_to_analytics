import spacy
import json
import pandas as pd
from spacy.attrs import ORTH

nlp = spacy.load("es_core_news_sm")
# No sé por qué estas letras no cuentan como stop words
nlp.Defaults.stop_words.add('y')
nlp.Defaults.stop_words.add('o')
nlp.Defaults.stop_words.add('a')

import xml.etree.ElementTree as ET
boe_file = 'BOE/2020-03-14.xml'
root = ET.parse('BOE/2020-03-14.xml').getroot()

texto = root.find('texto')
token = [p.text for p in texto] 
big_str = ' '.join(token)

doc = nlp(big_str)

#lematizamos (no me gusta el resultado, e.j, paramos -> parir, gracias->gracia)
#token = [token.lemma_ for token in doc]
# quitamos las stop words 
token = [token.text for token in doc if not (token.is_stop | token.is_punct | token.is_space )]

filtered_data = ' '.join(token)
filtered_doc = nlp(filtered_data)

counts = filtered_doc.count_by(ORTH)
print(len(counts))
word_list = []
for word_id, count in sorted(counts.items(), reverse=True, key=lambda item: item[1]):
    print(count, nlp.vocab.strings[word_id])
    word_list.append({'Veces': count, 'Palabra': nlp.vocab.strings[word_id]})

df = pd.DataFrame(word_list)
csv_file = boe_file.split('.xml')[0] + '.csv'
df.to_csv(csv_file, index=False)