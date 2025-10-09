#!/usr/bin/env python
"""
Filter misclicked mood entries from a WellTrack JSON export.

This script reads a WellTrack JSON export file, identifies mood entry
timeslots that contain only one or two entries, and filters them out.
A timeslot is defined as a 10-minute window starting from the first
mood entry in a potential group.

The filtered-out entries are printed to stderr, and the cleaned JSON
data is printed to stdout.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

def filter_misclicks(data):
    """
    Filters mood entries that are likely misclicks.

    Args:
        data (dict): The parsed WellTrack JSON data.

    Returns:
        dict: The WellTrack data with misclicked mood entries removed.
    """
    if 'metrics' not in data:
        return data

    all_metrics = data['metrics']
    mood_metrics = sorted([m for m in all_metrics if m['metric'].startswith('mood_')], key=lambda x: x['timestamp'])
    other_metrics = [m for m in all_metrics if not m['metric'].startswith('mood_')]

    if not mood_metrics:
        return data

    filtered_mood_metrics = []
    misclicked_metrics = []

    i = 0
    while i < len(mood_metrics):
        slot_start_time = mood_metrics[i]['timestamp']
        # 10 minutes in milliseconds
        slot_end_time = slot_start_time + 10 * 60 * 1000

        # Find all entries within the 10-minute slot
        current_slot = [m for m in mood_metrics[i:] if m['timestamp'] <= slot_end_time]

        # Check if the slot contains 1 or 2 entries
        if len(current_slot) <= 2:
            misclicked_metrics.extend(current_slot)
        else:
            filtered_mood_metrics.extend(current_slot)

        # Move index past the current slot
        i += len(current_slot)

    if misclicked_metrics:
        print("filtered:", file=sys.stderr)
        for metric in misclicked_metrics:
            print(json.dumps(metric), file=sys.stderr)

    data['metrics'] = sorted(other_metrics + filtered_mood_metrics, key=lambda x: x['timestamp'])
    return data

def main():
    """Main function to parse arguments and run the filter."""
    parser = argparse.ArgumentParser(
        description="Filter misclicked mood entries from a WellTrack JSON export.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "filename",
        type=str,
        help="Path to the WellTrack JSON export file.",
    )
    args = parser.parse_args()

    try:
        with open(args.filename, 'r', encoding='utf-8') as f:
            welltrack_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {args.filename}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {args.filename}", file=sys.stderr)
        sys.exit(1)

    filtered_data = filter_misclicks(welltrack_data)

    print(json.dumps(filtered_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()