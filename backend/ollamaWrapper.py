
from ollama import Client
from constants import OLLAMA_BASE_URL

def get_models():
    client = Client(host=OLLAMA_BASE_URL)
    models = client.list()["models"]
    return models
