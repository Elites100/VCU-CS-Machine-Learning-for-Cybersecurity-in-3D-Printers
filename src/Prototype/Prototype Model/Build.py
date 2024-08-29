import tensorflow as tf
import pandas as pd
import numpy as np
import os

# Define your model architecture
class MILModel(tf.keras.Model):
    def __init__(self):
        super(MILModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(32, activation='relu')
        self.dense3 = tf.keras.layers.Dense(1, activation='sigmoid')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        output = self.dense3(x)
        return output

# Define your Multiple Instance Learning algorithm
class MultipleInstanceLearning:
    def __init__(self, model):
        self.model = model
        self.optimizer = tf.keras.optimizers.Adam()
        self.loss_object = tf.keras.losses.BinaryCrossentropy()

    def train_step(self, bags, labels):
        with tf.GradientTape() as tape:
            predictions = self.model(bags)
            loss = self.loss_object(labels, predictions)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return loss

    def train(self, train_data, epochs):
        for epoch in range(epochs):
            epoch_loss_avg = tf.keras.metrics.Mean()
            for bag, label in train_data:
                loss = self.train_step(bag, label)
                epoch_loss_avg(loss)
            print(f'Epoch {epoch + 1}: Loss: {epoch_loss_avg.result()}')

    def evaluate(self, test_data):
        test_loss = tf.keras.metrics.Mean()
        for bag, label in test_data:
            predictions = self.model(bag)
            test_loss(self.loss_object(label, predictions))
        print(f'Test Loss: {test_loss.result()}')

# Load your datasets from CSV files
def load_dataset_from_csv(directory):
    bags = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            data = pd.read_csv(filepath)
            instances = data.values  # Assuming each row in CSV is an instance
            bags.append(instances)
            # You may need to adjust how labels are extracted depending on your dataset structure
            labels.append(data['label'].iloc[0])  # Assuming the label is in a column named 'label'
    return bags, labels

# Example usage
if __name__ == "__main__":
    # Directory containing CSV files
    train_csv_directory = 'path/to/train/csv/filess'
    test_csv_directory = 'path/to/test/csv/files'

    # Load datasets
    train_bags, train_labels = load_dataset_from_csv(train_csv_directory)
    test_bags, test_labels = load_dataset_from_csv(test_csv_directory)

    # Convert to TensorFlow tensors
    train_dataset = tf.data.Dataset.from_tensor_slices((train_bags, train_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_bags, test_labels))

    # Shuffle and batch the datasets
    BATCH_SIZE = 32
    train_dataset = train_dataset.shuffle(len(train_bags)).batch(BATCH_SIZE)
    test_dataset = test_dataset.batch(BATCH_SIZE)

    # Initialize model and MIL algorithm
    model = MILModel()
    mil = MultipleInstanceLearning(model)

    # Train the model
    EPOCHS = 10
    mil.train(train_dataset, epochs=EPOCHS)

    # Evaluate the model
    mil.evaluate(test_dataset)