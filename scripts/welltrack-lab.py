import marimo

__generated_with = "0.16.5"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import altair as alt
    import json
    import welltrack_lab.data as wtd
    return mo, wtd


@app.cell(hide_code=True)
def _(mo):
    file_uploader = mo.ui.file(filetypes=[".json"], kind="button")
    mo.vstack(
        [
            mo.md("## WellTrack Datenanalyse"),
            mo.hstack([mo.md("Import/Export Daten File auswählen"), file_uploader]),
        ],
        align="start",
    )
    return (file_uploader,)


@app.cell(hide_code=True)
def _(file_uploader, mo, wtd):
    main_tabs = mo.md("")
    if file_uploader.contents():
        raw_metrics_df, raw_event_types_df, raw_settings_df = wtd.load_from_json(
            file_uploader.contents()
        )
        processed_df = wtd.process_metrics(
            raw_metrics_df, raw_event_types_df, raw_settings_df
        )
        print(f"Geladene Metriken: **{len(processed_df)}**")
        df = processed_df

        # --- UI Tabs ---
        main_content = mo.vstack([mo.ui.data_explorer(df)])
        transform_content = mo.vstack([mo.ui.dataframe(df)])
        editor_content = mo.vstack([mo.ui.data_editor(df)])
        main_tabs = mo.ui.tabs(
            {
                "Bearbeiten": editor_content,
                "Analyse": main_content,
                "Transformation": transform_content,
            }
        )

    main_tabs
    return


if __name__ == "__main__":
    app.run()
