Código para pasar audio de un discurso a texto para analizar los discursos del Presidente de España durante la crisis del coronavirus. De momento contamos el número de palabras. 

# Discursos procesados

Puedes descargar los ficheros json de los discursos y los csv con el conteo de palabras en la carpeta [discursos](discursos)

# Cómo procesar otro audio

## Descargar un vídeo de RTVE, YouTube, etc.

1. Descargar el vídeo con Video Download Helper para Firefox u otra herramienta:

2. Extraer audio:

```bash
ffmpeg -i 2020-03-14-intervencion_presidente.webm 2020-03-14-intervencion_presidente.mp3
```

## Procesar audio con IBM Watson Speech to Text:

Vamos a usar el servicio *Speech to Text* de IBM Watson para pasar el audio a texto.

1. Como los audios son largos, hacemos una petición de procesamiento asíncrona, de otra forma la conexión acaba expirando. Además incluimos la opción de idiomas y marca de tiempo en las palabras. Tendrá que sustituir `{apikey}` y `{url}` en la llamada. Guardamos el ID del trabajo para poder descargar los resultados al terminar (idealmente podríamos un código python que lo hiciera todo o jugar con las opciones de URL de notificación, pero lo dejo otra pandemia)

```bash
curl -X POST -u "apikey:{apikey}" \
--header "Content-Type: audio/mp3" \
--data-binary @/home/javi/dwhelper/2020-03-14-intervencion_presidente.mp3 \
"{url}/v1/recognitions?timestamps=true&model=es-ES_BroadbandModel" > 2020-03-14-intervencion_presidente_job_id.json
```

2. Con este comando comprobamos el estado de la petición y cuando termina nos devuelve la lista de palabras. 

```bash
curl -X GET -u "apikey:{apikey}" \
"{url}/v1/recognitions/{job_id}" > 2020-03-14-intervencion_presidente.json
```

## Procesar y limpiar el texto con spacy

El siguiente código saca el texto del json y lo pone en una cadena listo para usarlo desde spacy. 

[procesa_discurso.py](procesa_discurso.py)

## Requisitos

Pandas, Spacy y ffmpeg.

Si tienes conda ya instalado: 
```
conda install -c conda-forge spacy
python -m spacy download es_core_news_sm
```

Upgrading:
```
pip install -U spacy
python -m spacy validate
```
