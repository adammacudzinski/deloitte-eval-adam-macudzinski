import tensorflow as tf
import numpy as np
import logging


log = logging.getLogger(__name__)


class FashionClassifierModel:
    pixel_scale = 255.0
    training_epochs = 10

    def __init__(self, model: tf.keras.Model):
        self.model = model

    @classmethod
    def load_from_file(cls, file_path):
        """
        Class method to init model object from saved file

        :param file_path: str file path containing model conf
        :return:
        """
        model = tf.keras.models.load_model(file_path)
        return cls(model)

    @classmethod
    def train_from_data(
        cls,
        train_images: np.ndarray,
        train_labels: np.ndarray,
        test_images: np.ndarray,
        test_labels: np.ndarray
    ):
        """
        Class method to train a TensorFlow model from input data represented as numpy arrays

        :param train_images:
        :param train_labels:
        :param test_images:
        :param test_labels:
        :return:
        """
        train_images = train_images / cls.pixel_scale
        test_images = test_images / cls.pixel_scale

        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10)
        ])

        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        log.info(f"Starting {cls.__name__} model training")

        model.fit(train_images, train_labels, epochs=cls.training_epochs)

        test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

        log.info(f"Model {cls.__name__} test evaluation accuracy: {test_acc}")

        return cls(model)

    def save_to_file(self, file_path: str):
        """
        Save the Tensorflow model to local disk

        :param file_path: Str path to write the model file to
        :return:
        """
        self.model.save(file_path)







