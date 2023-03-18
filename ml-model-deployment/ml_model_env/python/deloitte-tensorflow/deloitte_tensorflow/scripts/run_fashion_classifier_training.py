import argparse
import pathlib
import os
import sys
import tensorflow as tf

from deloitte_tensorflow.models.fashion_classifier import FashionClassifierModel


def run_model_training(model_path):
    """
    Function to run the FashionClassifierModel training on the fashion_mnist tensorflow sample dataset

    :param model_path:
    :return:
    """
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    model = FashionClassifierModel.train_from_data(train_images, train_labels, test_images, test_labels)
    model.save_to_file(model_path)

    print(f"Just saved the FashionClassifierModel to: {model_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True, help='Local path to write Tensorflow model conf')

    args = parser.parse_args()
    run_model_training(args.model_path)
