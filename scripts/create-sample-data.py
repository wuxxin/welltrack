#!/usr/bin/env python
"""Random Event/Mood/Pain Data Generator for WellTrack

This script generates realistic, configurable sample data for the WellTrack app.
It reads mood and pain configurations directly from the 'welltrack.html' file
to ensure compatibility, while using a predefined set of event types.
"""

import argparse
import bisect
import json
import random
import re
import sys

from datetime import datetime, time, timedelta

# Predefined event configurations as per the new requirements
SAMPLE_EVENT_TYPES = [
    {"name": "Kaffee Tassen", "activity": "coffee_cups", "increment": 1, "unitType": "", "groupType": "Ernährung", "displayType": 1},
    {"name": "Rückenübungen", "activity": "back_exercises", "increment": 15, "unitType": "min", "groupType": "Bewegung", "displayType": 0},
    {"name": "Inline skaten", "activity": "inlineskating", "increment": 15, "unitType": "min", "groupType": "Bewegung", "displayType": 0},
    {"name": "Ring Übungen", "activity": "ring_training", "increment": 5, "unitType": "min", "groupType": "Bewegung", "displayType": 0},
    {"name": "Tanzen", "activity": "dancing", "increment": 15, "unitType": "min", "groupType": "Bewegung", "displayType": 0},
    {"name": "Ibuprofen 400mg", "activity": "ibuprofen_400", "increment": 0, "unitType": "", "groupType": "Medikamente", "displayType": 2},
    {"name": "Ascorbisal", "activity": "acetylsalicylacid_500", "increment": 0, "unitType": "", "groupType": "Medikamente", "displayType": 2},
    {"name": "Vitamin D3+K2", "activity": "vitamin_d3_k2", "increment": 0, "unitType": "", "groupType": "Medikamente", "displayType": 2},
    {"name": "Joe", "activity": "joe", "increment": 0, "unitType": "", "groupType": "😀", "displayType": 0},
    {"name": "William", "activity": "william", "increment": 0, "unitType": "", "groupType": "😀", "displayType": 0},
    {"name": "Jack", "activity": "jack", "increment": 0, "unitType": "", "groupType": "😀", "displayType": 0},
    {"name": "Averell", "activity": "averell", "increment": 0, "unitType": "", "groupType": "😀", "displayType": 0},
    {"name": "Ein Hobby", "activity": "hobby_1", "increment": 0, "unitType": "min", "groupType": "Hobby", "displayType": 0},
    {"name": "Zwei Hobby", "activity": "hobby_2", "increment": 0, "unitType": "min", "groupType": "Hobby", "displayType": 0},
    {"name": "Drei Hobby", "activity": "hobby_3", "increment": 0, "unitType": "min", "groupType": "Hobby", "displayType": 0},
    {"name": "One Hobby", "activity": "hobby_4", "increment": 0, "unitType": "min", "groupType": "Hobby", "displayType": 0},
    {"name": "Eine Hausarbeit", "activity": "hausarbeit_1", "increment": 0, "unitType": "min", "groupType": "Hausarbeit", "displayType": 0},
    {"name": "Zwei Hausarbeit", "activity": "hausarbeit_2", "increment": 0, "unitType": "min", "groupType": "Hausarbeit", "displayType": 0},
    {"name": "Drei Hausarbeit", "activity": "hausarbeit_3", "increment": 0, "unitType": "min", "groupType": "Hausarbeit", "displayType": 0},
    {"name": "Vier Hausarbeit", "activity": "hausarbeit_4", "increment": 0, "unitType": "min", "groupType": "Hausarbeit", "displayType": 0},
    {"name": "Fünf Hausarbeit", "activity": "hausarbeit_5", "increment": 0, "unitType": "min", "groupType": "Hausarbeit", "displayType": 0}
]  # fmt: skip


