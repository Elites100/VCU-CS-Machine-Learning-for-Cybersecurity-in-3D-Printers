# Source Code Folder
| Subdirectory Name | Description |
|---|---|
| Dataset| The folder contains two directories, One containing CSV and one containing G-Code. |
| Production Model | The folder holds the machine learning model responsible for processing and training using CSV g-code data|
| Production Parser | The folder contains Python parsers that are tasked with extracting pertinent g-code data for the features of the Production Model. Within this folder are two parsers: one remains unaltered (considered good), while the other has been modified (deemed bad) and is utilized for training and testing the model   |
| Prototype | The folder contains outdated, unused, or previously used parsers.|
| G-Code_Tester.py| A Python Script that will allow a User to Input their own CSV to Test against a Pre-Trained Model to determine whether the inputted CSV has been previously modified.|
| | |
