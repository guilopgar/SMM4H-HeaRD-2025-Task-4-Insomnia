# SMM4H-HeaRD-2025-Task-4-Insomnia

## MIMIC-III Notes Processing Script

This Python script is designed to merge annotation data with patient notes and prescription data from the MIMIC-III clinical database. The script takes annotation data, merges it with relevant clinical data from MIMIC-III, and outputs a combined corpus with additional demographic and prescription information..

### Requirements

- Python 3.6 or higher
- pandas library
- datetime module

### Usage

The script requires three command-line arguments:
- `--ann_path`: The file path to the CSV containing the annotations.
- `--mimic_path`: The directory path containing the MIMIC-III CSV files (`NOTEEVENTS.csv.gz`, `PRESCRIPTIONS.csv.gz`, `PATIENTS.csv.gz`).
- `--output_path`: The file path where the processed corpus CSV will be saved.

### Command Syntax

The script is executed from the command line with the following syntax:

```bash
python text_mimic_notes.py --ann_path [path_to_annotation_csv] --mimic_path [path_to_mimic_csv_directory] --output_path [path_to_output_csv]
```

### Example Command

Here is an example command that illustrates how to run the script using specific paths for each required input:

```bash
python text_mimic_notes.py --ann_path ./training/subtask_1/sample.csv --mimic_path ./mimic-iii/1.4 --output_path ./training/subtask_1/sample_corpus.csv
```

