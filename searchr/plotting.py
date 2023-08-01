# from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from statsmodels.nonparametric.smoothers_lowess import lowess as use_lowess

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
    sns.regplot(data=df, x="Age", y="Beta_percent")
    # sns.regplot(data=df, x="Age", y="Beta_percent", lowess=True) # for nonlinear fit

    # attempting to add confidence interval shading to lowess fit...
    # ...because adding ci=95 to sns.regplot() does not work (https://github.com/mwaskom/seaborn/issues/552)
    # However, looks like it was recently fixed https://github.com/zeelsheladiya/seaborn/commit/f72896831af24da2dc52961653368ba7438c1c2f
    # ...but it would seem this change is not present in the version of seaborn.regplot we are using
    # ...so perhaps we should update seaborn to the newest version and then try...
    # sns.regplot(data=df, x="Age", y="Beta_percent", lowess=True, ci=95)

    # my attempt below to manually add conf interval shading from the seaborn.regplot script
    # lowess_fit = use_lowess(df["Beta_percent"], df["Age"])
    # lowess_y = lowess_fit[:, 1]
    # ci = 95
    # lowess_ci = np.percentile(lowess_fit[:, 1:], [100 - ci / 2, ci / 2], axis=1)
    # x = df["Age"]
    # xseq = np.linspace(min(x), max(x), num=91)
    # plt.plot(xseq, lowess_y)
    # plt.fill_between(xseq, lowess_ci[0], lowess_ci[1], alpha=0.2)

    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    linear_png = base64.b64encode(img.getbuffer()).decode("ascii")

    # create the non-linear plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="darkgrid")
    sns.regplot(data=df, x="Age", y="Beta_percent", line_kws={"color": "red"})
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    nonlinear_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return linear_png, nonlinear_png


def sex_plot(df):
    """TEST"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %
    sns.set_style("white")  # white background to match test_plot()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        x=df["Age"], y=df["Beta_percent"], hue=df["Sex"], s=55
    )  # s = size of points. Increased to match point sizes in test_plot()
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    linear_png = base64.b64encode(img.getbuffer()).decode("ascii")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        x=df["Age"],
        y=df["Beta_percent"],
        hue=df["Sex"],
        s=55,
        palette=["green", "blue"],
    )  # s = size of points. Increased to match point sizes in test_plot()
    plt.xlabel("Age (PCW)", fontsize=15)
    plt.ylabel("DNA methylation (%)", fontsize=15)
    FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    nlinear_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return linear_png, nlinear_png


## prev versions of plotting functions ##


def test_plot1(df):
    """TEST"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="darkgrid")
    x = df["Age"]
    y = df["Beta_percent"]
    # plt.scatter(data=df, x="Age", y="Beta_percent", color="orange") # plot data points
    plt.scatter(x, y, color="green")

    # adding regression line #
    b, a = np.polyfit(x, y, deg=1)  # polynomial of degree 1 i.e. straight line
    xseq = np.linspace(
        min(x), max(x), num=100
    )  # seq of 100 values between smallest to largest age
    plt.plot(xseq, a + b * xseq, color="k", lw=2.5)  # add line to plot

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


def sex_plot1(df):
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
