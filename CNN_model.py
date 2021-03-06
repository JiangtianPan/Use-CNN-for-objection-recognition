
import numpy as np
from cv2 import *

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import sgd
import load_dataset

img_sz = load_dataset.IMAGE_SIZE

def data_preprocessing(X_train,Y_train,X_test,Y_test):

    # preprocess the training and test data (transform into CNN supported data form)
    # also with normalization
    X_train = X_train.reshape(X_train.shape[0], img_sz, img_sz, 3)
    X_test = X_test.reshape(X_test.shape[0], img_sz, img_sz, 3)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    cat_sz = load_dataset.CATEGORY_SIZE[0]

    # Y_train = np_utils.to_categorical(Y_train, cat_sz)
    Y_train = my_to_categorical(Y_train, cat_sz)
    Y_test = my_to_categorical(Y_test, cat_sz)
    # Y_test = np_utils.to_categorical(Y_test, cat_sz)

    return X_train,Y_train,X_test,Y_test

def model_built():
    cat_sz = load_dataset.CATEGORY_SIZE[0]

    # 1. Define model architecture
    model = Sequential()

    # convolution layer 1
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(img_sz, img_sz, 3)))
    # pooling layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # convolution layer 2
    model.add(Conv2D(32,(3,3), activation='relu'))
    # pooling layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # convolution layer 3 # less recognition if added w/ overfitting problem
    # model.add(Conv2D(64,(3,3), activation='relu'))
    # # pooling layer
    # model.add(MaxPooling2D(pool_size=(2, 2)))

    # random loss of activity, also a part to decrease the computing complexity
    # model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))

    model.add(Dense(32, activation='relu'))

    # random loss of activity
    model.add(Dropout(0.5))

    model.add(Dense(cat_sz, activation='softmax'))
    # model.add(Dense(cat_sz, activation='sigmoid')) #less precise

    # 2. Compile model
    # opt = sgd(lr=0.01) # sgd are less precise
    opt = 'adam'
    model.compile(loss='categorical_crossentropy',
                  optimizer= opt,
                  metrics=['accuracy'])

    return model

# my model to categorical function
# y can be a list of list, instead of just list of integers (the way np.to_categorical deal with)
# every element, say k, in y[i] as 1 in categorical[i][k]
def my_to_categorical(y, num_classes):
    y=np.array(y)
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    # print(n,y)
    categorical = np.zeros((n, num_classes))
    for i in range(0,len(y)):
        for j in y[i]:
            categorical[i,j]=1
    # categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical