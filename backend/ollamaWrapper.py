
from ollama import Client
from backend.constants import OLLAMA_BASE_URL
import logging

logging.basicConfig(level=logging.INFO)

def get_models_as_json_array():
    logger = logging.getLogger(__name__)
    client = Client(host=OLLAMA_BASE_URL)
    try:
        models = client.list()["models"]
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    return models

def get_models():
    logger = logging.getLogger(__name__)    
    models_as_json = get_models_as_json_array()
    if models_as_json is None:
        logger.error("Error: Could not get models")
        return None
    model_names = [model['name'] for model in models_as_json]
    return model_names
