import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import keras_nlp
import tensorflow as tf
import keras_core as keras
import boto3
import tensorflow_datasets as tfds


class TrainModel:
    def __init__(self):
        self.model = None
        self.training_data = None
        self.s3 = None
        self.s3_bucket_name = 'ai-example'

    def init_s3(self):
        self.s3 = boto3.client('s3')

    def import_model(self):
        # To speed up training and generation, we use preprocessor of length 128
        # instead of full length 1024.
        preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
            "gpt2_base_en",
            sequence_length=128,
        )
        self.model = keras_nlp.models.GPT2CausalLM.from_preset(
            "gpt2_base_en", preprocessor=preprocessor
        )

    def import_training_data(self):
        reddit_ds = tfds.load("reddit_tifu", split="train", as_supervised=True)

        self.training_data = (
            reddit_ds.map(lambda document, _: document)
            .batch(32)
            .cache()
            .prefetch(tf.data.AUTOTUNE)
        )

    def train_model(self):
        train_ds = self.training_data.take(500)
        num_epochs = 1

        # Linearly decaying learning rate.
        learning_rate = keras.optimizers.schedules.PolynomialDecay(
            5e-5,
            decay_steps=train_ds.cardinality() * num_epochs,
            end_learning_rate=0.0,
        )
        loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate),
            loss=loss,
            weighted_metrics=["accuracy"],
        )

        self.model.fit(train_ds, epochs=num_epochs)

    def save_model(self):
        self.model.save('trained_gpt2.keras')  # save the trained model as a file

    def upload_trained_model(self):
        with open('trained_gpt2.keras', 'rb') as data:
            self.s3.upload_fileobj(data, self.s3_bucket_name, 'trained_model')


def main():
    t = TrainModel()
    t.init_s3()
    t.import_model()
    t.import_training_data()
    t.train_model()
    t.save_model()
    t.upload_trained_model()


if __name__ == '__main__':
    main()
