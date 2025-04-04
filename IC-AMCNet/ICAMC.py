# CLDNNLike model for RadioML.

# Reference:
# - [CONVOLUTIONAL,LONG SHORT-TERM MEMORY, FULLY CONNECTED DEEP NEURAL NETWORKS ]
# Adapted from code contributed by Mika.

import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Conv2D, MaxPooling2D, Flatten, GaussianNoise

def ICAMC(weights=None,
          input_shape=[2,128],
          classes=11,
          **kwargs):
    if weights is not None and not os.path.exists(weights):
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization), '
                         'or the path to the weights file to be loaded.')

    dr = 0.4
    input = Input(shape=input_shape + [1], name='input')
    x = Conv2D(64, (1, 8), activation="relu", name="conv1", padding='same', kernel_initializer='glorot_uniform')(input)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(64, (1, 4), activation="relu", name="conv2", padding='same', kernel_initializer='glorot_uniform')(x)
    x = Conv2D(128, (1, 8), activation="relu", name="conv3", padding='same', kernel_initializer='glorot_uniform')(x)
    x = MaxPooling2D(pool_size=(1, 1))(x)
    x = Dropout(dr)(x)
    x = Conv2D(128, (1, 8), activation="relu", name="conv4", padding='same', kernel_initializer='glorot_uniform')(x)
    x = Dropout(dr)(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu', name='dense1')(x)
    x = Dropout(dr)(x)
    x = GaussianNoise(1)(x)
    x = Dense(classes, activation='softmax', name='dense2')(x)

    model = Model(inputs=input, outputs=x)

    # Load weights.
    if weights is not None:
        model.load_weights(weights)

    return model

if __name__ == '__main__':
    model = ICAMC(None, input_shape=[2,128], classes=11)

    adam = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=adam)

    print('Model layers:', model.layers)
    print('Model config:', model.get_config())
    print('Model summary:', model.summary())
