import keras
from keras import ops as K


def plcc(y_true, y_pred):
    y_true = K.cast(K.reshape(y_true, [-1]), "float32")
    y_pred = K.cast(K.reshape(y_pred, [-1]), "float32")

    centered_true = y_true - K.mean(y_true)
    centered_pred = y_pred - K.mean(y_pred)

    std_true = K.std(y_true)
    std_pred = K.std(y_pred)

    epsilon = keras.config.epsilon()
    return K.mean(centered_true * centered_pred) / (std_true * std_pred + epsilon)
