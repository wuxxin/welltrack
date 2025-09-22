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
    """Generates 180 days of random health metrics."""
    metrics = []
    today = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    all_mood_questions = [q for group in MOOD_GROUPS.values() for q in group['questions']]
    event_config = {event['activity']: event for event in DEFAULT_EVENTS_JSON}

    for i in range(179, -1, -1):
        date = today - timedelta(days=i)
        day_of_week = date.weekday() # Monday is 0 and Sunday is 6

        def set_timestamp(hour, minute):
            return (date.replace(hour=hour, minute=minute, second=random.randint(0, 59))).isoformat()

        # --- EVENTS ---
        if 'walking' in event_config and random.random() < 0.9:
            event = event_config['walking']
            duration = round(min(90, ((random.random() + random.random()) / 2 * 1.3) * 90))
            if duration > 0:
                metrics.append({
                    'metric': f"event_{event['activity']}_value",
                    'timestamp': set_timestamp(18, 30),
                    'labels': get_event_labels(event),
                    'value': duration
                })

        if 'back_exercises' in event_config and day_of_week in [0, 1, 3, 4]:
            # Mon, Tue, Thu, Fri
            event = event_config['back_exercises']
            metrics.append({
                'metric': f"event_{event['activity']}_value",
                'timestamp': set_timestamp(8, 0),
                'labels': get_event_labels(event),
                'value': 15
            })

        if 'coffee_cups' in event_config:
            event = event_config['coffee_cups']
            for c in range(random.randint(2, 4)):
                metrics.append({
                    'metric': f"event_{event['activity']}_value",
                    'timestamp': set_timestamp(9 + c * 2, 15),
                    'labels': get_event_labels(event),
                    'value': 1
                })

        if 'ibuprofen_400' in event_config and random.random() < 5/7:
            event = event_config['ibuprofen_400']
            metrics.append({
                'metric': f"event_{event['activity']}_timestamp",
                'timestamp': set_timestamp(10, 0),
                'labels': get_event_labels(event),
                'value': 1
            })
            if day_of_week == 2: # Wednesday
                metrics.append({
                    'metric': f"event_{event['activity']}_timestamp",
                    'timestamp': set_timestamp(16, 0),
                    'labels': get_event_labels(event),
                    'value': 1
                })

        # --- MOOD ---
        mood_values = [random.choice([-1, 1]) for _ in range(8)] + [random.choice([-2, 2]) for _ in range(3)]
        if i % 14 == 0:
            mood_values.append(random.choice([-3, 3]))

        random.shuffle(all_mood_questions)
        for val, question in zip(mood_values, all_mood_questions):
            metrics.append({'metric': f"mood_{question['id']}_level", 'timestamp': set_timestamp(20, 0), 'labels': {'mood_id': question['id'], 'name': question['name']}, 'value': val})

        # --- PAIN ---
        pain_chance = random.random()
        random.shuffle(ALL_BODY_PARTS)
        if pain_chance < 0.25: # 3x Level 2
            for p in range(3):
                part = ALL_BODY_PARTS[p]
                metrics.append({'metric': f"pain_{part['id']}_level", 'timestamp': set_timestamp(14, 0), 'labels': {'body_part': part['id'], 'name': part['name']}, 'value': 2})
        elif pain_chance < 0.5: # 1x Level 1
            part = ALL_BODY_PARTS[0]
            metrics.append({'metric': f"pain_{part['id']}_level", 'timestamp': set_timestamp(14, 0), 'labels': {'body_part': part['id'], 'name': part['name']}, 'value': 1})
        elif pain_chance < 1: # 2x Level 1
            for p in range(2):
                part = ALL_BODY_PARTS[p]
                metrics.append({'metric': f"pain_{part['id']}_level", 'timestamp': set_timestamp(14, 0), 'labels': {'body_part': part['id'], 'name': part['name']}, 'value': 1})

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
    file_name = f"welltrack_export_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"Random data was successfully saved to '{file_name}'.")

