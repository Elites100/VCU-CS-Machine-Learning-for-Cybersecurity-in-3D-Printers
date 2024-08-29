# Production Parser Folder
| Subdirectory Name | Description |
|---|---|
| G-Code Parser.py | The function of the program is to Convert G-Code into a Suitable CSV format |
| G-Code Malicious Parser.py | The function of this program is to Modify G-Code Files into Modified G-Code |
| Modify Malicious CSV.py| The Function of this program is to correct the Modified Column within a CSV from a Information csv created from 'G-Code Malicious Parser.py' for all modified g-code |
| Layer Checker.py| The function of this program is to check if the layer comment is properly formated to prevent errors when attempting to train |
| Remove Insuitable CSV.py| The function of this program is to remove all files identified by 'Layer Checker.py" from a directroy. |
| | |

# Parsing Directions

## Benign G-Code  

__Step 1__: Run 'G-Code Parser.csv' on Benign G-code  
* Input: Benign G-Code Directory Path  
* Output: CSV  

__Step 2__: Run Layer Checker.py'  
* Input: Benign G-Code Directory Path  
* Output: A CSV containing any File containing Bad Layers  

__Step 3__: Run 'Remove Insuitable.csv'  
* Input: Modified Layers CSV from 'Layer Checker.py'  

## Malicious G-Code  

__Step 1__: Run 'G-Code Malicious Parser.py'  
* Input: Malicious G-Code Directory Path  
* Output: Modified G-Code  

__Step 2__: Run 'G-Code Parser.csv' on Malicious G-code  
* Input: Malicious G-Code Directory Path  
* Output: CSV  

__Step 3__: Run 'Modify Malicious CSV.py  
* Input: CSV file produced from 'G-Code Malicious Parser', Malicious G-Code Directory Path  
* Output: Modified CSV  

__Step 4__: Run Layer Checker.py'  
* Input: Benign G-Code Directory Path  
* Output: A CSV containing any File containing Bad Layers  

__Step 5__: Run 'Remove Insuitable.csv'  
* Input: Modified Layers CSV from 'Layer Checker.py'  