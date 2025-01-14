# -*- coding: utf-8 -*-
"""AIMODELBUILDER2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yXm4947Cv5KqKQGSuJ0WUdtn9ix_NUUw
"""

# Importing all dependencies
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def read_csv_files(folder_paths):
    data = []
    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path)
                data.append(df.values)
    return data

# def preprocess_data(folder_paths):
#     data = []
#     labels = []
#     for folder_path in folder_paths:
#         label = 1 if 'Good' in folder_path else 0
#         folder_data = read_csv_files([folder_path])
#         print("Number of samples in folder:", len(folder_data))
#         data.extend(folder_data)  # Extend the list with each file's data
#         labels.extend([label] * len(folder_data))
#     if data:  # Check if data is not empty
#         max_length = max(len(sample) for sample in data)  # Find the maximum length among samples
#         data = [np.pad(sample, ((0, max_length - len(sample)), (0, 0))) for sample in data]  # Pad samples to have equal length
#     data = np.array(data)  # Convert to numpy array
#     data = np.expand_dims(data, axis=-1)  # Add an extra dimension for time steps
#     labels = np.array(labels)
#     print("Data shape:", data.shape)
#     print("Labels shape:", labels.shape)
#     return data, labels

def preprocess_data(folder_paths):
    data = []
    labels = []
    for folder_path in folder_paths:
        label = 1 if 'Good' in folder_path else 0
        folder_data = read_csv_files([folder_path])
        data.extend(folder_data)
        print("Number of samples in folder:", len(folder_data))
        labels.extend([label] * len(data[-1]))  # Extend labels for each item in the last added data
    data = np.concatenate(data)  # Concatenate the list of arrays into one array
    data = np.expand_dims(data, axis=-1)  # Add an extra dimension for time steps
    labels = np.array(labels)
    print("Data shape:", data.shape)
    print("Labels shape:", labels.shape)
    return data, labels


def create_mil_model(input_shape):
    inputs = tf.keras.layers.Input(shape=input_shape)

    # Define the shared part of the model
    shared_layer = tf.keras.layers.Dense(64, activation='relu')(inputs)

    # Apply GlobalAveragePooling1D directly to the shared layer output
    pooled_output = tf.keras.layers.GlobalAveragePooling1D()(shared_layer)

    # Add a dense layer for classification
    output = tf.keras.layers.Dense(1, activation='sigmoid')(pooled_output)

    # Create the model
    model = tf.keras.Model(inputs=inputs, outputs=output)

    # Compile the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

def train_mil_model(X_train, y_train):
    model = create_mil_model(input_shape=X_train.shape[1:])
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    return model

def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print("Test Accuracy:", accuracy)

"""The main() function that would run the combined functions above"""

train_folder_paths = ['/content/TrainGood', '/content/TrainBad']
test_folder_paths = ['/content/TestGood', '/content/TestBad']

X_train, y_train = preprocess_data(train_folder_paths)
X_test, y_test = preprocess_data(test_folder_paths)

model = train_mil_model(X_train, y_train)

evaluate_model(model, X_test, y_test)