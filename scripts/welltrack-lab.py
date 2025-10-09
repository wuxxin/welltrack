import marimo
import pandas as pd
import json
import altair as alt
from welltrack_lab.data import (
    load_data,
    process_metrics,
    create_timeslot_sums,
    calculate_distribution,
    get_daily_summary,
    prepare_correlation_data,
)

__generated_with = "0.1.0"
app = marimo.App(width="full")

@app.cell
def __(mo):
    mo.md("# WellTrack Lab")
    file_uploader = mo.ui.file(filetypes=[".json"], kind="json")
    return file_uploader,

@app.cell
def __(file_uploader, load_data):
    if file_uploader.value:
        raw_metrics_df, raw_event_types_df, raw_settings_df = load_data(
            file_uploader.value
        )
    return raw_event_types_df, raw_metrics_df, raw_settings_df

@app.cell
def __(mo, process_metrics, raw_metrics_df, raw_settings_df):
    if raw_metrics_df is not None:
        processed_df = process_metrics(raw_metrics_df, raw_settings_df)
        mo.md(f"Geladene Metriken: **{len(processed_df)}**")
    return processed_df,

@app.cell
def __(create_timeslot_sums, processed_df):
    if processed_df is not None:
        pain_slots = create_timeslot_sums(processed_df, "pain")
        mood_slots = create_timeslot_sums(processed_df, "mood")
    return mood_slots, pain_slots

@app.cell
def __(
    alt,
    calculate_distribution,
    get_daily_summary,
    mo,
    mood_slots,
    pain_slots,
    prepare_correlation_data,
    processed_df,
):
    if processed_df is not None:
        # --- 1. Distributions ---
        pain_df = processed_df[processed_df["metric_type"] == "pain"]
        mood_df = processed_df[processed_df["metric_type"] == "mood"]
        event_df = processed_df[processed_df["metric_type"] == "event"]

        pain_dist = calculate_distribution(pain_df, "value", "label.name")
        mood_dist = calculate_distribution(mood_df, "value", "label.name")
        event_dist = calculate_distribution(
            event_df[event_df["label.groupType"].notna()], "value", "label.groupType"
        )

        pain_dist_chart = (
            alt.Chart(pain_dist)
            .mark_bar()
            .encode(
                x=alt.X("percentage:Q", title="Prozent"),
                y=alt.Y("label.name:N", title="Schmerzort", sort="-x"),
            )
            .properties(title="Verteilung der Schmerz-Gesamtwerte")
        )

        mood_dist_chart = (
            alt.Chart(mood_dist)
            .mark_bar()
            .encode(
                x=alt.X("percentage:Q", title="Prozent"),
                y=alt.Y("label.name:N", title="Stimmung", sort="-x"),
            )
            .properties(title="Verteilung der Stimmungs-Gesamtwerte")
        )

        event_dist_chart = (
            alt.Chart(event_dist)
            .mark_bar()
            .encode(
                x=alt.X("percentage:Q", title="Prozent"),
                y=alt.Y("label.groupType:N", title="Ereignisgruppe", sort="-x"),
            )
            .properties(title="Verteilung der Ereignis-Gesamtwerte (nach Gruppe)")
        )

        # --- 2. Daily Summaries ---
        daily_pain_summary = get_daily_summary(processed_df, "pain")
        daily_mood_summary = get_daily_summary(processed_df, "mood")

        daily_pain_chart = (
            alt.Chart(daily_pain_summary)
            .mark_line(point=True)
            .encode(
                x=alt.X("wt_day:T", title="Tag"),
                y=alt.Y("total:Q", title="Gesamtschmerz"),
                tooltip=["wt_day:T", "total:Q"],
            )
            .properties(title="Täglicher Gesamtschmerz über Zeit")
        )

        daily_mood_chart = (
            alt.Chart(daily_mood_summary)
            .mark_line(point=True)
            .encode(
                x=alt.X("wt_day:T", title="Tag"),
                y=alt.Y("total:Q", title="Gesamtstimmung"),
                tooltip=["wt_day:T", "total:Q"],
            )
            .properties(title="Tägliche Gesamtstimmung über Zeit")
        )

        # --- 3. Mood Correlation ---
        correlation_data = prepare_correlation_data(processed_df)
        if not correlation_data.empty and correlation_data.shape[1] > 1:
            mood_correlation_matrix = correlation_data.corr()
            corr_data_long = mood_correlation_matrix.reset_index().melt("index")
            corr_data_long.columns = ["mood1", "mood2", "correlation"]
            heatmap = (
                alt.Chart(corr_data_long)
                .mark_rect()
                .encode(
                    x=alt.X("mood1:N", title="Stimmung 1", sort=None),
                    y=alt.Y("mood2:N", title="Stimmung 2", sort=None),
                    color=alt.Color(
                        "correlation:Q",
                        scale=alt.Scale(scheme="redblue", domain=(-1, 1)),
                    ),
                )
                .properties(title="Stimmung Korrelations-Heatmap")
            )
            text = heatmap.mark_text(fontSize=10).encode(
                text=alt.Text("correlation:Q", format=".2f"),
                color=alt.condition(
                    abs(alt.datum.correlation) > 0.5,
                    alt.value("white"),
                    alt.value("black"),
                ),
            )
            correlation_chart = heatmap + text
        else:
            correlation_chart = mo.md("Nicht genügend Daten für Korrelationsanalyse.")

        # --- UI Tabs ---
        analysis_tabs = mo.tabs(
            {
                "Verteilungen": mo.tabs(
                    {
                        "Schmerz": pain_dist_chart,
                        "Stimmung": mood_dist_chart,
                        "Ereignisse": event_dist_chart,
                    }
                ),
                "Tages-Zusammenfassungen": mo.tabs(
                    {"Schmerz": daily_pain_chart, "Stimmung": daily_mood_chart}
                ),
                "Stimmungs-Korrelation": correlation_chart,
                "Timeslot-Daten": mo.tabs(
                    {
                        "Schmerz": mo.ui.table(pain_slots),
                        "Stimmung": mo.ui.table(mood_slots),
                    }
                ),
            }
        )
    return analysis_tabs,


