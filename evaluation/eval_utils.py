import json
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report


# Define class mappings
POSITIVE_CLASS = 'yes'
NEGATIVE_CLASS = 'no'
MAP_CLASS = {
    POSITIVE_CLASS: 1,
    NEGATIVE_CLASS: 0
}


def check_gs_pred_note_ids(df_gs, df_pred):
    """
    Check if all note IDs in the gold standard are present in the predictions.

    Args:
        df_gs (DataFrame): DataFrame containing the Gold Standard annotations
        df_pred (DataFrame): DataFrame containing the system predictions

    Raises:
        ValueError: If note IDs in the gold standard are missing from the predictions
    """
    missing_ids = df_gs.index.difference(df_pred.index)
    if not missing_ids.empty:
        raise ValueError(
            f"Missing the following note IDs in predictions: {', '.join(map(str, missing_ids))}"
        )


def read_and_validate_json(json_path, labels, data_name='system predictions'):
    """
    Generic function to read and validate JSON data.

    Args:
        json_path (str): Path to the JSON file
        labels (list): List of labels to validate in the JSON data
        data_name (str): Description of the data (either 'gold standard' or 'system predictions')

    Returns:
        DataFrame: DataFrame with note IDs as indices and required labels as columns

    Raises:
        ValueError: If the JSON data is malformed or labels are incorrect
    """
    with open(json_path, 'r') as file:
        data = json.load(file)

    validated_data = {}
    for note_id, content in data.items():
        validated_data[note_id] = {}
        for label in labels:
            if label not in content:
                raise ValueError(f"Missing '{label}' label for note {note_id} in {data_name}")
            
            label_value = content[label].lower()
            if label_value not in [POSITIVE_CLASS, NEGATIVE_CLASS]:
                raise ValueError(
                    f"Incorrect value for '{label}' label at note {note_id} in {data_name}: {content[label]}. "
                    f"Expected '{POSITIVE_CLASS}' or '{NEGATIVE_CLASS}'."
                )
            validated_data[note_id][label] = MAP_CLASS[label_value]

    return pd.DataFrame.from_dict(validated_data, orient='index')


def subtask_2b_read_and_validate_json(json_path, labels, data_name='system predictions'):
    """
    Function to read and validate JSON data from Subtask 2B, ensuring each item's format is correct,
    and that the text spans align with the assigned labels.

    Args:
        json_path (str): Path to the JSON file
        labels (list): List of labels to validate in the JSON data
        data_name (str): Description of the data (either 'gold standard' or 'system predictions')

    Returns:
        dict: Dictionary with note IDs as keys and validated label and text data as values

    Raises:
        ValueError: If the JSON data is malformed or labels are incorrect
    """
    with open(json_path, 'r') as file:
        data = json.load(file)

    validated_data = {}
    for note_id, content in data.items():
        validated_data[note_id] = {}
        for label in labels:
            if label not in content:
                raise ValueError(f"Missing '{label}' label for note {note_id} in {data_name}")
            
            label_content = content[label]
            if not isinstance(label_content, dict):
                raise ValueError(
                    f"Incorrect format for '{label}' label at note {note_id} in {data_name}: {label_content}. "
                    f"Expected dict with 'label' and 'text' keys."
                )

            # 'label' key
            if 'label' not in label_content:
                raise ValueError(f"Missing 'label' key in '{label}' for note {note_id} in {data_name}")
            label_content_value = label_content['label'].lower()
            if label_content_value not in [POSITIVE_CLASS, NEGATIVE_CLASS]:
                raise ValueError(
                    f"Incorrect 'label' for '{label}' at note {note_id} in {data_name}: {label_content['label']}. "
                    f"Expected '{POSITIVE_CLASS}' or '{NEGATIVE_CLASS}'."
                )

            # 'text' key
            if 'text' not in label_content:
                raise ValueError(f"Missing 'text' key in '{label}' for note {note_id} in {data_name}")
            if not isinstance(label_content['text'], list) or not all(isinstance(i, str) for i in label_content['text']):
                raise ValueError(
                    f"Incorrect 'text' format for '{label}' at note {note_id} in {data_name}: {label_content['text']}. "
                    f"Expected list of strings."
                )
            
            # Check 'label' and 'text' consistency
            if label_content_value == POSITIVE_CLASS and len(label_content['text']) == 0:
                raise ValueError(
                    f"Empty 'text' list for positive '{label}' at note {note_id} in {data_name}. "
                    f"Expected non-empty list."
                )
            if label_content_value == NEGATIVE_CLASS and len(label_content['text']) > 0:
                raise ValueError(
                    f"Non-empty 'text' list for negative '{label}' at note {note_id} in {data_name}. "
                    f"Expected empty list."
                )

            # Store the validated label and text
            validated_data[note_id][label] = {
                'label': label_content_value,
                'text': label_content['text'],
            }

    return validated_data


