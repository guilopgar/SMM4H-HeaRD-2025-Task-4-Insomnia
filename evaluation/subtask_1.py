import argparse
import eval_utils


def main(gs_path, pred_path):
    """
    Main function to evaluate the system predictions against the gold standard annotations for Subtask 1.

    Args:
        gs_path (str): Path to the JSON file containing the Gold Standard annotations
        pred_path (str): Path to the JSON file containing the system predictions
    """

    # Load data from JSON files
    df_gs = eval_utils.read_and_validate_json(
        json_path=gs_path,
        data_name='gold standard',
        labels=['Insomnia']
    )
    df_pred = eval_utils.read_and_validate_json(
        json_path=pred_path,
        data_name='system predictions',
        labels=['Insomnia']
    )

    # Check for matching note IDs between gold standard and predictions
    eval_utils.check_gs_pred_note_ids(
        df_gs=df_gs,
        df_pred=df_pred
    )

    # Compute evaluation metrics
    result = eval_utils.compute_metrics(
        labels=df_gs["Insomnia"].values,
        preds=df_pred.loc[df_gs.index, "Insomnia"].values,
        average='binary',
        target_names=[eval_utils.NEGATIVE_CLASS, eval_utils.POSITIVE_CLASS]
    )
    print("Evaluation results for Subtask 1:")
    print(result)


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Evaluate predictions for Subtask 1 of the Insomnia detection task.")
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
