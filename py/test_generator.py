"""
Tests the generator
"""

import os
import tensorflow as tf
from py.procedures import build_model, init_tf_environ
from py.datasets.data_utils import load_data_as_ids
from py.utils.io_utils import save2csv


flags = tf.flags
flags.DEFINE_string("config_path", None, "The path of the model configuration file")
flags.DEFINE_string("data_path", None, "The path of the input data")
flags.DEFINE_string("log_path", None, "The path to save the log")
FLAGS = flags.FLAGS


def config_path():
    return FLAGS.config_path


def data_path():
    return FLAGS.data_path


def log_path():
    return FLAGS.log_path


if __name__ == '__main__':

    init_tf_environ()

    model, train_config = build_model(config_path())
    _, word_to_id = load_data_as_ids([os.path.join(data_path(), "ptb.train.txt")])
    save2csv([[s, v] for s, v in word_to_id.items()], os.path.join(data_path(), 'word_to_id.csv'))
    model.add_generator(word_to_id)
    model.restore()
    model.generate(10, 'test.json', max_branch=3, accum_cond_prob=0.9,
                   min_cond_prob=0.1, min_prob=0.001, max_step=10)


