import os
from Bio import SeqIO

def import_libraries():
    global pd, np, train_test_split, LabelBinarizer, Sequential, LSTM, Dense, Dropout, Embedding, Adam, pad_sequences, SeqIO
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelBinarizer
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from Bio import SeqIO

def load_data(file_path, file_format='csv'):
    """Load data from a file (CSV, FASTA, GFF, or text).
    
    Supports CSV, FASTA, GFF, and simple text format files.
    
    Parameters:
    file_path (str): Path to the file containing the data.
    file_format (str): File format, one of 'csv', 'fasta', 'gff', 'txt'. Default is 'csv'.

    Returns:
    DataFrame: Loaded data as a pandas DataFrame.
    """
    if file_format == 'csv':
        return pd.read_csv(file_path)
    elif file_format in ['fasta', 'gff', 'txt']:
        sequences = []
        for record in SeqIO.parse(file_path, file_format):
            sequences.append(str(record.seq))
        return pd.DataFrame(sequences, columns=['Sequence'])
    else:
        raise ValueError("Invalid file format. Supported formats: 'csv', 'fasta', 'gff', 'txt'.")

def preprocess_data(data):
    """Preprocess protein sequences and subcellular localizations.
    
    Parameters:
    data (DataFrame): DataFrame containing protein sequences and subcellular localizations.

    Returns:
    tuple: A tuple containing preprocessed protein sequences (X) and subcellular localizations (y) as numpy arrays.
    """
    X = data['Sequence'].apply(lambda x: np.array([ord(c) - ord('A') + 1 for c in x])).tolist()
    X = pad_sequences(X, maxlen=500, padding='post', truncating='post')
    if 'Subcellular location [CC]' in data.columns:
        y = data['Subcellular location [CC]']
        label_binarizer = LabelBinarizer()
        y = label_binarizer.fit_transform(y)
    else:
        y = None
    return X, y

def create_model(input_shape, num_classes):
    """Create an LSTM model for sequence classification.
    
    Parameters:
    input_shape (tuple): Shape of the input data.
    num_classes (int): Number of classes in the target variable.

    Returns:
    Model: A compiled LSTM model for sequence classification.
    """
    model = Sequential()
    model.add(Embedding(input_dim=26, output_dim=64, input_length=input_shape[1]))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    return model

def test_preprocess_data():
    """Test the preprocess_data function."""
    data = pd.DataFrame({
        'Sequence': ['MSTNPKPQRK', 'NPKPQRK'],
        'Subcellular location [CC]': ['Cytoplasm', 'Nucleus']
    })
    X, y = preprocess_data(data)
    assert X.shape == (2, 500)
    assert y.shape == (2, 2)

def test_create_model():
    """Test the create_model function."""
    model = create_model((None, 500), 5)
    assert len(model.layers) == 7

if __name__ == '__main__':
    import_libraries()

    # Run tests
    test_preprocess_data()
    test_create_model()
    # Load data
    data = load_data("Uniprot_data.csv")

    # Preprocess data
    X, y = preprocess_data(data)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and compile the model
    model = create_model(X_train.shape, y.shape[1])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_split=0.2, epochs=8, batch_size=32)

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")


