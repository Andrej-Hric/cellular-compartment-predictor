import os
import mimetypes
import argparse
import sys
import pandas as pd
import numpy as np
from Bio import SeqIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_data(file_path):
    """
    Load data from a file.

    Parameters:
    file_path (str): The path to the input file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    file_type = mimetypes.guess_type(file_path)[0]

    if file_type == 'text/csv':
        data = pd.read_csv(file_path)
    elif file_type == 'text/plain':
        with open(file_path) as file:
            data = pd.DataFrame([line.strip() for line in file], columns=['Sequence'])
    elif file_type == 'application/gff' or file_type == 'application/octet-stream':
        data = pd.DataFrame([{'ID': record.id, 'Sequence': str(record.seq)} for record in SeqIO.parse(file_path, 'fasta')])
    elif file_type == 'application/fasta':
        data = pd.DataFrame([{'ID': record.id, 'Sequence': str(record.seq)} for record in SeqIO.parse(file_path, 'fasta')])
    else:
        print(f'Error: The input file type {file_type} is not supported.')
        sys.exit(1)

    return data

def validate_sequence(sequence):
    """
    Validate a protein sequence, ensuring it only contains valid amino acid characters.

    Parameters:
    sequence (str): The protein sequence to validate.

    Returns:
    bool: True if the sequence is valid, False otherwise.
    """
    valid_amino_acids = 'ARNDCQEGHILKMFPSTWYV'
    for char in sequence:
        if char not in valid_amino_acids:
            return False
    return True

def preprocess_data(data):
    """
    Preprocess protein sequences and subcellular localizations.

    Parameters:
    data (pd.DataFrame): A DataFrame containing protein sequences and subcellular localizations.

    Returns:
    tuple: A tuple containing the preprocessed sequences (X) and subcellular localizations (y).
    """
    data = data.dropna(subset=['Sequence'])
    data['Sequence'] = data['Sequence'].apply(lambda x: x.upper())
    data = data[data['Sequence'].apply(validate_sequence)]

    if 'Subcellular location [CC]' not in data.columns:
        return data['Sequence'].apply(encode_sequence).tolist(), None

    data = data.dropna(subset=['Subcellular location [CC]'])

    X = data['Sequence'].apply(encode_sequence).tolist()
    y = data['Subcellular location [CC]']

    lb = LabelBinarizer()
    y = lb.fit_transform(y)

    return pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH), y

def create_model(input_shape, output_shape):
    """
    Create an LSTM model for protein subcellular localization prediction.

    Parameters:
    input_shape (tuple): The shape of the input data (sequences).
    output_shape (int): The number of unique subcellular localizations.

    Returns:
    Sequential: A Keras Sequential model.
    """
    model = Sequential()
    model.add(Embedding(input_dim=21, output_dim=32, input_length=input_shape[1]))
    model.add(LSTM(units=64, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(units=32))
    model.add(Dropout(0.5))
    model.add(Dense(output_shape, activation='softmax'))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    return model

def train_and_evaluate_model(X, y):
    """
    Train and evaluate the LSTM model.

    Parameters:
    X (array-like): The preprocessed protein sequences.
    y (array-like): The preprocessed subcellular localizations.

    Returns:
    None
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = create_model(X_train.shape, y_train.shape[1])
    model.summary()
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))

def main(input_file):
    """
    Main function to load data, preprocess it, and train and evaluate the LSTM model.

    Parameters:
    input_file (str): The path to the input file.

    Returns:
    None
    """
    data = load_data(input_file)
    X, y = preprocess_data(data)
    if y is None:
        print("Error: The input file must contain a 'Subcellular location [CC]' column.")
        return
    train_and_evaluate_model(X, y)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Protein Subcellular Localization Predictor")
    parser.add_argument("input_file", type=str, help="The path to the input file.")
    args = parser.parse_args()
    main(args.input_file)
