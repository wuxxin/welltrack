import marimo

__generated_with = "0.16.5"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    """
    Imports the necessary libraries for the Marimo application.

    This cell imports marimo for UI components, altair for charting (though not used
    in the current version), json for data handling, and the custom welltrack_lab.data
    module for data processing functions.

    Returns:
        tuple: A tuple containing the imported modules (mo, wtd) for use in
               other cells.
    """
    import marimo as mo
    import altair as alt
    import json
    import welltrack_lab.data as wtd
    return mo, wtd


@app.cell(hide_code=True)
def _(mo):
    """
    Creates and displays the file uploader UI component.

    This cell sets up the main header for the application and provides a button
    for users to upload their WellTrack JSON export file.

    Args:
        mo: The Marimo library object.

    Returns:
        tuple: A tuple containing the file_uploader UI element.
    """
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
    """
    Processes the uploaded file and displays the main analysis interface.

    This cell is the core of the application's reactivity. It checks if a file
    has been uploaded. If so, it uses the `welltrack_lab.data` module to load
    and process the data into a pandas DataFrame. It then creates a tabbed
    interface for exploring, viewing, and editing the data.

    Args:
        file_uploader: The file uploader UI element from the previous cell.
        mo: The Marimo library object.
        wtd: The welltrack_lab.data module.
    """
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
