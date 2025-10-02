# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "0.16.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.resources import INLINE
    from bokeh.embed import components
    from vega_datasets import data
    return (
        ColumnDataSource,
        HoverTool,
        INLINE,
        components,
        data,
        figure,
        mo,
        plt,
    )


@app.cell
def _(data, mo):
    # Load a sample dataset (e.g., stocks)
    stocks = data.stocks()

    # Show a preview of the data
    mo.ui.data_explorer(stocks)
    return (stocks,)


@app.cell
def _(mo, stocks):
    # UI elements for interactive selection
    symbol_selector = mo.ui.dropdown(
        options=stocks["symbol"].unique().tolist(),
        value=stocks["symbol"].unique()[0],
        label="Stock Symbol",
    )
    plot_type_selector = mo.ui.radio(
        options=["Bokeh", "Matplotlib"], value="Bokeh", label="Plot Library"
    )
    mo.hstack([symbol_selector, plot_type_selector])
    return plot_type_selector, symbol_selector


@app.cell
def _(stocks, symbol_selector):
    # Filter data based on selected symbol
    selected_symbol = symbol_selector.value
    filtered_df = stocks[stocks["symbol"] == selected_symbol]
    filtered_df = filtered_df.sort_values("date")
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df
    return filtered_df, selected_symbol


@app.cell
def _(ColumnDataSource, HoverTool, figure, filtered_df, plt, selected_symbol):
    # Bokeh plot
    source = ColumnDataSource(filtered_df)
    p_bokeh = figure(
        title=f"{selected_symbol} Stock Price (Bokeh)",
        x_axis_type="datetime",
        width=700,
        height=350,
    )
    p_bokeh.line(
        "date",
        "price",
        source=source,
        line_width=2,
        color="navy",
        legend_label=selected_symbol,
    )
    p_bokeh.circle("date", "price", source=source, size=5, color="orange", alpha=0.6)
    p_bokeh.add_tools(
        HoverTool(
            tooltips=[("Date", "@date{%F}"), ("Price", "@price")],
            formatters={"@date": "datetime"},
        )
    )
    p_bokeh.xaxis.axis_label = "Date"
    p_bokeh.yaxis.axis_label = "Price"

    # Matplotlib plot
    plt.figure(figsize=(10, 5))
    plt.plot(
        filtered_df["date"],
        filtered_df["price"],
        marker="o",
        color="teal",
        label=selected_symbol,
    )
    plt.title(f"{selected_symbol} Stock Price (Matplotlib)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    matplotlib_ax = plt.gca()
    return matplotlib_ax, p_bokeh


@app.cell
def _(INLINE, components, matplotlib_ax, mo, p_bokeh, plot_type_selector):
    # Display the selected plot interactively
    if plot_type_selector.value == "Bokeh":
        from bokeh.io import output_notebook, show

        output_notebook(resources=INLINE)
        from bokeh.embed import json_item

        mo.Html(components(p_bokeh)[0])
    else:
        matplotlib_ax
    return


if __name__ == "__main__":
    app.run()
