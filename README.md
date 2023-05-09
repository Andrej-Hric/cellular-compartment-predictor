# Protein Subcellular Localization Predictor

<p align="center">
  <iframe src="https://github.com/Andrej-Hric/cellular-compartment-predictor/blob/main/Logo//anim.html" width="500" height="500"></iframe>

  
  
</p>

<p align="center">
  A deep learning model to predict protein subcellular localization from amino acid sequences.
  <br />
  <a href="https://github.com/Andrej-Hric/cellular-compartment-predictor"><strong>Explore the repository »</strong></a>
  <br />
  <br />
  <a href="<URL_TO_ISSUES_PAGE>">Report a Bug</a>
</p>

## Table of Contents

- [About the Project](#about-the-project)
  - [Adapting the code for other Database](#Adapting-the-code-for-other-database)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Input File Formats](#input-file-formats)
- [Contributing](#contributing)
- [License](#license)




## About the Project
This Python script uses a deep learning model (LSTM) to predict protein subcellular localization based on their amino acid sequences. The input data can be in CSV, FASTA, GFF, or simple text format. The script currently uses the UniProt database, **however, it can be adapted for other databases if required** ([Adapting the code for other Database](#adapting-the-code-for-another-database)).

### Adapting the Code for Another Database

If you would like to use a different protein sequence database instead of UniProt, follow these steps to adapt the code:

1. Replace the `get_uniprot_data` function with a new function to retrieve data from your preferred database. Update the function name and the URL for the API request. You may also need to modify the request parameters and the way the response is processed, depending on the API documentation of the new database.

2. If the new database uses a different file format for protein sequences, update the `read_input_file` function to handle the new format. You may need to add a new condition in the function to check for the file extension and process the file accordingly.

3. Update the `preprocess_data` function if the new database has different data formatting or additional attributes that need to be processed before training the model.

4. Verify that the remaining code works correctly with the new database. You may need to adjust the model architecture, hyperparameters, or training process based on the characteristics of the new data.

### ⚠️Potential Issues When Adapting the Code for Another Database ⚠️
While adapting the code for another protein sequence database, you may come across some issues or errors. Here are some common challenges you might face and need to address during the adaptation process:

  1. **API limitations**: Some databases may have limitations on the number of requests, rate limits, or require authentication. You may need to adjust the code accordingly to handle these limitations, which may include using API keys, implementing request throttling, or handling pagination.

  2. **API response format**: Different databases may return data in various formats, such as JSON or XML. You will need to adapt the code to parse the new response format correctly and extract the relevant information.

  3. **Data preprocessing**: Depending on the new database, the data preprocessing steps might need to be adjusted to handle different data formats, attributes, or normalization methods.

  4. **Model performance**: The performance of the LSTM model might be different when trained on data from a new database. You might need to experiment with different model architectures, hyperparameters, or training techniques to achieve optimal performance on the new dataset.

  5. **Code compatibility**: There might be compatibility issues with the new database or the required libraries for handling the data, which may require updates or adjustments to the existing code.



## Getting Started

To get started with the Protein Subcellular Localization Predictor, follow these steps.

### Prerequisites

You'll need to have the following software installed on your computer:

- Python 3.x: Download and install the appropriate version for your operating system from [python.org](https://www.python.org/downloads/).
- Git: Download and install the appropriate version for your operating system from [git-scm.com](https://git-scm.com/downloads).

### Setting up a Virtual Environment

1. Clone the repository:
   ```sh
    git clone https://github.com/Andrej-Hric/cellular-compartment-predictor.git
2. Navigate to the cloned repository directory:
   ```sh
   cd protein-localization-predictor
3. Create a virtual environment:
   ```sh
    python3 -m venv cell_comp_project_env
4. Activate the virtual environment:
- For Windows:
   ```sh
   cell_comp_project_env\Scripts\activate
- For macOS/Linux:
   ```sh
   source cell_comp_project_env/bin/activate


### Installation
- Install the required Python libraries:
   ```sh
   pip install pandas numpy scikit-learn tensorflow biopython


### Installation
- Install the required Python libraries:
   ```sh
   pip install pandas numpy scikit-learn tensorflow biopython

## Usage

To use the Protein Subcellular Localization Predictor, follow these steps:

1. Save your protein sequences in a supported file format (CSV, FASTA, GFF, or TXT).
2. Open a terminal window and navigate to the folder containing the `protein_localization_predictor.py` file.
3. Run the following command:
    ```sh
    protein_localization_predictor.py
4. The model will be trained and evaluated. The performance metrics will be displayed in the terminal.

## Input File Formats

The script supports the following input file formats:

- CSV: Comma-separated values format, with a header row.
- FASTA: FASTA format, with each sequence preceded by a header line starting with '>'.
- GFF: General Feature Format, with each sequence in a separate entry.
- TXT: Simple text format, with one sequence per line.

## Contributing:

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a branch with a descriptive name.
3. Make changes to the code in your branch.
4. Commit your changes and push them to your fork.
5. Create a pull request and explain your changes.

## License:

This project is licensed under the MIT License. 

## Acknowledgements:

- UniProt: Source of protein sequence data.
- TensorFlow: Deep learning library used for model development.
- Biopython: Library for handling FASTA and GFF files.
- Looka: Logo maker used to create the project logo.




       




