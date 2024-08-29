# *Machine Learning for Cybersecurity in 3D Printers*
Additive manufacturing (aka., 3D printers) is increasingly utilized in industry, supporting mass customization of parts manufacturing and industry 4.0 vision. G-code is a 3D printing programming language used to print objects. Attackers target them to sabotage objects being printed. This capstone project will use machine learning techniques to analyze G-code programs to detect and analyze malware.
## *Sponsoring Company or Organization*
Irfan Ahmed / VCU CS
## *Description*
This project aims to create a Machine Learning Algorithm model to detect any malicious attacks or manipulations on G-Code for 3D printer files at the Layer level. This will be accomplished by creating a large Dataset containing extrapolated features that can be found within G-Code files that have been processed through Cura, a splicing program, that could be easily manipulated to cause damage to the devices or prints. Once a dataset is created, it is then fed and trained into a multiple-instance learning algorithm that will be able to predict for any changes within a provided G-code sample. This model will be created through the use of Python and the TensorFlow library. Additionally, another dataset will be created from G-code files that have been maliciously altered and used as a Testing dataset for the model. The outcome will be a machine learning model that can predict an expected outcome for a provided G-code file and determine if the file has been maliciously manipulated or altered by a cybersecurity attack.

| Folder | Description |
|---|---|
| Documentation |  all documentation the project team has created to describe the architecture, design, installation and configuration of the peoject |
| Notes and Research | Relavent information useful to understand the tools and techniques used in the project |
| Status Reports | Project management documentation - weekly reports, milestones, etc. |
| scr | Source code - contains the model, parsers, and an installation guide. |

## Project Team
- *Irfan Ahmed*  - *VCU CS* - Faculty Advisor
- *Hala Ali* - *VCU CS* - Mentor
- *Christ Le* - *CS* - Student Team Member
- *Kevin Phung* - *CS* - Student Team Member
- *Trae Evans* - *CS* - Student Team Member
- *Michael Brown* - *CS* - Student Team Member
