import os
import json
from typing import List,Dict
from collections import defaultdict
from config.common_word import common_words
from schemas.schemas import KeyPhrases,KeyTokens
import yake
import spacy
from unidecode import unidecode
from spacy.tokens import Token
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Spacy model INIT
common_word_getter = lambda token: token.text in common_words
Token.set_extension("is_common_word", getter=common_word_getter,force=True)
model = os.getenv('SPACY_MODEL')
nlp = spacy.load(model)



# API INIT
app = FastAPI()


def extract_keytokens(text):
    pos_tag = ["NOUN", "ADJ", "ADV"]
    text_no_accents = unidecode(str(text))
    doc = nlp(text_no_accents.lower())
    top_key_tokens = [token.text for token in doc 
                      if token.is_alpha and 
                       not token.is_stop and 
                       token.pos_ in pos_tag and 
                       not token._.is_common_word and
                       token.ent_type_ not in ['PER','LOC']]
  
    all_keywords = list(set(top_key_tokens))

    return all_keywords



def extract_keysenteces(text,config):
    language = config.language
    max_ngram_size = config.max_ngram_size
    deduplication_thresold = config.deduplication_threshold
    deduplication_algo = config.deduplication_algo
    windowSize = config.window_size
    numOfKeywords = config.num_of_keywords
    kw_extractor = yake.KeywordExtractor(
                                lan=language,
                                n=max_ngram_size, 
                                dedupLim=deduplication_thresold, 
                                dedupFunc=deduplication_algo, 
                                windowsSize=windowSize, 
                                top=numOfKeywords
                                )

    return kw_extractor.extract_keywords(text)



@app.get("/")
def root():
  return ""


@app.post("/extract_keywords")
def extract_keywords(data: KeyTokens):

    """
    Endpoint para extraer las palabras clave más importantes de una lista de mensajes.

    Args:
        data (KeyTokens): Objeto Pydantic que contiene la lista de mensajes.
    
    Returns:
        dict: Un diccionario con las palabras clave ordenadas por importancia.
    """

    list_messages = data.messages_list
    if not list_messages:
        raise HTTPException(status_code=400, detail="La lista de mensajes está vacía")
    
    dict_palabras_encontradas = defaultdict(int)

    for message in list_messages:
        keywords = extract_keytokens(message)
        for keyword in keywords:
            dict_palabras_encontradas[keyword] += 1
    
    sorted_dict = dict(sorted(dict_palabras_encontradas.items(), key=lambda item: item[1], reverse=True))

    return {"key_words": sorted_dict}

@app.post("/extract_keyphrases")
def extract_keyphrases(data: KeyPhrases):

    """
    Endpoint para extraer las frases clave de una lista de mensajes.

    Args:
        data (KeyPhrases): Objeto Pydantic que contiene la lista de mensajes y la configuración.
        
        Config: parámetros de YAKE:
            --language: Idioma en el que se realiza la extracción de frases clave.
            --ngram-size: Tamaño máximo del n-grama.
            --dedup-func: Función de desduplicación (leve/jaro/seqm).
            --dedup-lim: Límite de desduplicación.
            --window-size: Tamaño de la ventana.
            --top: Número de frases clave a extraer.
    Returns:
        dict: Un diccionario con las frases clave ordenadas por importancia.
    """
    list_messages = data.messages_list
    if not list_messages:
        raise HTTPException(status_code=400, detail="La lista de mensajes está vacía")
    
    dict_palabras_encontradas = defaultdict(int)

    for message in list_messages:
        keywords = extract_keysenteces(message,data.config)
        for keyword,_ in keywords:
            dict_palabras_encontradas[keyword] += 1
    
    sorted_dict = dict(sorted(dict_palabras_encontradas.items(), key=lambda item: item[1], reverse=True))

    return {"key_phrases": sorted_dict}


app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)