def compute_metrics(labels, preds, average='binary', target_names=[NEGATIVE_CLASS, POSITIVE_CLASS]):
    """
    Compute precision, recall, and F1-score for the given labels and predictions.

    Args:
        labels (Series): True labels
        preds (Series): Predicted labels
        average (str): Type of averaging performed on the metrics depending on the task.
            Expected values are: 'binary' (Subtask 1) or 'micro' (Subtask 2A)
        target_names (list): List of target names for classification report

    Returns:
        dict: Dictionary containing precision, recall, and F1-score
    """
    print(classification_report(
        y_true=labels,
        y_pred=preds,
        digits=4,
        zero_division=0.0,
        target_names=target_names
    ))
    return {
        'Precision': round(
            precision_score(
                y_true=labels,
                y_pred=preds,
                average=average
            ), 4
        ),
        'Recall': round(
            recall_score(
                y_true=labels,
                y_pred=preds,
                average=average
            ), 4
        ),
        'F1-score': round(
            f1_score(
                y_true=labels,
                y_pred=preds,
                average=average
            ), 4
        ),
    }


def subtask_2b_compute_metrics(dict_gs, dict_pred, arr_labels, rouge_scorer):
    """
    Calculates the ROUGE-L score for the given gold standard and prediction dictionaries
    based on the provided labels. This function is designed to evaluate text spans extracted
    from clinical notes for subtask 2B which requires justification of classifications with text evidence.

    Args:
        dict_gs (dict): A dictionary containing the gold standard data with note IDs as keys and
                        dictionaries of labels and their corresponding text evidence as values.
        dict_pred (dict): A dictionary containing the prediction data in the same format as dict_gs.
        arr_labels (list): A list of provided labels (str).
        rouge_scorer (ROUGE Scorer object): An instantiated ROUGE scorer object used to compute ROUGE-L scores.

    Returns:
        float: The average ROUGE-L score across all provided labels and notes, providing a measure
               of the similarity between the predicted text and the gold standard."
    """
    dict_results = {label: [] for label in arr_labels}
    for note_id in dict_gs:
        gs_note_id = dict_gs[note_id]
        pred_note_id = dict_pred[note_id]

        for label in arr_labels:
            gs_text = ' '.join(gs_note_id[label]['text'])
            pred_text = ' '.join(pred_note_id[label]['text'])

            if gs_text or pred_text: # Calculate ROUGE-L only if there's text to compare
                dict_results[label].append(
                    rouge_scorer.score(
                        target=gs_text,
                        prediction=pred_text,
                    )["rougeL"].fmeasure
                )

    # Calculate the average ROUGE-L score for each label
    dict_results_avg = {label: None for label in arr_labels}
    arr_results = []
    for label in arr_labels:
        if dict_results[label]:
            avg_score = sum(dict_results[label]) / len(dict_results[label])
            dict_results_avg[label] = round(avg_score, 4)
            arr_results.append(avg_score)
    print("Average ROUGE-L scores per label:")
    print(dict_results_avg)

    # Return the overall average ROUGE-L score
    result = 0.0
    if arr_results:
        result = round(sum(arr_results) / len(arr_results), 4)
    return result
