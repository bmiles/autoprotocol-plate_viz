import numpy as np
import random
import pandas as pd
import re
import string
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.io import output_notebook
from bokeh.models import HoverTool

def returnFactors(plate):
    factors = {}
    # plate_type = re.sub(r'\D+', '', plate.container_type.name)
    # if plate_type == "96":
    #     factors["x"] = [str(i) for i in range(1,13)]
    #     factors["y"] = list(reversed(string.ascii_uppercase[:8]))
    #     return factors
    # elif plate_type == "384":
    #     factors["x"] = [str(i) for i in range(1,25)]
    #     factors["y"] = list(reversed(string.ascii_uppercase[:16]))
    #     return factors
    # elif plate_type == "6":
    #     factors["x"] = [str(i) for i in range(1,4)]
    #     factors["y"] = list(reversed(string.ascii_uppercase[:2]))
    #     return factors
    factors["x"] = [str(i) for i in range(1,plate.container_type.col_count+1)]
    factors["y"] = list(reversed(string.ascii_uppercase[:len(plate.all_wells())/plate.container_type.col_count]))
    return factors

def plate_map(container):
    indices = list()
    volumes = list()
    row = list()
    column = list()
    for well in container.all_wells():
        indices.append(well.index)
        if well.volume == None:
            volumes.append(0)
        else:
            volumes.append(well.volume.to("microliter").magnitude)
        row.append(re.sub(r'\d+', '', well.humanize()))
        column.append(re.sub(r'\D+', '', well.humanize()))
    df = pd.DataFrame([indices, volumes, row, column])
    df = df.transpose()
    df.columns = ["index", "volume", "row","column"]
    factors = returnFactors(container)
    fig = figure(title="Plate Map of " + container.name, tools="resize, hover, save",
        x_range=factors["x"], y_range=factors["y"],plot_width=900, plot_height=600)

    fig.circle(source = ColumnDataSource(data=df), x=df["column"], y=df["row"],  color = "black", alpha=0.2, size=(df["volume"]/(container.container_type.well_volume_ul.magnitude)) * 0.8*(900/len(factors["x"])))
    hover = fig.select(dict(type=HoverTool))
    fig.select_one(HoverTool).tooltips = [
        ("Index", "$index"),
        ("Volume", "@volume" + " uL"),
    ]
    show(fig)