def extract_config_from_html(html_content):
    """Extracts MOOD_GROUPS and BODY_PARTS from the HTML script."""
    config = {}

    # 1. Extract MOOD_GROUPS
    mood_match = re.search(r"MOOD_GROUPS:\s*(\{.*?\s*\}\s*\})", html_content, re.DOTALL)
    if mood_match:
        mood_str = mood_match.group(1)
        mood_str = re.sub(r",\s*(\}|\])", r"\1", mood_str)
        mood_str = re.sub(r"(\w+)\s*:", r'"\1":', mood_str)
        mood_str = mood_str.replace("'", '"')
        try:
            config["MOOD_GROUPS"] = json.loads(mood_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing MOOD_GROUPS: {e}", file=sys.stderr)
            config["MOOD_GROUPS"] = {}

    # 2. Extract Body Parts from SVG
    body_parts = []
    part_matches = re.findall(
        r'<(?:rect|circle).*?id="([^"]+)".*?data-name="([^"]+)"', html_content
    )
    for part_id, part_name in part_matches:
        body_parts.append({"id": part_id, "name": part_name})

    seen = set()
    unique_body_parts = []
    for part in body_parts:
        if part["id"] not in seen:
            unique_body_parts.append(part)
            seen.add(part["id"])
    config["BODY_PARTS"] = unique_body_parts

    return config


def get_event_labels(event_config):
    """Extracts the correct label properties from an event configuration object."""
    return {
        "name": event_config.get("name", ""),
        "activity": event_config.get("activity", ""),
        "unitType": event_config.get("unitType", ""),
        "groupType": event_config.get("groupType", ""),
    }


def get_random_timestamp_in_slot(base_date, start_hour, end_hour):
    """Generates a random millisecond timestamp within a given time slot for a base date."""
    slot_date = base_date if start_hour >= 5 else base_date + timedelta(days=1)
    start_time = slot_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)

    # Handle overnight slots like (21, 0) which means 21:00 to 23:59:59
    if end_hour == 0:
        end_time = slot_date.replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        end_time = slot_date.replace(
            hour=end_hour, minute=0, second=0, microsecond=0
        ) - timedelta(microseconds=1)

    start_ts = int(start_time.timestamp())
    end_ts = int(end_time.timestamp())
    random_ts = random.randint(start_ts, end_ts)
    return random_ts * 1000


def get_random_timestamp_for_day(base_date):
    """Generates a random millisecond timestamp within a WellTrack day (5 AM to 4:59 AM)."""
    day_start = base_date.replace(hour=5, minute=0, second=0, microsecond=0)
    day_end = (base_date + timedelta(days=1)).replace(
        hour=4, minute=59, second=59, microsecond=999999
    )

    start_ts = int(day_start.timestamp())
    end_ts = int(day_end.timestamp())
    random_ts = random.randint(start_ts, end_ts)
    return random_ts * 1000


