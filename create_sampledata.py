#!/usr/bin/env python
"""Random Event/Mood/Pain Data Generator for WellTrack

"""

import json
import random
from datetime import datetime, timedelta

DEFAULT_EVENTS_JSON = [
    {"name": "Spaziergang", "activity": "walking", "days": [], "increment": 15, "unitType": "min", "groupType": "Bewegung"},
    {"name": "Kaffee Tassen", "activity": "coffee_cups", "days": [], "increment": 1, "unitType": "", "groupType": "Ernährung"},
    {"name": "Ibuprofen 400mg", "activity": "ibuprofen_400", "days": [], "increment": 0, "unitType": "Einnahme", "groupType": "Medikamente"},
    {"name": "Rückenübungen", "activity": "back_exercises", "days": [1, 2, 3, 4, 5], "increment": 15, "unitType": "min", "groupType": "Bewegung"}
]

MOOD_GROUPS = {
    'arousal_level': {
        'name': 'Energie & Motivation',
        'questions': [
            { 'id': 'energy', 'name': 'Energie' },
            { 'id': 'motivation', 'name': 'Motivation' },
            { 'id': 'inner_drive', 'name': 'Innere Unruhe' },
            { 'id': 'temperament', 'name': 'Temperament' },
            { 'id': 'anxiety', 'name': 'Angstfreiheit' },
            { 'id': 'focus', 'name': 'Fokus' }
        ]
    },
    'affective_state': {
        'name': 'Stimmung & Selbstwert',
        'questions': [
            { 'id': 'happiness', 'name': 'Glücklichkeit' },
            { 'id': 'outlook', 'name': 'Ausblick/Hoffnung' },
            { 'id': 'self_esteem', 'name': 'Selbstwert' },
            { 'id': 'stability', 'name': 'Stabilität' },
            { 'id': 'social_connection', 'name': 'Soziale Verbindung' }
        ]
    }
}

ALL_BODY_PARTS = [
    {'id': 'head_front', 'name': 'Kopf'}, {'id': 'torso_chest_left', 'name': 'Brust (L)'}, {'id': 'torso_chest_right', 'name': 'Brust (R)'},
    {'id': 'torso_abdomen_left', 'name': 'Bauch (L)'}, {'id': 'torso_abdomen_right', 'name': 'Bauch (R)'}, {'id': 'arm_left_front', 'name': 'Linker Arm'},
    {'id': 'hand_left_front', 'name': 'Hand (L)'}, {'id': 'arm_right_front', 'name': 'Rechter Arm'}, {'id': 'hand_right_front', 'name': 'Hand (R)'},
    {'id': 'leg_left_front', 'name': 'Linkes Bein'}, {'id': 'foot_left_front', 'name': 'Fuß (L)'}, {'id': 'leg_right_front', 'name': 'Rechtes Bein'},
    {'id': 'foot_right_front', 'name': 'Fuß (R)'}, {'id': 'head_back', 'name': 'Hinterkopf'}, {'id': 'back_cervical_left', 'name': 'HWS (L)'},
    {'id': 'back_cervical_right', 'name': 'HWS (R)'}, {'id': 'back_thoracic_left', 'name': 'BWS (L)'}, {'id': 'back_thoracic_right', 'name': 'BWS (R)'},
    {'id': 'back_lumbar_left', 'name': 'LWS (L)'}, {'id': 'back_lumbar_right', 'name': 'LWS (R)'}, {'id': 'arm_left_back', 'name': 'Linker Arm (h)'},
    {'id': 'hand_left_back', 'name': 'Hand (L,h)'}, {'id': 'arm_right_back', 'name': 'Rechter Arm (h)'}, {'id': 'hand_right_back', 'name': 'Hand (R,h)'},
    {'id': 'glute_left_back', 'name': 'Gesäß (L)'}, {'id': 'glute_right_back', 'name': 'Gesäß (R)'}, {'id': 'leg_left_back', 'name': 'Linkes Bein (h)'},
    {'id': 'foot_left_back', 'name': 'Fuß (L,h)'}, {'id': 'leg_right_back', 'name': 'Rechtes Bein (h)'}, {'id': 'foot_right_back', 'name': 'Fuß (R,h)'}
]

