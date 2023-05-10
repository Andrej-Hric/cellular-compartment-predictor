import argparse
import pandas as pd
from model import train_and_evaluate_model, predict, save_model, load_saved_model
from data_processing import load_data, preprocess_data, check_file_format

def format_predictions(predictions, data):
    """
    Format the predictions into a list of dictionaries containing protein IDs and predicted localizations.

    Parameters:
    predictions (array-like): The predicted subcellular localizations.
    data (pd.DataFrame): The original data with protein IDs.

    Returns:
    list: A list of dictionaries containing protein IDs and predicted localizations.
    """
    formatted_predictions = []
    for i, pred in enumerate(predictions):
        protein_id = data.iloc[i]['ID']
        localization = pred.argmax()  # Assuming localizations are one-hot encoded
        formatted_predictions.append({'ID': protein_id, 'Subcellular Localization': localization})

    return formatted_predictions

def output_results(formatted_predictions, output_file):
    """
    Save the results to the output file.

    Parameters:
    formatted_predictions (list): A list of dictionaries containing protein IDs and predicted localizations.
    output_file (str): The path to the output file.

    Returns:
    None
    """
    df = pd.DataFrame(formatted_predictions)
    df.to_csv(output_file, index=False)

def main(input_file, output_file, model_file=None):
    """
    Main function to load data, preprocess it, and train, evaluate, and predict using the LSTM model.

    Parameters:
    input_file (str): The path to the input file.
    output_file (str): The path to the output file.
    model_file (str, optional): The path to the saved model file. Defaults to None.

    Returns:
    None
    """
    if not check_file_format(input_file, 'input'):
        print("Error: The input file must be in a supported format (CSV, FASTA, GFF, or TXT).")
        return

    if not check_file_format(output_file, 'output'):
        print("Error: The output file must be in CSV format.")
        return

    data = load_data(input_file)
    X, y = preprocess_data(data)

    if model_file:
        model = load_saved_model(model_file)
    else:
        model = create_model(X.shape[1], y.shape[1])
        train_and_evaluate_model(model, X, y)
        save_model(model, "trained_model.h5")  # Save the model in HDF5 format

    predictions = predict(model, X)
    formatted_predictions = format_predictions(predictions, data)
    output_results(formatted_predictions, output_file)

    if model_file:
        save_model(model, model_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Protein Subcellular Localization Predictor")
    parser.add_argument("input_file", type=str, help="The path to the input file.")
    parser.add_argument("output_file", type=str, help="The path to the output file.")
    parser.add_argument("--model_file", type=str, help="The path to the saved model file.", default=None)
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.model_file)