@app.cell
def __(
    file_uploader,
    json,
    mo,
    pd,
    raw_event_types_df,
    raw_metrics_df,
    raw_settings_df,
):
    if file_uploader.value:
        if raw_metrics_df is not None:
            metrics_editor = mo.ui.data_editor(raw_metrics_df)
            event_types_editor = mo.ui.data_editor(raw_event_types_df)
            settings_editor = mo.ui.data_editor(raw_settings_df)

            @mo.ui.button(label="Daten herunterladen")
            def download_data():
                edited_metrics_df = metrics_editor.value
                edited_event_types_df = event_types_editor.value
                edited_settings_df = settings_editor.value
                export_data = {
                    "metrics": json.loads(
                        edited_metrics_df.to_json(orient="records", date_format="iso")
                    ),
                    "eventTypes": json.loads(
                        edited_event_types_df.to_json(
                            orient="records", date_format="iso"
                        )
                    ),
                    "settings": json.loads(
                        edited_settings_df.to_json(orient="records", date_format="iso")
                    )[0],
                }
                mo.download(
                    data=json.dumps(export_data, indent=2),
                    filename="welltrack_export_edited.json",
                )

            data_editing_tabs = mo.tabs(
                {
                    "Metrics": metrics_editor,
                    "Event Types": event_types_editor,
                    "Settings": settings_editor,
                }
            )
            main_content = mo.vstack([data_editing_tabs, download_data])
        else:
            main_content = mo.md(
                "### Ungültige JSON-Datei. Bitte eine gültige `welltrack_export.json`-Datei hochladen."
            )
    else:
        main_content = mo.md(
            "### Bitte eine `welltrack_export.json`-Datei hochladen, um zu beginnen."
        )
    return main_content,

@app.cell
def __(analysis_tabs, main_content, mo, raw_metrics_df):
    if raw_metrics_df is not None:
        main_tabs = mo.tabs(
            {"Daten bearbeiten": main_content, "Analyse": analysis_tabs}
        )
        main_tabs
    else:
        main_content
    return main_tabs,


if __name__ == "__main__":
    app.run()