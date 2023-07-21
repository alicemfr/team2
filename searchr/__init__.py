import os
import re

from flask import Flask, render_template, request, redirect, url_for, flash, Response, g
import sqlite3
import pandas as pd

from searchr.plotting import test_plot, sex_plot

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev"

DATABASE = "searchr/Team2_Siyi.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# main pages
@app.route("/", methods=["GET", "POST"])
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return render_template("example.html", title = "Example")

@app.route("/pipeline")
def pipeline():
    return render_template("pipeline.html", title="Analysis and Pipeline")


@app.route("/team")
def team():
    return render_template("team.html", title="Meet the plot-Me team")


@app.route("/plot", methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        searchr = request.form["searchr"]
        # sex = request.form["sex"]
        return redirect(url_for("get_data", gene_name=searchr))
    return render_template("plot.html")


@app.route("/plot/<gene_name>")
def get_data(
    gene_name,
):  # this route has been updated to use a template containing a form
    searchr = gene_name
    cursor = get_db().cursor()
    if searchr[0:2] == "cg" and len(searchr) > 9:
        check = "This is actiavted"
        cursor.execute(
            "SELECT PROBEINFO.ProbeKey \
                FROM PROBEINFO \
                WHERE PROBEINFO.ProbeName = ?;",
            [searchr],
        )
        result = cursor.fetchall()
        check = result
        index_CpG = result[0][0]
        check1 = index_CpG
        # Based on the Probe Key, run the corresponding query
        if index_CpG <= 107899:
            # check = "Go to AAA table"
            cursor.execute(
                "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, AAAVALUE.Value \
                FROM PROBEINFO, PHENO, AAAVALUE \
                WHERE AAAVALUE.ProbeKey = ? \
                AND PROBEINFO.ProbeKey = ? \
                AND AAAVALUE.SampleKey = PHENO.SampleKey;",
                [index_CpG, index_CpG],
            )
        elif 307899 >= index_CpG > 107899:
            check = "Go to BBB table"
            cursor.execute(
                "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, BBBVALUE.Value \
                FROM PROBEINFO, PHENO, BBBVALUE \
                WHERE BBBVALUE.ProbeKey = ? \
                AND PROBEINFO.ProbeKey = ? \
                AND BBBVALUE.SampleKey = PHENO.SampleKey;",
                [index_CpG, index_CpG],
            )
        elif 507899 >= index_CpG > 307899:
            check = "Go to CCC table"
            cursor.execute(
                "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, CCCVALUE.Value \
                FROM PROBEINFO, PHENO, CCCVALUE \
                WHERE CCCVALUE.ProbeKey = ? \
                AND PROBEINFO.ProbeKey = ? \
                AND CCCVALUE.SampleKey = PHENO.SampleKey;",
                [index_CpG, index_CpG],
            )
        elif 807899 >= index_CpG > 507899:
            check = "Go to DDD table"
            cursor.execute(
                "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, DDDVALUE.Value \
                FROM PROBEINFO, PHENO, DDDVALUE \
                WHERE DDDVALUE.ProbeKey = ? \
                AND PROBEINFO.ProbeKey = ? \
                AND DDDVALUE.SampleKey = PHENO.SampleKey;",
                [index_CpG, index_CpG],
            )
        get_db().commit()
        data = cursor.fetchall()
    else:
        # search by gene
        cursor.execute(
            "SELECT betas.CpG \
                from betas, epic \
                WHERE epic.CpG = betas.CpG AND\
                epic.GeneName LIKE ? \
                LIMIT 1;",
            [searchr],
        )
        get_db().commit()
        cpg = cursor.fetchall()
        cursor.execute(
            "SELECT betas.CpG, pheno.Age, betas.Value, pheno.Sex \
                                from betas, pheno \
                                WHERE betas.SampleName = pheno.SampleName AND \
                                betas.CpG LIKE ?",
            [cpg],
        )
    # get_db().commit()
    # data = cursor.fetchall()
    CpG_list = []
    Age_list = []
    Value_list = []
    Sex_list = []
    for i in data:
        CpG, Age, Sex, Value = i
        CpG_list.append(CpG)
        Age_list.append(Age)
        Sex_list.append(Sex)
        Value_list.append(Value)

    result_df = pd.DataFrame(list(zip(CpG_list, Age_list, Sex_list, Value_list)))
    result_df.columns = ["CpG", "Age", "Sex", "Value"]
    data = result_df

    # plot = age_scatter_save(data, False, False)
    # plot = test_plot(data)
    plot = test_plot(data)

    sexplot = sex_plot(data)
    return render_template("table.html", plot=plot, sexplot=sexplot)


if __name__ == "__main__":
    app.run(debug=True)
