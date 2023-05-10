import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
from data_processing import load_data, preprocess_data, check_file_format


def create_model(input_length):
    """
    Create and return the LSTM model.

    Parameters:
    input_length (int): The length of the input sequences.

    Returns:
    Sequential: The created Keras Sequential model.
    """
    model = Sequential()
    model.add(Embedding(21, 128, input_length=input_length))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(9, activation='softmax'))

    model.compile(
        optimizer=Adam(lr=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def train_and_evaluate_model(model, X, y):
    """
    Train and evaluate the LSTM model.

    Parameters:
    X (array-like): The preprocessed protein sequences.
    y (array-like): The preprocessed protein subcellular localizations.

    Returns:
    None
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    input_length = X_train.shape[1]

    model = create_model(input_length)
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

    scores = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {scores[1] * 100:.2f}%")


def predict(model, X):
    """
    Predict the localization of a protein using the trained model.

    Parameters:
    model (Sequential): The trained Keras Sequential model.
    X (array-like): The preprocessed protein sequences.

    Returns:
    array-like: The predicted subcellular localizations.
    """
    return model.predict(X)


def save_model(model, file_path):
    """
    Save the trained model to a file.

    Parameters:
    model (Sequential): The trained Keras Sequential model.
    file_path (str): The path to the output file.

    Returns:
    None
    """
    model.save(file_path)


def load_saved_model(file_path):
    """
    Load the trained model from a file.

    Parameters:
    file_path (str): The path to the input file.

    Returns:
    Sequential: The loaded Keras Sequential model.
    """
    return load_model(file_path)
