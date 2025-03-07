# SMM4H-HeaRD @AAAI-ICWSM-2025 Shared Task 4: Detection of Insomnia in Clinical Notes

## Task Overview

This text classification shared task is divided into three distinct subtasks:

- **Subtask 1: Binary Text Classification**
Participants are given a clinical note and must determine whether the patient described in the note is likely to suffer from insomnia ("yes" or "no").

- **Subtask 2A: Multi-label Text Classification**
Participants evaluate each clinical note against the defined Insomnia rules: Definition 1, Definition 2, Rule A, Rule B, and Rule C. They must predict whether each item is satisfied based on the information in the note ("yes" or "no").

- **Subtask 2B: Evidence-Based Classification**
This task extends Subtask 2A by requiring not only classification of each item but also the identification and extraction of text evidence from the clinical note that supports each classification. For items Definition 1, Definition 2, Rule B, and Rule C, participants must provide a label ("yes" or "no") and include specific text spans from the note that justify the classification. This subtask focuses on promoting transparency and explainability in NLP models by requiring justification for each decision made.

For each subtask, ground truth annotations are provided in JSON format. Participants are required to submit their system outputs following the same format as the ground truth annotations provided by the organizers.

## Evaluation

## Data

This shared task utilizes a corpus of clinical notes derived from the MIMIC-III Database. The clinical notes have been augmented with additional structured patient information, specifically sex, age, and the medications prescribed during their hospital stay.

Participants are required to complete necessary training and sign a data usage agreement to access the [MIMIC-III Clinical Database (v1.4)](https://physionet.org/content/mimiciii/1.4/). After gaining access and downloading the files, participants must run the `text_mimic_notes.py` script to retrieve clinical notes and associated patient information using the provided note IDs. This process builds the corpus utilized in this shared task, as detailed in the instructions provided below.

### MIMIC-III Notes Processing

The `text_mimic_notes.py` Python script is designed to retrieve clinical notes and patient information from the MIMIC-III clinical database. The script takes a text file containing note IDs, and merges it with the content of the notes from MIMIC-III, including additional demographic and prescription information.

#### Requirements

- Python 3.6 or higher
- pandas library
- datetime module

#### Usage

The script requires three command-line arguments:
- `--note_ids_path`: The file path to the text file containing the note IDs.
- `--mimic_path`: The directory path containing the MIMIC-III v1.4 CSV files (`NOTEEVENTS.csv.gz`, `PRESCRIPTIONS.csv.gz` and `PATIENTS.csv.gz`).
- `--output_path`: The file path where the processed corpus CSV will be saved. This output CSV file will have two columns: the note IDs and the textual data retrieved from MIMIC-III.

#### Command Syntax

The script is executed from the command line with the following syntax:

```bash
python text_mimic_notes.py --ann_path [path_to_note_ids_txt] --mimic_path [path_to_mimic_csv_directory] --output_path [path_to_output_csv]
```

#### Example Command

Here is an example command that illustrates how to run the script using specific paths for each required input:

```bash
python text_mimic_notes.py --note_ids_path ./training/sample_note_ids.txt  --mimic_path ./mimic-iii/1.4 --output_path ./training/sample_corpus.csv
```

This command will process the note IDs from `./training/sample_note_ids.txt`, merge them with the data found in `./mimic-iii/1.4`, and output the resulting corpus to `./training/sample_corpus.csv`.
