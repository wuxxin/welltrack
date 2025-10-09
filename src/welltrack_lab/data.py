# SPDX-FileCopyrightText: 2024-present wuxxin <wuxxin@wuxxin.dev>
#
# SPDX-License-Identifier: BSD-3-Clause

import json
import pandas as pd
from datetime import timedelta

def load_data(file_content):
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

def get_welltrack_day(series, start_time_str='05:00'):
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
    offset = pd.to_timedelta(f'{start_time.hour}h {start_time.minute}m')
    return (series - offset).dt.floor('D')

def process_metrics(metrics_df, settings_df):
    """
    Processes the raw metrics DataFrame to make it analysis-ready.

    Args:
        metrics_df (pd.DataFrame): The raw metrics DataFrame.
        settings_df (pd.DataFrame): The settings DataFrame.

    Returns:
        pd.DataFrame: The processed metrics DataFrame.
    """
    if metrics_df.empty:
        return metrics_df

    df = metrics_df.copy()

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate WellTrack Day
    start_time = settings_df['dayStartTime'].iloc[0] if not settings_df.empty else '05:00'
    df['wt_day'] = get_welltrack_day(df['timestamp'], start_time)

    # Extract metric type
    df['metric_type'] = df['metric'].apply(lambda x: x.split('_')[0])

    # Normalize labels
    if 'labels' in df.columns and not df['labels'].empty:
        labels_df = pd.json_normalize(df['labels']).add_prefix('label.')
        df = pd.concat([df.drop('labels', axis=1), labels_df], axis=1)

    return df

def create_timeslot_sums(metrics_df, metric_type='pain'):
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

    metric_df = metrics_df[metrics_df['metric_type'] == metric_type].copy()
    if metric_df.empty:
        return pd.DataFrame()

    metric_df['timeslot'] = metric_df['timestamp'].dt.floor('10min')

    # Group by timeslot and the specific body part or mood name
    group_col = 'label.name'
    if group_col not in metric_df.columns:
        return pd.DataFrame()

    sum_df = metric_df.groupby(['timeslot', group_col])['value'].sum().reset_index()
    return sum_df

def calculate_distribution(df, value_col, group_by_col):
    """
    Calculates the percentage distribution of values within groups.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        value_col (str): The column with values to sum.
        group_by_col (str): The column to group by.

    Returns:
        pd.DataFrame: A DataFrame with the percentage distribution.
    """
    if df.empty or value_col not in df.columns or group_by_col not in df.columns:
        return pd.DataFrame()

    total_sum = df[value_col].sum()
    if total_sum == 0:
        return pd.DataFrame()

    distribution = df.groupby(group_by_col)[value_col].sum().reset_index()
    distribution['percentage'] = (distribution[value_col] / total_sum) * 100
    return distribution.sort_values('percentage', ascending=False)

def get_daily_summary(processed_df, metric_type):
    """
    Creates a daily summary of a specific metric type.

    Args:
        processed_df (pd.DataFrame): The processed metrics DataFrame.
        metric_type (str): The metric type to summarize ('pain', 'mood', or 'event').

    Returns:
        pd.DataFrame: A DataFrame with daily aggregated values.
    """
    if processed_df.empty:
        return pd.DataFrame()

    df = processed_df[processed_df['metric_type'] == metric_type].copy()
    if df.empty:
        return pd.DataFrame()

    daily_summary = df.groupby(['wt_day', 'label.name'])['value'].sum().unstack(fill_value=0)

    daily_summary['total'] = daily_summary.sum(axis=1)

    return daily_summary.reset_index()


def prepare_correlation_data(processed_df):
    """
    Prepares mood data for correlation analysis.

    Args:
        processed_df (pd.DataFrame): The processed metrics DataFrame.

    Returns:
        pd.DataFrame: A pivoted DataFrame suitable for correlation.
    """
    if processed_df.empty:
        return pd.DataFrame()

    mood_df = processed_df[processed_df['metric_type'] == 'mood'].copy()
    if mood_df.empty:
        return pd.DataFrame()

    mood_df['timeslot'] = mood_df['timestamp'].dt.floor('10min')

    correlation_df = mood_df.pivot_table(
        index='timeslot',
        columns='label.name',
        values='value',
        aggfunc='sum'
    ).fillna(0)

    return correlation_df