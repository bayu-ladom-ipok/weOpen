import tensorflow as tf
import json
import shutil
import os
import pickle
import fastai
from lookahead import Lookahead
from callback import MultipleClassAUROC, MultiGPUModelCheckpoint
from configparser import ConfigParser
from generator import AugmentedImageSequence
from keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau, EarlyStopping
from keras.optimizers import Adam
from keras.utils import multi_gpu_model
from models.keras_phase1 import ModelFactory
#from models.keras_phase2 import ModelFactory
from utility import get_sample_counts
from weights import get_class_weights
from augmenter import augmenter
from keras_radam import RAdam
import keras
from keras import backend as K


def focal_loss(y_true, y_pred):
    epsilon = K.epsilon()
        # Add the epsilon to prediction value
        #y_pred = y_pred + epsilon
        # Clip the prediction value
    y_pred = K.clip(y_pred, epsilon, 1.0-epsilon)
    gamma = 1.0
    alpha = 0.5
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0))


def main():
    # parser config
    config_file = "./config.ini"
    cp = ConfigParser()
    cp.read(config_file)

    # default config
    output_dir = cp["DEFAULT"].get("output_dir")
    image_source_dir = cp["DEFAULT"].get("image_source_dir")
    base_model_name = cp["DEFAULT"].get("base_model_name")
    class_names = cp["DEFAULT"].get("class_names").split(",")

    # train config
    use_base_model_weights = cp["TRAIN"].getboolean("use_base_model_weights")
    use_trained_model_weights = cp["TRAIN"].getboolean("use_trained_model_weights")
    use_best_weights = cp["TRAIN"].getboolean("use_best_weights")
    output_weights_name = cp["TRAIN"].get("output_weights_name")
    epochs = cp["TRAIN"].getint("epochs")
    batch_size = cp["TRAIN"].getint("batch_size")
    initial_learning_rate = cp["TRAIN"].getfloat("initial_learning_rate")
    generator_workers = cp["TRAIN"].getint("generator_workers")
    image_dimension = cp["TRAIN"].getint("image_dimension")
    train_steps = cp["TRAIN"].get("train_steps")
    patience_reduce_lr = cp["TRAIN"].getint("patience_reduce_lr")
    min_lr = cp["TRAIN"].getfloat("min_lr")
    validation_steps = cp["TRAIN"].get("validation_steps")
    positive_weights_multiply = cp["TRAIN"].getfloat("positive_weights_multiply")
    dataset_csv_dir = cp["TRAIN"].get("dataset_csv_dir")
    # if previously trained weights is used, never re-split
    if use_trained_model_weights:
        # resuming mode
        print("** use trained model weights **")
        # load training status for resuming
        training_stats_file = os.path.join(output_dir, ".training_stats.json")
        if os.path.isfile(training_stats_file):
            # TODO: add loading previous learning rate?
            training_stats = json.load(open(training_stats_file))
        else:
            training_stats = {}
    else:
        # start over
        training_stats = {}

    show_model_summary = cp["TRAIN"].getboolean("show_model_summary")
    # end parser config

    # check output_dir, create it if not exists
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    running_flag_file = os.path.join(output_dir, ".training.lock")
    if os.path.isfile(running_flag_file):
        raise RuntimeError("A process is running in this directory!!!")
    else:
        open(running_flag_file, "a").close()

    try:
        print(f"backup config file to {output_dir}")
        shutil.copy(config_file, os.path.join(output_dir, os.path.split(config_file)[1]))

        datasets = ["train", "dev", "test"]
        for dataset in datasets:
            shutil.copy(os.path.join(dataset_csv_dir, f"{dataset}.csv"), output_dir)

        # get train/dev sample counts
        train_counts, train_pos_counts = get_sample_counts(output_dir, "train", class_names)
        dev_counts, _ = get_sample_counts(output_dir, "dev", class_names)

        # compute steps
        if train_steps == "auto":
            train_steps = int(train_counts / batch_size)
        else:
            try:
                train_steps = int(train_steps)
            except ValueError:
                raise ValueError(f"""
                train_steps: {train_steps} is invalid,
                please use 'auto' or integer.
                """)
        print(f"** train_steps: {train_steps} **")

        if validation_steps == "auto":
            validation_steps = int(dev_counts / batch_size)
        else:
            try:
                validation_steps = int(validation_steps)
            except ValueError:
                raise ValueError(f"""
                validation_steps: {validation_steps} is invalid,
                please use 'auto' or integer.
                """)
        print(f"** validation_steps: {validation_steps} **")

        # compute class weights
        print("** compute class weights from training data **")
        class_weights = get_class_weights(
            train_counts,
            train_pos_counts,
            multiply=positive_weights_multiply,
        )
        print("** class_weights **")
        print(class_weights)

        print("** load model **")
        if use_trained_model_weights:
            if use_best_weights:
                model_weights_file = os.path.join(output_dir, f"best_{output_weights_name}")
            else:
                model_weights_file = os.path.join(output_dir, output_weights_name)
        else:
            model_weights_file = None

        model_factory = ModelFactory()
        model = model_factory.get_model(
            class_names,
            model_name=base_model_name,
            use_base_weights=use_base_model_weights,
            weights_path=model_weights_file,
            input_shape=(image_dimension, image_dimension, 3))

        if show_model_summary:
            print(model.summary())


    finally:
        os.remove(running_flag_file)


if __name__ == "__main__":
     main()
