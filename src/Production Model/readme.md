ALGORITHMS: NEURAL NETWORKS

ARCHITECTURES: RNN / LSTM (predominantly LSTM)

## Summary of model
This machine learning model employs an RNN architecture based on LSTM to capture temporal dependencies within sequential data. It performs binary classification with sigmoid activation, utilizing TensorFlow and Keras libraries for efficient model development and training. Preprocessing steps include label encoding, one-hot encoding, dropout regularization, and early stopping to mitigate overfitting and improve generalization. The model combines unaltered and altered datasets, encodes labels, partitions data for training and testing, adjusts input shapes for LSTM compatibility, and proceeds with LSTM model definition, training, and evaluation.

## Files:
1. Model-1 : A Folder containing a pre-trained model.
2. RNN.py : A Machine Learning Algorithm written in Python.
3. RNN_Learning_Algorithm.ipynb : A Machine Learning Algorithm written in Python for Juypter Notebook

## Directions to the initial use of this model
After receiving two or more CSV files that were previously parsed into G-code by the parser, you now possess both a good CSV file and a bad (malicious) CSV file that can be utilized by the machine learning system. It is highly recommended to incorporate as many datasets as possible into the machine learning model, including both good and bad (malicious) CSV files. Following this, adjust the machine learning model itself by changing the variables "unmodified_folder_path" and "modified_folder_path" with the actual folder paths containing the good and bad (malicious) CSV files respectively. Alternatively, you can obtain the datasets from the provided GitHub repository at [Dataset/CSV](https://github.com/VCU-CS-Capstone/CS-24-318-Machine-Learning-for-Cybersecurity-in-3D-Printers/tree/master/src/Dataset/CSV) and adjust the paths accordingly. Then, execute the program to train and test the machine learning model.


## Key Components of the Model (in-depth):

--> RNN/LSTM: LSTMs are utilized to handle the sequential nature of input data, emphasizing the significance of data order.

RNN - Processes the current input along with the previous step's output.
LSTM - Maintains a memory unit known as a cell state, enabling long-term information retention. LSTMs employ input, forget, and output gates to control information flow:
Input gate: Manages the intake of new information into the cell state.
Forget gate: Determines how much of the previous cell state to retain or discard.
Output gate: Generates the output based on the current cell state.

--> Binary: The model's output layer employs a sigmoid activation function suitable for binary classification, producing probabilities indicating the likelihood of each class. (Where 1 signifies closeness to "modified" and 0 to "unaltered.")

--> Model Compilation: The model is compiled using the Adam optimizer, an adaptive learning rate optimization algorithm. It utilizes binary cross-entropy as the loss function, appropriate for binary classification tasks.

## Installation Guide

There are two methods of installing the project's dependencies: one method uses Poetry and a Virtual Environment, and the other ues the requirements.txt file.

### Installation with Poetry and Venv
1. __Create a Python Virtual Environment (optional)__
    * in a directory of your choice, create a virtual environment with:
    ```
    python -m venv (name of your venv)
    ```
    * this will create a package to store the projects dependencies that won't interfere with your other python projects.
    * to activate the environment, navigate to (venv name)/Scripts, and run __activate__.


2. __Install Poetry__: 
    * Install poetry using:
    ```
    pip install poetry
    ```
    * this will install poetry into your virtual environment's libraries, and allow us to install the peoject's other dependencies much faster


2. __Run Poetry__:
    * To install the projects other dependencies with poetry, enter:
    ```
    poetry install
    ```
    in the _/src_ directory containing the pyproject.toml file.
    * After it runs, all of the projects dependencies will be installed, and you can run the model


### Installation with pip and requirements.txt
1. __Run Pip with Requirements.txt__:
    * Install Pip if not already installed and install the required dependency using pip and requirements.txt located in /src directory with the following command.
```
pip install -r requirements.txt
```
