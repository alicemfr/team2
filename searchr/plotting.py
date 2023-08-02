# from plotnine import *
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from statsmodels.nonparametric.smoothers_lowess import lowess as use_lowess
import statistics
from moepy import lowess


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
    """Generate linear and non-linear plots for whole dataset"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %

    # create the linear plot
    sns.set_style("white")
    p = sns.lmplot(
        x="Age", y="Beta_percent", data=df, height=5, aspect=1.75
    )  # width=height*aspect
    p.set_axis_labels("Age (PCW)", "DNA methylation (%)")
    img = io.BytesIO()
    p.savefig(img, format="png", dpi=300)
    # img.seek(0)
    linear_png = base64.b64encode(img.getbuffer()).decode("ascii")

    # ----------------------------------
    ## create non linear plot
    # ----------------------------------
    # Lowess method using moepy (Merit Order Effect Python)
    # url: https://ayrtonb.github.io/Merit-Order-Effect/
    # doi: 10.5281/zenodo.4642896

    # prepare data
    x = np.array(df["Age"])  # turn list into 1D arrays
    y = np.array(df["Beta_percent"])

    # run lowess model
    lowess_model = lowess.Lowess()
    lowess_model.fit(x, y)

    # predict on new x data
    x_pred = np.linspace(
        min(x), max(x), 91 * 2
    )  # added double the number of samples for tighter fit
    y_pred = lowess_model.predict(x_pred)

    # calc 95% confidence interval
    upper = y_pred + (1.96 * statistics.stdev(y_pred))  # 1.96 is equivalent to 2sd
    lower = y_pred - (1.96 * statistics.stdev(y_pred))

    sns.set_style(style="white")
    p = sns.lmplot(
        data=df, x="Age", y="Beta_percent", fit_reg=False, height=5, aspect=1.75
    )
    p.ax.plot(x_pred, y_pred, color="tab:blue", zorder=3)
    p.ax.fill_between(
        x_pred, y1=upper, y2=lower, alpha=0.1, color="tab:blue"
    )  # shaded conf interval
    p.set_axis_labels("Age (PCW)", "DNA methylation (%)")
    img = io.BytesIO()
    p.savefig(img, format="png", dpi=300)
    nonlinear_png = base64.b64encode(img.getbuffer()).decode("ascii")

    return linear_png, nonlinear_png


def sex_plot(df):
    """Generate linear and non-linear plots for each sex"""
    df["Beta_percent"] = (
        df["Value"] * 100
    )  # corresponding DNAm values for probe. Multiplied by 100 for %
    sns.set_style("white")

    p = sns.lmplot(
        x="Age", y="Beta_percent", hue="Sex", data=df, height=5, aspect=1.6
    )  # width=height*aspect
    p.set_axis_labels("Age (PCW)", "DNA methylation (%)")
    img = io.BytesIO()
    p.savefig(img, format="png", dpi=300)
    # img.seek(0)
    linear_png = base64.b64encode(img.getbuffer()).decode("ascii")

    # ---------------------------------------
    ## create non-linear plot
    # ---------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.set_style(style="whitegrid")

    # Lowess method using moepy (Merit Order Effect Python)
    # url: https://ayrtonb.github.io/Merit-Order-Effect/
    # doi: 10.5281/zenodo.4642896

    sex = {"F": [], "M": []}
    for s in set(df["Sex"]):
        # prepare data
        x = np.array(df[df["Sex"] == s]["Age"])  # turn list into 1D arrays
        y = np.array(df[df["Sex"] == s]["Beta_percent"])

        # run lowess model
        lowess_model = lowess.Lowess()
        lowess_model.fit(x, y)

        # predict on new x data
        x_pred = np.linspace(
            min(x), max(x), 91 * 2
        )  # added double the number of samples for tighter fit
        y_pred = lowess_model.predict(x_pred)

        # calc 95% confidence interval
        upper = y_pred + (1.96 * statistics.stdev(y_pred))  # 1.96 is equivalent to 2sd
        lower = y_pred - (1.96 * statistics.stdev(y_pred))

        sex[s] = [x_pred, y_pred, upper, lower]

    female = sex.get("F")
    male = sex.get("M")

    sns.set_style(style="white")
    p = sns.lmplot(
        data=df, x="Age", y="Beta_percent", fit_reg=False, height=5, aspect=1.75
    )
    # plot female regression line
    p.ax.plot(
        female[0],
        female[1],
        color="tab:blue",
        zorder=3,
        label="F",
    )
    p.ax.fill_between(
        female[0], y1=female[2], y2=female[3], alpha=0.1, color="tab:blue"
    )  # shaded conf interval

    # plot male regression line
    p.ax.plot(
        male[0],
        male[1],
        color="tab:orange",
        zorder=3,
        label="M",
    )
    p.ax.fill_between(
        male[0], y1=male[2], y2=male[3], alpha=0.1, color="tab:orange"
    )  # shaded conf interval

    p.ax.legend()
    p.set_axis_labels("Age (PCW)", "DNA methylation (%)")
    img = io.BytesIO()
    p.savefig(img, format="png", dpi=300)
    nonlinear_png = base64.b64encode(img.getbuffer()).decode("ascii")
    return linear_png, nonlinear_png
