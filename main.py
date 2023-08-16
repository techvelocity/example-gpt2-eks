import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import keras_nlp
import tensorflow as tf
import keras_core as keras

from fastapi import FastAPI

app = FastAPI()


MODEL = keras.models.load_model('trained_gpt2.keras')

@app.post("/api/generate")
async def generate_text(prompt:str):
    max_length = 200
    
    r = MODEL.generate(prompt, max_length)

    
    return {"generated_text": r}