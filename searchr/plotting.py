# from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure

# import pandas as pd
# df = pd.read_csv('~/OneDrive - University of Exeter/Documents/Projects/Hackathon_2023/probe1_test.csv')


def age_scatter_mat(df, plot_sex, non_linear):
    # extract info
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    # plot
    plt.figure()
    if plot_sex:
        sns.lmplot(
            data=df,
            x="Age",
            y="Beta_percent",
            hue="Sex",
            scatter=True,
            lowess=non_linear,
        )
    else:
        sns.lmplot(
            data=df,
            x="Age",
            y="Beta_percent",
            scatter=True,
            lowess=non_linear,
            scatter_kws={"color": "black"},
            line_kws={"color": "black"},
        )

    plt.ylim(0, 100)
    plt.xlim(5, 25)
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)


def test_plot(df):
    """TEST"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="darkgrid")
    plt.scatter(data=df, x="Age", y="Beta_percent", color="orange")
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    figdata_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return figdata_png

def jess_plot(df):
    """TEST"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="darkgrid")
    plt.scatter(data=df, x="Age", y="Beta_percent", color="black")
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    figdata_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return figdata_png
    

def sex_plot(df):
    """TEST"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="darkgrid")
    # plt.scatter(df["Age"], df["Beta_percent"], c="green")
    sns.scatterplot(data=df, x="Age", y="Beta_percent", hue="Sex")
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    figdata_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return figdata_png
