import os
import re

from flask import Flask, render_template, request, redirect, url_for, flash, Response, g
import sqlite3
import pandas as pd

import plotting

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev"

DATABASE = "searchr/Team2_demo.db"


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


@app.route("/pipeline")
def pipeline():
    return render_template("pipeline.html", title="Analysis and Pipeline")


@app.route("/plot", methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        searchr = request.form["searchr"]
        return redirect(url_for("get_data", gene_name=searchr))
    return render_template("plot.html")


@app.route("/plot/<gene_name>")
def get_data(
    gene_name,
):  # this route has been updated to use a template containing a form
    searchr = gene_name
    cursor = get_db().cursor()
    # search by gene
    cursor.execute(
        "SELECT betas.CpG, pheno.Age, betas.Value, pheno.Sex \
                            from betas, pheno \
                            WHERE betas.CpG LIKE ?",
        [searchr],
    )

    get_db().commit()
    data = cursor.fetchall()
    CpG_list = []
    Age_list = []
    Value_list = []
    Sex_list = []
    for i in data:
        CpG, Age, Value, Sex = i
        CpG_list.append(CpG)
        Age_list.append(Age)
        Value_list.append(Value)
        Sex_list.append(Sex)
    result_df = pd.DataFrame(list(zip(CpG_list, Age_list, Value_list, Sex_list)))
    result_df.columns = ["CpG", "Age", "Value", "Sex"]
    data = result_df

    plotting.age_scatter()
    return render_template("table.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
