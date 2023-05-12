import os
import argparse
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, Embedding, Bidirectional, GRU
from keras.optimizers import Adam
from keras.regularizers import l1_l2, l2
from keras.callbacks import EarlyStopping
from data_processing import load_data, preprocess_data, check_file_format


def create_model(input_length, output_length):
    """
    Create and return the improved LSTM model.

    Parameters:
    input_length (int): The length of the input sequences.
    output_length (int): The length of the output sequences.

    Returns:
    Sequential: The created Keras Sequential model.
    """
    model = Sequential()
    
    # Embedding layer for protein sequences
    model.add(Embedding(21, 128, input_length=input_length))

    # Bidirectional GRU layers
    model.add(Bidirectional(GRU(256, return_sequences=True)))
    model.add(Bidirectional(GRU(256)))

    # Dropout and Dense layers with L1 and L2 regularization
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4), bias_regularizer=l2(1e-4)))
    model.add(Dropout(0.5))

    """
    Regularization helps prevent overfitting by adding penalties to the loss function 
    based on the weights of the model. L1 regularization adds a penalty proportional to the 
    absolute value of the weights, while L2 regularization adds a penalty proportional 
    to the square of the weights.
    """

    # Output layer
    model.add(Dense(output_length, activation='softmax'))

    model.compile(
        optimizer=Adam(learning_rate=0.0005),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def train_and_evaluate_model(model, X, y):
    """
    Train and evaluate the improved LSTM model.

    Parameters:
    X (array-like): The preprocessed protein sequences.
    y (array-like): The preprocessed protein subcellular localizations.

    Returns:
    None
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    input_length = X_train.shape[1]

    model = create_model(input_length, y_train.shape[1])

    # Early stopping to avoid overfitting
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=64, callbacks=[early_stopping])

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

