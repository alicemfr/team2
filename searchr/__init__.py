from flask import Flask, render_template, request, redirect, url_for, g
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
        if searchr[0:2] == "cg" and len(searchr) > 9:
            searchr = "={}".format(searchr)
            return redirect(url_for("get_data", searchr=searchr))
        else:
            return redirect(url_for("get_gene", gene_name=searchr))
    return render_template("plot.html")


@app.route("/plot/<gene_name>", methods=["GET", "POST"])
def get_gene(gene_name):
    searchr = gene_name
    # search by gene
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT EPIC.ProbeName \
        from EPIC \
        WHERE EPIC.GeneName LIKE ?",
        [searchr],
    )
    get_db().commit()
    probe_result = cursor.fetchall()

    probe_list = []
    for i in probe_result:
        probe_list.append(i[0])

    return render_template(
        "probes.html", data=probe_result, show_results=1, searchr=searchr
    )  # title = title, headings = headings,


@app.route("/plot/cpg", methods=["GET", "POST"])
def send_probe():
    searchr = request.form.get("searchr")

    # return render_template("plot.html", gene=gene, searchr=probe)
    return redirect(url_for("get_data", searchr=searchr))


@app.route("/plot/cpg/<searchr>")
def get_data(
    searchr,
):  # this route has been updated to use a template containing a form
    # searchr = probe_name
    gene_name = searchr.split("=")[0].upper()
    probe_name = searchr.split("=")[1]
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT PROBEINFO.ProbeKey \
            FROM PROBEINFO \
            WHERE PROBEINFO.ProbeName = ?;",
        [probe_name],
    )
    probe_key_result = cursor.fetchall()
    index_CpG = probe_key_result[0][0]

    # Based on the Probe Key, run the corresponding query
    if index_CpG <= 107899:
        cursor.execute(
            "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, AAAVALUE.Value \
            FROM PROBEINFO, PHENO, AAAVALUE \
            WHERE AAAVALUE.ProbeKey = ? \
            AND PROBEINFO.ProbeKey = ? \
            AND AAAVALUE.SampleKey = PHENO.SampleKey;",
            [index_CpG, index_CpG],
        )
    elif 307899 >= index_CpG > 107899:
        cursor.execute(
            "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, BBBVALUE.Value \
            FROM PROBEINFO, PHENO, BBBVALUE \
            WHERE BBBVALUE.ProbeKey = ? \
            AND PROBEINFO.ProbeKey = ? \
            AND BBBVALUE.SampleKey = PHENO.SampleKey;",
            [index_CpG, index_CpG],
        )
    elif 507899 >= index_CpG > 307899:
        cursor.execute(
            "SELECT PROBEINFO.ProbeName, PHENO.Age, PHENO.Sex, CCCVALUE.Value \
            FROM PROBEINFO, PHENO, CCCVALUE \
            WHERE CCCVALUE.ProbeKey = ? \
            AND PROBEINFO.ProbeKey = ? \
            AND CCCVALUE.SampleKey = PHENO.SampleKey;",
            [index_CpG, index_CpG],
        )
    elif 807899 >= index_CpG > 507899:
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
    plot, nlinplot = test_plot(data)

    data, sexplot, nlinsexplot = sex_plot(data)
    return render_template(
        "table.html",
        # data=data,
        probe_name=probe_name,
        gene=gene_name,
        plot=plot,
        nlinplot=nlinplot,
        sexplot=sexplot,
        nlinsexplot=nlinsexplot,
    )


if __name__ == "__main__":
    app.run(debug=True)
