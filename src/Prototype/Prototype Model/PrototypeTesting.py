import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Step 1: Preprocess the data
def preprocess_data(folder_paths):
    data = []
    labels = []
    for folder_path in folder_paths:
        label = 1 if 'good' in folder_path else 0
        files = os.listdir(folder_path)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            # Read text data from file
            with open(file_path, 'r') as file:
                text = file.read()
            # Process text data (e.g., tokenization, padding)
            # Here, we'll use a simple tokenization example
            tokens = text.split()  # Split text into tokens
            # Convert tokens to a numerical representation (e.g., one-hot encoding)
            features = np.zeros((1000,))  # Assuming fixed-length representation
            for token in tokens:
                index = hash(token) % 1000  # Map token to an index (using hash function)
                features[index] += 1  # Increment count for the token index
            data.append(features)
            labels.append(label)
    return np.array(data), np.array(labels)

# Step 2: Define the MIL model with attention mechanism
def create_mil_model(input_shape):
    input_layer = tf.keras.layers.Input(shape=input_shape)
    # Define attention mechanism
    attention = tf.keras.layers.Dense(1, activation='tanh')(input_layer)
    attention = tf.keras.layers.Flatten()(attention)
    attention = tf.keras.layers.Activation('softmax')(attention)
    attention = tf.keras.layers.RepeatVector(input_shape[1])(attention)
    attention = tf.keras.layers.Permute([2, 1])(attention)
    # Apply attention to features
    attended_features = tf.keras.layers.Multiply()([input_layer, attention])
    # Aggregate attended features
    aggregated_features = tf.keras.layers.Lambda(lambda x: tf.keras.backend.sum(x, axis=1))(attended_features)
    # Fully connected layers for classification
    fc1 = tf.keras.layers.Dense(64, activation='relu')(aggregated_features)
    output_layer = tf.keras.layers.Dense(1, activation='sigmoid')(fc1)
    model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

# Step 3: Train the model
def train_mil_model(X_train, y_train):
    model = create_mil_model(input_shape=X_train.shape[1:])
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    return model

# Step 4: Evaluate the model
def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print("Test Accuracy:", accuracy)

# Main function
def main():
    # Modify the paths to point to your data in Google Drive or use direct file upload methods provided by Google Colab.
    train_folder_paths = ['/content/TrainGood', '/content/TrainBad']
    test_folder_paths = ['/content/TestGood', '/content/TestBad']

    # Preprocess data for training
    X_train, y_train = preprocess_data(train_folder_paths)

    # Preprocess data for testing
    X_test, y_test = preprocess_data(test_folder_paths)

    # Shuffle and split data into training and testing sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    # Train the model
    model = train_mil_model(X_train, y_train)

    # Evaluate the model on validation set
    evaluate_model(model, X_val, y_val)

    # Evaluate the model on test set
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()