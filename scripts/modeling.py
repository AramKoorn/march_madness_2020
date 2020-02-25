import tensorflow as tf
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)



def run():

    df = pd.read_pickle('data/processed/tour_features.pkl')
    X_train = df.seed_difference
    y_train = df.goal_difference