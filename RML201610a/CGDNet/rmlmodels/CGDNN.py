import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv1D, MaxPooling1D, ReLU, Dropout, Softmax, concatenate, Flatten, Reshape, \
    GaussianNoise, Activation, GaussianDropout, Conv2D, GRU, BatchNormalization
from tensorflow.keras.layers import Lambda, Multiply, Add, Subtract, MaxPooling2D, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model

def CGDNN(weights=None,
          input_shape=[1, 2, 128],
          input_shape2=[128],
          classes=11,
          **kwargs):
    if weights is not None and not os.path.exists(weights):
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization), '
                         'or the path to the weights file to be loaded.')

    dr = 0.2  # dropout rate (%)
    input = Input(input_shape, name='input1')
    input1 = Input(input_shape2, name='input2')
    input2 = Input(input_shape2, name='input3')

    x1 = Conv2D(50, (1, 6), activation='relu', kernel_initializer='lecun_uniform', data_format="channels_first")(input)
    x1 = MaxPooling2D(pool_size=(2, 2), strides=1, padding='same', data_format="channels_first")(x1)
    x1 = GaussianDropout(dr)(x1)
    x2 = Conv2D(50, (1, 6), activation='relu', kernel_initializer='glorot_uniform', data_format="channels_first")(x1)
    x2 = MaxPooling2D(pool_size=(2, 2), strides=1, padding='same', data_format="channels_first")(x2)
    x2 = GaussianDropout(dr)(x2)
    x3 = Conv2D(50, (1, 6), activation='relu', kernel_initializer='glorot_uniform', data_format="channels_first")(x2)
    x3 = MaxPooling2D(pool_size=(2, 2), strides=1, padding='same', data_format="channels_first")(x3)
    x3 = GaussianDropout(dr)(x3)
    x11 = concatenate([x1, x3], axis=3)
    x4 = Reshape(target_shape=(50, 472), name='reshape4')(x11)
    x4 = GRU(units=50)(x4)  # Automatically chooses the best implementation
    x4 = GaussianDropout(dr)(x4)
    x = Dense(256, activation='relu', name='fc4', kernel_initializer='he_normal')(x4)
    x = GaussianDropout(dr)(x)
    x = Dense(classes, activation='softmax', name='softmax')(x)

    model = Model(inputs=input, outputs=x)

    # Load weights
    if weights is not None:
        model.load_weights(weights)

    return model

if __name__ == '__main__':
    model = CGDNN(None, classes=10)

    adam = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=adam)

    plot_model(model, to_file='model.png', show_shapes=True)  # Save the model architecture plot
    print('Model layers:', model.layers)
    print('Model config:', model.get_config())
