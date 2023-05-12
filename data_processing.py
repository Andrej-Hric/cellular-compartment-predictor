import os
import pandas as pd
from Bio import SeqIO
from sklearn.preprocessing import LabelBinarizer
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences

MAX_SEQUENCE_LENGTH = 1000



def check_file_format(file_path, file_type):
    """
    Check if the file is in a correct format.

    Parameters:
    file_path (str): The path to the file.
    file_type (str): The type of the file, either 'input' or 'output'.

    Returns:
    bool: True if the file format is correct, False otherwise.
    """
    allowed_input_formats = {'.csv', '.fasta', '.gff', '.txt', '.tsv'}
    allowed_output_formats = {'.csv'}
    _, file_extension = os.path.splitext(file_path)

    if file_type == 'input':
        return file_extension in allowed_input_formats
    elif file_type == 'output':
        return file_extension in allowed_output_formats
    else:
        return False


def load_data(input_file):
    """
    Load the data from the input file and return a DataFrame.

    Parameters:
    input_file (str): The path to the input file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    file_extension = os.path.splitext(input_file)[1]
    if file_extension == '.csv':
        data = pd.read_csv(input_file)
    elif file_extension == '.tsv':
        data = pd.read_csv(input_file, sep='\t')
    elif file_extension in ['.fasta', '.gff', '.txt']:
        records = list(SeqIO.parse(input_file, 'fasta'))
        data = pd.DataFrame(
            {'ID': [rec.id for rec in records], 'Sequence': [str(rec.seq) for rec in records]}
        )
    else:
        raise ValueError(f"Unsupported input file format: {file_extension}")

    return data


def encode_sequence(sequence):
    """
    Encode a protein sequence into numerical values.

    Parameters:
    sequence (str): The protein sequence.

    Returns:
    list: A list of integers representing the encoded protein sequence.
    """
    encoding = {
        'A': 1, 'R': 2, 'N': 3, 'D': 4, 'C': 5, 'Q': 6, 'E': 7, 'G': 8, 'H': 9, 'I': 10,
        'L': 11, 'K': 12, 'M': 13, 'F': 14, 'P': 15, 'S': 16, 'T': 17, 'W': 18, 'Y': 19, 'V': 20
    }
    return [encoding.get(char, 0) for char in sequence]


def preprocess_data(data):
    """
    Preprocess the data by encoding the protein sequences and subcellular localizations.

    Parameters:
    data (pd.DataFrame): The input data containing protein IDs, sequences, and subcellular localizations.

    Returns:
    tuple: A tuple containing the preprocessed protein sequences (X) and subcellular localizations (y).
    """
    data['Subcellular location [CC]'] = data['Subcellular location [CC]'].astype(str)  # Add this line

    # Encode sequences
    seq_encoded = data['Sequence'].apply(encode_sequence)
    X = pad_sequences(seq_encoded, maxlen=None, dtype='int32', padding='post', value=0.0)

    # Encode subcellular localizations
    lb = LabelBinarizer()
    y = lb.fit_transform(data['Subcellular location [CC]'])

    return X, y