def generate_random_data(config, days_to_generate, settings={}):
    """Generates random health metrics based on the provided config."""
    metrics = []
    now = datetime.now()
    # We generate data for days_to_generate up to today
    today_start = now.replace(hour=5, minute=0, second=0, microsecond=0)

    all_mood_questions = [
        q
        for group in config.get("MOOD_GROUPS", {}).values()
        for q in group.get("questions", [])
    ]
    all_body_parts = config.get("BODY_PARTS", [])
    events_map = {e["activity"]: e for e in SAMPLE_EVENT_TYPES}

    if not all_mood_questions or not all_body_parts or not events_map:
        print(
            "Error: Configuration missing. Could not find mood, body part, or event data.",
            file=sys.stderr,
        )
        return None

    # Pick 4-6 recurring pain body parts from a random starting point
    start_index = random.randint(0, len(all_body_parts) - 6)
    num_recurring_parts = random.randint(4, 6)
    recurring_pain_parts = all_body_parts[start_index : start_index + num_recurring_parts]

    # Time slots for entries: (start_hour, end_hour)
    time_slots = [(5, 11), (11, 14), (14, 16), (16, 18), (18, 21), (21, 0), (0, 2), (2, 4)]

    for i in range(days_to_generate, -1, -1):
        current_day_base = today_start - timedelta(days=i)
        day_of_week = current_day_base.weekday()  # Monday is 0, Sunday is 6

        # Rule: 1 out of 20 days has no entries at all, except last two entries, which will always have entries
        if (i > 1) and random.random() < (1 / 20):
            continue

        # --- Generate Mood and Pain Data ---
        # last two days have 4 entries, the last day may have lesser because metric recording of future will break app.
        num_slots_today = random.randint(2, 8) if (i > 2) else 4
        # Sort slots by start hour to simulate chronological order (handle overnight)
        slots_for_today = sorted(
            random.sample(time_slots, num_slots_today), key=lambda x: (x[0] < 5, x[0])
        )

        for slot_num, (start_hour, end_hour) in enumerate(slots_for_today):
            ts = get_random_timestamp_in_slot(current_day_base, start_hour, end_hour)
            day_progress = (slot_num + 1) / len(slots_for_today)

            # Mood
            num_mood_questions_to_answer = len(all_mood_questions)
            questions_for_slot = random.sample(
                all_mood_questions, num_mood_questions_to_answer
            )
            for question in questions_for_slot:
                mood_weights = [0.30, 0.30, 0.15, 0.15, 0.05, 0.05]
                mood_values = [-1, 1, -2, 2, -3, 3]
                if random.random() < (0.2 * day_progress):
                    mood_weights = [0.45, 0.15, 0.225, 0.075, 0.075, 0.025]
                value = random.choices(mood_values, weights=mood_weights, k=1)[0]
                metrics.append(
                    {
                        "metric": f"mood_{question['id']}_level",
                        "timestamp": ts + random.randint(-30000, 30000),
                        "labels": {"mood_id": question["id"], "name": question["name"]},
                        "value": value,
                    }
                )

            # Pain
            if random.random() < (1 / 20):
                metrics.append(
                    {
                        "metric": "pain_free_level",
                        "timestamp": ts + random.randint(-30000, 30000),
                        "labels": {"name": "Schmerz Frei"},
                        "value": 0,
                    }
                )
            else:
                num_pain_parts = random.randint(3, 5)
                parts_for_slot = random.sample(
                    recurring_pain_parts, min(num_pain_parts, len(recurring_pain_parts))
                )
                pain_level_weights = [0.7, 0.25, 0.05]
                if random.random() < (0.2 * day_progress):
                    pain_level_weights = [0.55, 0.35, 0.10]
                for part in parts_for_slot:
                    level = random.choices([1, 2, 3], weights=pain_level_weights, k=1)[0]
                    metrics.append(
                        {
                            "metric": f"pain_{part['id']}_level",
                            "timestamp": ts + random.randint(-30000, 30000),
                            "labels": {"body_part": part["id"], "name": part["name"]},
                            "value": level,
                        }
                    )
                    if level == 3:
                        ibu_cfg = events_map["ibuprofen_400"]
                        metrics.append(
                            {
                                "metric": f"event_{ibu_cfg['activity']}_timestamp",
                                "timestamp": ts + random.randint(0, 5000),
                                "labels": get_event_labels(ibu_cfg),
                                "value": 1,
                            }
                        )

                if random.random() < (1 / 15):
                    available_random_parts = [
                        p for p in all_body_parts if p not in parts_for_slot
                    ]
                    if available_random_parts:
                        random_part = random.choice(available_random_parts)
                        level = random.choices([1, 2], weights=[0.8, 0.2], k=1)[0]
                        metrics.append(
                            {
                                "metric": f"pain_{random_part['id']}_level",
                                "timestamp": ts + random.randint(-30000, 30000),
                                "labels": {
                                    "body_part": random_part["id"],
                                    "name": random_part["name"],
                                },
                                "value": level,
                            }
                        )

        # --- Generate Event Data ---
        # Coffee: 2-6 per day
        coffee_cfg = events_map["coffee_cups"]
        metrics.append(
            {
                "metric": f"event_{coffee_cfg['activity']}_value",
                "timestamp": get_random_timestamp_for_day(current_day_base),
                "labels": get_event_labels(coffee_cfg),
                "value": random.randint(2, 6),
            }
        )

        # Contacts: 3-7 per day
        daltons = ["joe", "william", "jack", "averell"]
        for _ in range(random.randint(3, 7)):
            contact_activity = random.choice(daltons)
            contact_cfg = events_map[contact_activity]
            metrics.append(
                {
                    "metric": f"event_{contact_cfg['activity']}_timestamp",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(contact_cfg),
                    "value": 1,
                }
            )

        # Inline Skating: 60 min, 5/7 days
        if random.random() < (5 / 7):
            skate_cfg = events_map["inlineskating"]
            metrics.append(
                {
                    "metric": f"event_{skate_cfg['activity']}_value",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(skate_cfg),
                    "value": 60,
                }
            )

        # Ring Training: 5 min, 2-3 times per week (avg 2.5/7)
        if random.random() < (2.5 / 7):
            ring_cfg = events_map["ring_training"]
            metrics.append(
                {
                    "metric": f"event_{ring_cfg['activity']}_value",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(ring_cfg),
                    "value": 5,
                }
            )

        # Dancing: 120min, 0-2 times per week on Th, Fr, Sa (avg 1/week -> 1/3 on those days)
        if day_of_week in [3, 4, 5] and random.random() < (1 / 3):
            dance_cfg = events_map["dancing"]
            metrics.append(
                {
                    "metric": f"event_{dance_cfg['activity']}_value",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(dance_cfg),
                    "value": 120,
                }
            )

        # Ascorbisal: 3 out of 14 days
        if random.random() < (3 / 14):
            ascor_cfg = events_map["acetylsalicylacid_500"]
            metrics.append(
                {
                    "metric": f"event_{ascor_cfg['activity']}_timestamp",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(ascor_cfg),
                    "value": 1,
                }
            )

        # Vitamin D3+K2: every 3rd day, 10% chance to forget
        day_number = days_to_generate - i
        if day_number % 3 == 0 and random.random() < 0.9:
            vit_cfg = events_map["vitamin_d3_k2"]
            metrics.append(
                {
                    "metric": f"event_{vit_cfg['activity']}_timestamp",
                    "timestamp": get_random_timestamp_for_day(current_day_base),
                    "labels": get_event_labels(vit_cfg),
                    "value": 1,
                }
            )

    metrics.sort(key=lambda x: x["timestamp"])

    last_valid_timestamp = int(datetime.now().timestamp()) * 1000
    last_valid_index = bisect.bisect_right(
        metrics, last_valid_timestamp, key=lambda x: x["timestamp"]
    )
    if last_valid_index > 0:
        final_metrics = metrics[:last_valid_index]
    else:
        final_metrics = metrics

    return {
        "metrics": final_metrics,
        "eventTypes": SAMPLE_EVENT_TYPES,
        "settings": settings,
    }


