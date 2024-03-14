"""
Script Name: Anonymize Reports

Description:
This script anonymizes sensitive information in text data contained within a
specified column of a CSV file. It uses a named entity recognition (NER) model
to identify sensitive information and then anonymizes these details. The script
supports customizable NER models and anonymization strategies. Users can specify
the input and output file paths, the data column to anonymize, and various options
for the NER model and anonymization process.

Usage:
python anonymize_reports.py --st_model [MODEL_PATH] --st_model_package [MODEL_PACKAGE]
                            --st_ta_key [TA_KEY] --st_ta_endpoint [TA_ENDPOINT]
                            --report_file [INPUT_CSV] --save_file [OUTPUT_CSV]
                            --data_column [COLUMN_NAME] --append [True/False]
"""

import argparse
import pandas as pd
from tqdm import tqdm
from presidio_helpers import analyzer_engine, analyze, anonymize


def main(args, reports):
    """
    Process the given reports for analysis and anonymization.

    Parameters:
    - args: The argparse.Namespace containing command-line arguments.
    - reports: The pandas DataFrame containing the reports to be processed.

    Returns:
    - A pandas DataFrame with the anonymized reports.
    """
    # instantiate and cache AnalyzerEngine
    analyzer_params = (args.st_model_package, args.st_model, args.st_ta_key, args.st_ta_endpoint)
    analyzer = analyzer_engine(*analyzer_params)

    result = []
    for idx, row in tqdm(reports.iterrows(), total=len(reports)):
        try:
            st_text = row[args.data_column]

            # Analyze
            st_analyze_results = analyze(
                analyzer_engine=analyzer,
                text=st_text,
                entities="All",
                language="en",
                score_threshold=0.35,
                return_decision_process=True,
                allow_list=[],
                deny_list=[],
            )

            # Anonymize
            st_anonymize_results = anonymize(
                text=st_text,
                operator="replace",
                mask_char=None,
                number_of_chars=None,
                encrypt_key=None,
                analyze_results=st_analyze_results,
            )

            assert st_anonymize_results.text != ""

            result.append({
                f'{args.data_column}_anon': st_anonymize_results.text,
            })

        except AssertionError:
            print(f'Idx: {idx} anonymization failed.')

    return pd.DataFrame(result)


if __name__ == '__main__':

    # Parse the arguments
    parser = argparse.ArgumentParser(description='Data Anonymization Script')
    parser.add_argument('--st_model', default='/mnt/data/stanford-deidentifier-base', help='Model path for NER')
    parser.add_argument('--st_model_package', default='HuggingFace', help='Model package for NER')
    parser.add_argument('--st_ta_key', default='None', help='Text Analytics key (if using Azure)')
    parser.add_argument('--st_ta_endpoint', default='None', help='Text Analytics endpoint (if using Azure)')
    parser.add_argument('--report_file', default='sample_reports.csv', help='Path to the input report file')
    parser.add_argument('--save_file', default='output.csv', help='Path to save the anonymized report')
    parser.add_argument('--data_column', default='report', help='Column name of the reports in csv')
    parser.add_argument('--append', default=False, help='Append anonymized report to input csv')
    args = parser.parse_args()

    # Load and preprocess reports
    reports = pd.read_csv(args.report_file)
    reports[args.data_column] = reports[args.data_column].fillna('None')

    # Process and anonymize reports
    anon_report = main(args, reports)

    # Optionally append the anonymized report to the original and save
    if args.append:
        combined_report = pd.concat([reports, anon_report], axis=1)
        combined_report.to_csv(args.save_file, index=False)
    else:
        anon_report.to_csv(args.save_file, index=False)
