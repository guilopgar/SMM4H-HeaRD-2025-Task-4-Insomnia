import argparse
import pandas as pd
import eval_utils
from rouge_score import rouge_scorer

def main(gs_path, pred_path):
    """
    Main function to evaluate the system predictions against the gold standard annotations for Subtask 2B.

    Args:
        gs_path (str): Path to the JSON file containing the Gold Standard annotations
        pred_path (str): Path to the JSON file containing the system predictions
    """
    arr_labels = ['Definition 1', 'Definition 2', 'Rule B', 'Rule C']
    
    # Load data from JSON files
    dict_gs = eval_utils.subtask_2b_read_and_validate_json(
        json_path=gs_path,
        data_name='gold standard',
        labels=arr_labels
    )
    dict_pred = eval_utils.subtask_2b_read_and_validate_json(
        json_path=pred_path,
        data_name='system predictions',
        labels=arr_labels
    )

    # Check for matching note IDs between gold standard and predictions
    eval_utils.check_gs_pred_note_ids(
        df_gs=pd.DataFrame(dict_gs).T,
        df_pred=pd.DataFrame(dict_pred).T
    )

    # Compute evaluation metrics
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
    result = eval_utils.subtask_2b_compute_metrics(
        dict_gs=dict_gs,
        dict_pred=dict_pred,
        arr_labels=arr_labels,
        rouge_scorer=scorer
    )
    print("\nEvaluation results for Subtask 2B:")
    print(f"Average ROUGE-L score across all labels: {result}")


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Evaluate predictions for Subtask 2B of the Insomnia detection task.")
    parser.add_argument(
        "-g",
        "--gs_path",
        type=str,
        required=True,
        help="File path to the JSON file containing the Gold Standard annotations"
    )
    parser.add_argument(
        "-p",
        "--pred_path",
        type=str,
        required=True,
        help="File path to the JSON file containing the system predictions"
    )

    # Parse arguments
    args = parser.parse_args()

    # Run script
    main(
        gs_path=args.gs_path,
        pred_path=args.pred_path
    )
