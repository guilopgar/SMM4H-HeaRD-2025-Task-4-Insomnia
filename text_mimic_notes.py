import os
import pandas as pd
from datetime import datetime
import argparse


def age_to_decade(age):
    """
    Converts an integer age into a decade bucket.

    Args:
        age (int): The age to convert.

    Returns:
        str: A string representing the decade bucket.
    """
    if age < 0:
        return "Invalid age"  # Handling negative ages if any
    decades = [
        'zero', 'ten', 'twenties', 'thirties', 'forties', 'fifties',
        'sixties', 'seventies', 'eighties', 'nineties', 'hundreds'
    ]
    index = age // 10  # Find the decade index (e.g., 74 // 10 = 7)
    if index >= len(decades):
        index = -1  # Handling ages 100 and above
    return decades[index]


def main(note_ids_path, mimic_path, output_path):
    """
    Main function to process note IDs and MIMIC-III notes into a combined dataset.
    
    Args:
        note_ids_path (str): Path to the text file containing note IDs.
        mimic_path (str): Directory path containing MIMIC-III CSV files.
        output_path (str): Output path for the processed corpus CSV file.
    """
    # Data loading
    arr_note_ids = []
    with open(note_ids_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                arr_note_ids.append(int(line))

    df_mimic_note = pd.read_csv(
        os.path.join(mimic_path, 'NOTEEVENTS.csv.gz'),
        sep=','
    )
    df_mimic_note.index = df_mimic_note["ROW_ID"].values

    df_mimic_presc = pd.read_csv(
        os.path.join(mimic_path, 'PRESCRIPTIONS.csv.gz'),
        sep=','
    )
    
    df_mimic_patient = pd.read_csv(
        os.path.join(mimic_path, 'PATIENTS.csv.gz'),
        sep=','
    )

    # Tables mapping
    df_data = pd.DataFrame({"note_id": arr_note_ids})
    df_data.index = df_data["note_id"].values

    df_data["subject_id"] = df_mimic_note.loc[df_data.index, "SUBJECT_ID"]
    df_data["hadm_id"] = df_mimic_note.loc[df_data.index, "HADM_ID"]
    df_data["text_mimic"] = df_mimic_note.loc[df_data.index, "TEXT"]
    df_data["note_date"] = df_mimic_note.loc[df_data.index, "CHARTDATE"]

    # Prescriptions
    df_data["hadm_id_int"] = df_data["hadm_id"].astype(int)
    df_data_presc = pd.merge(
        left=df_data,
        right=df_mimic_presc[["SUBJECT_ID", "HADM_ID", "DRUG", "STARTDATE"]],
        how='left',
        left_on=["subject_id", "hadm_id_int"],
        right_on=["SUBJECT_ID", "HADM_ID"]
    )
    df_data_presc_nan = df_data_presc[~df_data_presc["STARTDATE"].apply(pd.isna)].copy()
    df_data_presc_filt = df_data_presc_nan[
        df_data_presc_nan["note_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d")) >= \
        df_data_presc_nan["STARTDATE"].apply(lambda x: datetime.strptime(str(x).split(' ')[0], "%Y-%m-%d"))
    ].copy()

    arr_drugs = df_data_presc_filt.groupby('note_id')['DRUG'].apply(lambda x: [drug for drug in x if not pd.isna(drug)])

    for note_id in df_data["note_id"].values:
        if note_id not in arr_drugs:
            arr_drugs[note_id] = []

    df_data['drug'] = arr_drugs[df_data.index]
    df_data['drug_pre'] = df_data['drug'].apply(
        lambda x: ', '.join(
            pd.Series(x).drop_duplicates(keep='first').to_list()
        ) if len(x) else "no drugs"
    )

    # Demographic information
    df_data_patient = pd.merge(
        left=df_data,
        right=df_mimic_patient[["SUBJECT_ID", "GENDER", "DOB"]],
        how='left',
        left_on=["subject_id"],
        right_on=["SUBJECT_ID"]
    )
    df_data_patient.index = df_data_patient["note_id"]
    df_data["gender"] = df_data_patient.loc[df_data.index, "GENDER"]
    df_data["dob"] = df_data_patient.loc[df_data.index, "DOB"]

    df_data["gender_pre"] = df_data["gender"].map({"F": "female", "M": "male"})

    df_data["age"] = df_data.apply(
        lambda x: int((datetime.strptime(x["note_date"], "%Y-%m-%d") - datetime.strptime(x["dob"], "%Y-%m-%d %H:%M:%S")).days / 365),
        axis=1
    )
    df_data["age_pre"] = df_data["age"].apply(age_to_decade)

    # Final text assembly
    df_data["text_pref"] = df_data.apply(
        lambda row: f"{row['gender_pre']} patient in {row['age_pre']} prescribed {row['drug_pre']}\n",
        axis=1
    )
    df_data["text"] = df_data.apply(lambda row: f"{row['text_pref']}\n{row['text_mimic']}", axis=1)
    
    # Save data
    df_data.loc[arr_note_ids, ["note_id", "text"]].to_csv(output_path, sep=',', index=False)


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Process and combine note IDs with MIMIC-III notes into a single dataset.")
    parser.add_argument(
        "-n",
        "--note_ids_path",
        type=str,
        required=True,
        help="Path to the text file containing note IDs"
    )
    parser.add_argument(
        "-m",
        "--mimic_path",
        type=str,
        required=True,
        help="Directory path containing the following CSV files from MIMIC-III v1.4: NOTEEVENTS.csv.gz, PRESCRIPTIONS.csv.gz and PATIENTS.csv.gz"
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="./corpus.csv",
        help="Output path for the processed corpus CSV file"
    )

    # Parse arguments
    args = parser.parse_args()

    # Run script
    main(
        note_ids_path=args.note_ids_path,
        mimic_path=args.mimic_path,
        output_path=args.output_path
    )