def get_event_labels(event_config):
    """Extracts the correct label properties from an event configuration object."""
    return {
        "name": event_config.get("name", ""),
        "activity": event_config.get("activity", ""),
        "unitType": event_config.get("unitType", ""),
        "groupType": event_config.get("groupType", "")
    }

def generate_random_data():
    """Generates 180 days of random health metrics based on time windows and probabilities."""
    metrics = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    all_mood_questions = [q for group in MOOD_GROUPS.values() for q in group['questions']]

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
            # Ensure end_hour and end_minute are respected
            if hour == end_hour:
                minute = random.randint(0, end_minute)

            dt_obj = date.replace(hour=hour, minute=minute, second=second)
            return int(dt_obj.timestamp())

        # --- Entry Block Logic ---
        num_entries_roll = random.random()
        num_entry_blocks = 3
        if num_entries_roll < 0.05: # 5% chance
            num_entry_blocks = 1
        elif num_entries_roll < 0.15: # 10% chance
            num_entry_blocks = 2

        time_windows = [
            (9, 11),  # 9:00 - 11:59
            (17, 18), # 17:00 - 18:59
            (23, 23, 50)  # 23:00 - 23:50
        ]

        selected_windows = random.sample(time_windows, num_entry_blocks)

        for window in selected_windows:
            ts = get_random_timestamp(*window)

            # --- Generate Mood Data ---
            num_mood_entries = random.randint(3, len(all_mood_questions))
            mood_values = [random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(num_mood_entries)]
            random.shuffle(all_mood_questions)
            for val, question in zip(mood_values, all_mood_questions[:num_mood_entries]):
                metrics.append({
                    'metric': f"mood_{question['id']}_level",
                    'timestamp': ts + random.randint(-60, 60), # Add jitter
                    'labels': {'mood_id': question['id'], 'name': question['name']},
                    'value': val
                })

            # --- Generate Pain Data ---
            if random.random() < 0.6: # 60% chance of pain entry
                num_pain_entries = random.randint(1, 4)
                random.shuffle(ALL_BODY_PARTS)
                for p in range(num_pain_entries):
                    part = ALL_BODY_PARTS[p]
                    metrics.append({
                        'metric': f"pain_{part['id']}_level",
                        'timestamp': ts + random.randint(-60, 60), # Add jitter
                        'labels': {'body_part': part['id'], 'name': part['name']},
                        'value': random.randint(1, 5)
                    })

            # --- Generate Event Data (less frequent) ---
            if random.random() < 0.5: # 50% chance of an event entry
                event_config = random.choice(DEFAULT_EVENTS_JSON)
                if event_config['increment'] > 0: # Incrementing event
                     metrics.append({
                        'metric': f"event_{event_config['activity']}_value",
                        'timestamp': ts + random.randint(-60, 60),
                        'labels': get_event_labels(event_config),
                        'value': event_config['increment'] * random.randint(1, 3)
                    })
                else: # Timestamp event
                    metrics.append({
                        'metric': f"event_{event_config['activity']}_timestamp",
                        'timestamp': ts + random.randint(-60, 60),
                        'labels': get_event_labels(event_config),
                        'value': 1
                    })

    # Sort metrics by timestamp, as expected by the app
    metrics.sort(key=lambda x: x['timestamp'])

    return {
        "metrics": metrics,
        "events": DEFAULT_EVENTS_JSON,
        "settings": {
            "reminderTime": "20:00",
            # All generated data is "committed"
            "committedIndex": len(metrics) - 1
        }
    }

if __name__ == "__main__":
    export_data = generate_random_data()
    file_name = f"welltrack_export_{int(datetime.now().timestamp())}.json"

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"Random data was successfully saved to '{file_name}'.")

