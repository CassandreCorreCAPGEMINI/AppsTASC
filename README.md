# Name of the repository

## Description

This section offers a concise overview of the repository's purpose, detailing what it contains and its intended use. It serves as an introduction to the repository's functionality.

## RDI Method: EDC(s)
If this repository contains several "EDCs'branches" they need to be listed them and the link toward the PDE document and the internal article need to be added. 
For instance:

| EDCs| PDE | Internal Article |Current State| Main File| Main Contributor|Corresponding EDC|
|----------|----------|----------|----------|----------|----------|----------|
| 2.044| [Link to PDE](https://capgemini.sharepoint.com/:p:/r/sites/RIMindActProject/Shared%20Documents/M%C3%A9thodeRDI_MindAct/Fiches_PdE/Fiche_PdE_2.044_DW_31012024.pptx?d=w983127e1021740f49ade529e38bb7d49&csf=1&web=1&e=7eN67b)| [Link to Internal Article](https://capgemini.sharepoint.com/:w:/r/sites/RIMindActProject/Shared%20Documents/M%C3%A9thodeRDI_MindAct/Articles_MindAct/Articles%20internes/Article_Interne_EdC_2.044_DW_31012024.docx?d=wc96b58f25845425aa9bc731d17c85f92&csf=1&web=1&e=2b4ozU) |Consolidated | [main.py](...)<!--link to the file-->| John Doe|X
| X.XXX | [Link to PDE](...) | [Link to Internal Article](...)|Consolidating| [extractor.py](...)<!--link to the file-->| Jane Doe|
| ... | ... | ..|..| ..|..|


This Readme has to be converted to a pdf file for each new EDC using the following terminology EDCNumber_Readme_V_Versionnumber.pdf and uploaded to the project SharePoint. It needs to be done when:
- a CIR review happened
- the new EDC is completed 

In the first case, the column "Main file" must be updated with the file name the main contributor is working on for the corresponding new EDCs ( corresponding EDCs line). The main contributor also needs to update the "Current State." The number of the current EDC and the name of the main contributor need to be completed. There is no need to complete "PDE" and "Internal Article" since, at this stage, no PDE and internal articles have been produced. The line of the corresponding EDC needs to be highlighted in red.

In the second case, the only difference from the previous cases is that the columns "PDE" and "Internal Article" need to be completed with the corresponding state, and "Current State" needs to be changed to Consolidated.

To add value to each part of the code produced in a project, they must be linked to an EDC.


## Requirements

In this part, the necessary prerequisites and dependencies for using the repository are listed. It provides users with information on the required environment and software versions needed to run the code effectively.

## Installation

This section provides instructions on how to install the repository and its dependencies. It may include commands or guidelines for setting up the environment, installing packages, or configuring settings to ensure smooth installation.

```
# The necessary commands for the install must be put in scripts snippets like this
python -m pip install -r /path/to/requirements.txt
```

## Usage

Users are provided with examples or guidelines on how to use the code or features within the repository. It typically includes code snippets, explanations, and usage scenarios to help users understand how to interact with the provided functionality. It may also include links to example notebooks stored in the repository.

Code snippets example:


```python
# Import the necessary modules
from maadatamanager.load_extract.manage_datasets import DataSetManager
from maadatamanager.load_extract import data_extraction, preprocessing, epoching, medusa_utils

# Your python functions, ...

```

## Documentation
This part serves as comprehensive documentation for the repository's features, methods, and classes. It explains the functionalities, usage instructions, and available options in detail to assist users in utilizing the repository effectively.

## Contributing
If one would like to contribute to the repository, issues can be reported, improvements suggested, or merge requests submitted. The guidelines need to be followed for contributing and any specific requirements or coding standards need to be adopted.

## License
This code is for internal use and research purposes only.

## Contact
For any questions or inquiries, please contact the maintener 

## Acknowledgements
Contributors acknowledge and express gratitude to individuals, organizations, or projects that have contributed to or influenced the repository's development. It's a way to recognize and appreciate external contributions and collaborations.

## References
The references section includes citations and links to relevant literature, research papers, or external resources that are pertinent to the repository's subject matter. It provides users with additional reading materials and sources for further exploration.
