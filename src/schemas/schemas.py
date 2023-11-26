from pydantic import BaseModel
from typing import List

class KeyTokens(BaseModel):
    messages_list: List[str]

class Config(BaseModel):
    language: str
    max_ngram_size: int
    deduplication_threshold: float
    deduplication_algo: str
    window_size: int
    num_of_keywords: int

class KeyPhrases(BaseModel):
    config: Config
    messages_list: List[str]