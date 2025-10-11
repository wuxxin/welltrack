import json
import pandas as pd
from datetime import timedelta


def load_from_json(file_content):
    """
    Loads WellTrack data from a JSON file content.

    Args:
        file_content (bytes): The content of the uploaded JSON file.

    Returns:
        tuple: A tuple containing three pandas DataFrames:
               metrics, event_types, and settings.
    """
    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        return None, None, None

    metrics_df = pd.DataFrame(data.get("metrics", []))
    event_types_df = pd.DataFrame(data.get("eventTypes", []))
    settings_data = data.get("settings", {})
    settings_df = pd.DataFrame([settings_data])

    return metrics_df, event_types_df, settings_df


def calc_welltrack_day(series, start_time_str="05:00"):
    """
    Calculates the 'WellTrack Day' for a pandas Series of timestamps.
    A WellTrack day starts at a custom time (e.g., 5:00 AM).

    Args:
        series (pd.Series): A pandas Series of timestamps.
        start_time_str (str): The start time of the day in 'HH:MM' format.

    Returns:
        pd.Series: A pandas Series with the calculated WellTrack day for each timestamp.
    """
    start_time = pd.to_datetime(start_time_str).time()
    offset = pd.to_timedelta(f"{start_time.hour}h {start_time.minute}m")
    return (series - offset).dt.floor("D")


def process_metrics(metrics_df, event_types_df, settings_df):
    """
    Processes the raw metrics DataFrame to make it analysis-ready.

    Args:
        metrics_df (pd.DataFrame): The raw metrics DataFrame.
        event_types_df (pd.DataFrame): The raw event_types DataFrame.
        settings_df (pd.DataFrame): The settings DataFrame.

    Returns:
        pd.DataFrame: The processed metrics DataFrame.
    """
    if metrics_df.empty:
        return metrics_df

    df = metrics_df.copy()

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Calculate WellTrack Day
    # start_time = settings_df["dayStartTime"].iloc[0] if not settings_df.empty else "05:00"
    start_time = "05:00"
    df["wt_day"] = calc_welltrack_day(df["timestamp"], start_time)

    # Extract metric type
    df["metric_type"] = df["metric"].apply(lambda x: x.split("_")[0])

    # Normalize labels
    if "labels" in df.columns and not df["labels"].empty:
        labels_df = pd.json_normalize(df["labels"]).add_prefix("label.")
        df = pd.concat([df.drop("labels", axis=1), labels_df], axis=1)

    return df


def create_timeslot_sums(metrics_df, metric_type="pain"):
    """
    Aggregates pain or mood metrics into 10-minute timeslots.

    Args:
        metrics_df (pd.DataFrame): The processed metrics DataFrame.
        metric_type (str): The type of metric to aggregate ('pain' or 'mood').

    Returns:
        pd.DataFrame: A DataFrame with summed values per timeslot.
    """
    if metrics_df.empty:
        return pd.DataFrame()

    metric_df = metrics_df[metrics_df["metric_type"] == metric_type].copy()
    if metric_df.empty:
        return pd.DataFrame()

    metric_df["timeslot"] = metric_df["timestamp"].dt.floor("10min")

    # Group by timeslot and the specific body part or mood name
    group_col = "label.name"
    if group_col not in metric_df.columns:
        return pd.DataFrame()

    sum_df = metric_df.groupby(["timeslot", group_col])["value"].sum().reset_index()
    return sum_df
