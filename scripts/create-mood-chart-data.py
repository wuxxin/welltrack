import json
import random
from datetime import datetime, timedelta

def create_mood_chart_data():
    """
    Generates rich sample data for the mood chart, spanning 3 months.
    """
    # Dummy WellTrackApp config for standalone execution
    class MockWellTrackApp:
        config = {
            "MOOD_GROUPS": {
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
                        { 'id': 'outlook', 'name': 'Ausblick / Hoffnung' },
                        { 'id': 'self_esteem', 'name': 'Selbstwert' },
                        { 'id': 'stability', 'name': 'Stabilität' },
                        { 'id': 'social_connection', 'name': 'Soziale Verbindung' }
                    ]
                }
            },
            "MOOD_VALUE_MAP": [-3, -2, -1, 1, 2, 3]
        }

    # Generate the data
    mood_metrics = []
    now = datetime.now()
    for day_offset in range(90):
        current_date = now - timedelta(days=day_offset)
        # Simulate 2-5 mood entries per day
        for _ in range(random.randint(2, 5)):
            entry_time = current_date.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            # Create a full mood entry slot (all mood types)
            for group_key, group_value in MockWellTrackApp.config["MOOD_GROUPS"].items():
                for question in group_value['questions']:
                    mood_value = random.choice(MockWellTrackApp.config["MOOD_VALUE_MAP"])
                    mood_metrics.append({
                        "metric": f"mood_{question['id']}_level",
                        "timestamp": int(entry_time.timestamp() * 1000),
                        "labels": {"mood_id": question['id'], "name": question['name']},
                        "value": mood_value
                    })

    # Create a dummy export structure
    export_data = {
        "metrics": mood_metrics,
        "eventTypes": [],
        "settings": {}
    }

    # Write to file
    with open("build/tests/mood-chart-data.json", "w") as f:
        json.dump(export_data, f, indent=2)

    print("Successfully created build/tests/mood-chart-data.json")

if __name__ == "__main__":
    import os
    os.makedirs("build/tests", exist_ok=True)
    create_mood_chart_data()