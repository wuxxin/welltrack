#!/usr/bin/env python
"""Random Event/Mood/Pain Data Generator for WellTrack

This script reads data definitions directly from the 'welltrack.html' file
to ensure the generated sample data is always in sync with the application.
"""

import json
import random
import re
from datetime import datetime, timedelta

def extract_config_from_html(html_content):
    """Extracts MOOD_GROUPS, DEFAULT_EVENTS_JSON, and body parts from the HTML script."""
    config = {}

    # 1. Extract MOOD_GROUPS
    mood_match = re.search(r'MOOD_GROUPS:\s*(\{.*?\s*\}\s*\})', html_content, re.DOTALL)
    if mood_match:
        mood_str = mood_match.group(1)
        # Clean up for JSON parsing: remove trailing commas, use double quotes
        mood_str = re.sub(r",\s*(\}|\])", r"\1", mood_str)
        mood_str = re.sub(r"(\w+)\s*:", r'"\1":', mood_str)
        mood_str = mood_str.replace("'", '"')
        try:
            config['MOOD_GROUPS'] = json.loads(mood_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing MOOD_GROUPS: {e}")
            print(f"Content: {mood_str}")
            config['MOOD_GROUPS'] = {}

    # 2. Extract DEFAULT_EVENTS_JSON
    events_match = re.search(r'DEFAULT_EVENTS_JSON:\s*`(\[.*?\])`', html_content, re.DOTALL)
    if events_match:
        events_str = events_match.group(1)
        try:
            config['DEFAULT_EVENTS_JSON'] = json.loads(events_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing DEFAULT_EVENTS_JSON: {e}")
            print(f"Content: {events_str}")
            config['DEFAULT_EVENTS_JSON'] = []

    # 3. Extract Body Parts from SVG
    body_parts = []
    # Regex to find any SVG element with id and data-name attributes
    part_matches = re.findall(r'<(?:rect|circle).*?id="([^"]+)".*?data-name="([^"]+)"', html_content)
    for part_id, part_name in part_matches:
        body_parts.append({'id': part_id, 'name': part_name})

    # Remove duplicates
    seen = set()
    unique_body_parts = []
    for part in body_parts:
        if part['id'] not in seen:
            unique_body_parts.append(part)
            seen.add(part['id'])

    config['ALL_BODY_PARTS'] = unique_body_parts

    return config

def get_event_labels(event_config):
    """Extracts the correct label properties from an event configuration object."""
    return {
        "name": event_config.get("name", ""),
        "activity": event_config.get("activity", ""),
        "unitType": event_config.get("unitType", ""),
        "groupType": event_config.get("groupType", "")
    }

def generate_random_data(config):
    """Generates 180 days of random health metrics based on the provided config."""
    metrics = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    all_mood_questions = [q for group in config.get('MOOD_GROUPS', {}).values() for q in group.get('questions', [])]
    all_body_parts = config.get('ALL_BODY_PARTS', [])
    default_events = config.get('DEFAULT_EVENTS_JSON', [])

    if not all_mood_questions or not all_body_parts or not default_events:
        print("Error: Configuration missing from HTML. Could not find mood, body, or event data.")
        return None

    for i in range(179, -1, -1):
        # --- Day Skipping Logic ---
        day_roll = random.random()
        if day_roll < 0.03:
            continue # 3% chance of a missing day

        date = today - timedelta(days=i)

        def get_random_timestamp(start_hour, end_hour, end_minute=59):
            hour = random.randint(start_hour, end_hour)
            minute = random.randint(0, end_minute)
            second = random.randint(0, 59)
            if hour == end_hour:
                minute = random.randint(0, end_minute)
            dt_obj = date.replace(hour=hour, minute=minute, second=second)
            return int(dt_obj.timestamp() * 1000)

        # --- Entry Block Logic ---
        num_entries_roll = random.random()
        num_entry_blocks = 3
        if num_entries_roll < 0.05: num_entry_blocks = 1
        elif num_entries_roll < 0.15: num_entry_blocks = 2

        time_windows = [(9, 11), (17, 18), (23, 23, 50)]
        selected_windows = random.sample(time_windows, num_entry_blocks)

        for window in selected_windows:
            ts = get_random_timestamp(*window)

            # --- Generate Mood Data ---
            if all_mood_questions:
                num_mood_entries = random.randint(3, len(all_mood_questions))
                mood_values = [random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(num_mood_entries)]
                random.shuffle(all_mood_questions)
                for val, question in zip(mood_values, all_mood_questions[:num_mood_entries]):
                    metrics.append({
                        'metric': f"mood_{question['id']}_level",
                        'timestamp': ts + random.randint(-60000, 60000),
                        'labels': {'mood_id': question['id'], 'name': question['name']},
                        'value': val
                    })

            # --- Generate Pain Data ---
            if all_body_parts and random.random() < 0.6:
                num_pain_entries = random.randint(1, 4)
                random.shuffle(all_body_parts)
                for p in range(num_pain_entries):
                    part = all_body_parts[p]
                    metrics.append({
                        'metric': f"pain_{part['id']}_level",
                        'timestamp': ts + random.randint(-60000, 60000),
                        'labels': {'body_part': part['id'], 'name': part['name']},
                        'value': random.randint(1, 5)
                    })

            # --- Generate Event Data ---
            if default_events and random.random() < 0.5:
                event_config = random.choice(default_events)
                if event_config['increment'] > 0:
                     metrics.append({
                        'metric': f"event_{event_config['activity']}_value",
                        'timestamp': ts + random.randint(-60000, 60000),
                        'labels': get_event_labels(event_config),
                        'value': event_config['increment'] * random.randint(1, 3)
                    })
                else:
                    metrics.append({
                        'metric': f"event_{event_config['activity']}_timestamp",
                        'timestamp': ts + random.randint(-60000, 60000),
                        'labels': get_event_labels(event_config),
                        'value': 1
                    })

    metrics.sort(key=lambda x: x['timestamp'])

    return {
        "metrics": metrics,
        "events": default_events,
        "settings": {
            "reminderTime": "20:00",
            "committedIndex": len(metrics) - 1
        }
    }

if __name__ == "__main__":
    try:
        with open("welltrack.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: welltrack.html not found. Make sure the script is in the same directory.")
        exit(1)

    app_config = extract_config_from_html(html_content)

    if not app_config.get('ALL_BODY_PARTS') or not app_config.get('MOOD_GROUPS') or not app_config.get('DEFAULT_EVENTS_JSON'):
         print("\nCould not extract all required configurations from welltrack.html. Aborting.")
         exit(1)

    export_data = generate_random_data(app_config)

    if export_data:
        file_name = f"welltrack_export_{int(datetime.now().timestamp() * 1000)}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"Random data was successfully saved to '{file_name}'.")
