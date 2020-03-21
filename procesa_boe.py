import spacy
import json
import pandas as pd
from spacy.attrs import ORTH
import xml.etree.ElementTree as ET
import os 

nlp = spacy.load("es_core_news_sm")
# No sé por qué estas letras no cuentan como stop words
nlp.Defaults.stop_words.add('y')
nlp.Defaults.stop_words.add('o')
nlp.Defaults.stop_words.add('a')

boe_dir = 'BOE'

fs = os.listdir(boe_dir)
list_boe = list()

for f in fs:
    if ('.xml' in f):
        boe_file = boe_dir + '/' + f 
        root = ET.parse(boe_file).getroot()
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
            #print(count, nlp.vocab.strings[word_id])
            word_list.append({'Veces': count, 'Palabra': nlp.vocab.strings[word_id]})

        df = pd.DataFrame(word_list)
        list_boe.append(word_list)
        csv_file = boe_file.split('.xml')[0] + '.csv'
        df.to_csv(csv_file, index=False)