def main():
    """Main function to parse arguments and generate data."""
    parser = argparse.ArgumentParser(
        description="Random Event/Mood/Pain Data Generator for WellTrack.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--days",
        type=int,
        default=112,
        help="Number of days to generate data for (default: 112).",
    )
    parser.add_argument(
        "--setting",
        action="append",
        type=str,
        help="""Set a key-value pair in the settings object.
The value will be parsed as a boolean, integer, or string.
Example: --setting theme=dark --setting notifications=true --setting maxItems=50""",
    )
    parser.add_argument("output_file", type=str, help='Output filename or "-" for stdout.')
    args = parser.parse_args()

    settings_dict = {}
    if args.setting:
        for s in args.setting:
            if "=" not in s:
                print(
                    f"Warning: Ignoring invalid setting format: {s}. Expected key=value.",
                    file=sys.stderr,
                )
                continue
            key, value_str = s.split("=", 1)

            # Attempt to parse value as boolean, then integer, finally string
            if value_str.lower() == "true":
                value = True
            elif value_str.lower() == "false":
                value = False
            else:
                try:
                    value = int(value_str)
                except ValueError:
                    value = value_str
            settings_dict[key] = value

    try:
        with open("src/welltrack/welltrack.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(
            "Error: src/welltrack/welltrack.html not found. Make sure you are running from the project root.",
            file=sys.stderr,
        )
        sys.exit(1)

    app_config = extract_config_from_html(html_content)

    if not app_config.get("BODY_PARTS") or not app_config.get("MOOD_GROUPS"):
        print(
            "\nCould not extract required pain/mood configurations from welltrack.html.",
            file=sys.stderr,
        )
        sys.exit(1)

    export_data = generate_random_data(app_config, args.days, settings=settings_dict)

    output_json = json.dumps(export_data, ensure_ascii=False, indent=2)
    if args.output_file == "-":
        print(output_json)
    else:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Random data was successfully saved to '{args.output_file}'.", file=sys.stderr)


if __name__ == "__main__":
    main()
