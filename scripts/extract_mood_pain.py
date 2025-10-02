#!/usr/bin/env python
"""
Extracts mood and pain entries from a WellTrack JSON export.

This script filters mood and pain data from a given WellTrack export file
based on a specified start date. It validates the entries against the
current application configuration found in 'welltrack.html'.

Usage:
    cat welltrack_export.json | python scripts/extract_mood_pain.py <dd.mm.yyyy|all>
"""

import json
import re
import sys
from datetime import datetime

def show_usage():
    """Prints the usage information to stderr."""
    print(
        "Usage: cat <export_file.json> | python extract_mood_pain.py <dd.mm.yyyy|all>",
        file=sys.stderr
    )
    sys.exit(1)

def extract_config_from_html(html_content):
    """Extracts MOOD_GROUPS and body parts from the HTML script."""
    config = {}

    # 1. Extract MOOD_GROUPS
    mood_match = re.search(r'MOOD_GROUPS:\s*(\{.*?\s*\}\s*\})', html_content, re.DOTALL)
    if mood_match:
        mood_str = mood_match.group(1)
        mood_str = re.sub(r",\s*(\}|\])", r"\1", mood_str)
        mood_str = re.sub(r"(\w+)\s*:", r'"\1":', mood_str)
        mood_str = mood_str.replace("'", '"')
        try:
            config['MOOD_GROUPS'] = json.loads(mood_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing MOOD_GROUPS: {e}\nContent: {mood_str}", file=sys.stderr)
            config['MOOD_GROUPS'] = {}

    # 2. Extract Body Parts from SVG
    body_parts = []
    part_matches = re.findall(r'<(?:rect|circle).*?id="([^"]+)".*?data-name="([^"]+)"', html_content)
    for part_id, part_name in part_matches:
        body_parts.append({'id': part_id, 'name': part_name})

    seen = set()
    unique_body_parts = []
    for part in body_parts:
        if part['id'] not in seen:
            unique_body_parts.append(part)
            seen.add(part['id'])
    config['ALL_BODY_PARTS'] = unique_body_parts

    return config

def main():
    """Main function to execute the script logic."""
    if len(sys.argv) != 2 or sys.stdin.isatty():
        show_usage()

    date_arg = sys.argv[1]
    start_timestamp = 0
    if date_arg.lower() != 'all':
        try:
            start_date = datetime.strptime(date_arg, "%d.%m.%Y").replace(hour=0, minute=0, second=0, microsecond=0)
            start_timestamp = int(start_date.timestamp() * 1000)
        except ValueError:
            print(f"Error: Invalid date format '{date_arg}'. Please use dd.mm.yyyy.", file=sys.stderr)
            sys.exit(1)

    try:
        with open("src/welltrack/welltrack.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: src/welltrack/welltrack.html not found. Make sure you run the script from the project root.", file=sys.stderr)
        sys.exit(1)

    app_config = extract_config_from_html(html_content)
    valid_mood_ids = {q['id'] for group in app_config.get('MOOD_GROUPS', {}).values() for q in group.get('questions', [])}
    valid_pain_ids = {p['id'] for p in app_config.get('ALL_BODY_PARTS', [])}

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON received from stdin.", file=sys.stderr)
        sys.exit(1)

    filtered_metrics = []
    for metric in input_data.get("metrics", []):
        if metric.get("timestamp", 0) < start_timestamp:
            continue

        metric_name = metric.get("metric", "")
        is_mood = metric_name.startswith("mood_")
        is_pain = metric_name.startswith("pain_")

        if not is_mood and not is_pain:
            continue

        is_valid = False
        if is_mood:
            mood_id = metric.get("labels", {}).get("mood_id")
            if mood_id in valid_mood_ids:
                is_valid = True
            else:
                print(f"Rejected mood entry with unknown id: {mood_id}", file=sys.stderr)

        if is_pain:
            body_part_id = metric.get("labels", {}).get("body_part")
            if body_part_id in valid_pain_ids:
                is_valid = True
            else:
                print(f"Rejected pain entry with unknown id: {body_part_id}", file=sys.stderr)

        if is_valid:
            filtered_metrics.append(metric)

    output_data = {
        "metrics": filtered_metrics,
        "events": input_data.get("events", []),
        "settings": input_data.get("settings", {})
    }

    print(json.dumps(output_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()