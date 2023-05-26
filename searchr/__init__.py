import os
import re

from flask import Flask, render_template, request, redirect, url_for, flash, Response, g
import sqlite3
import click

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

DATABASE = 'searchr/site.db'
		
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



#main pages
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        searchr = request.form['searchr']
        return redirect(url_for('search', sample_name = searchr))
        #return render_template('project.html', project = searchr)
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/search/<sample_name>')
def search(sample_name):    # this route has been updated to use a template containing a form
        searchr = sample_name
        cursor = get_db().cursor()
        # search by uniprotID or name
        cursor.execute("SELECT individualID, cohort, sex, age, postConceptionWeeks \
                            from phenotype \
                            WHERE individualID LIKE ?", [searchr])
        get_db().commit()
        data_pheno = cursor.fetchall()
        # change age or post-conception weeks to -
        if data_pheno:
            i = data_pheno[0].index('')
            data_pheno[0]=list(data_pheno[0])
            data_pheno[0][i]='-'
        
        cursor.execute("SELECT acceptableFACS \
                            from facs \
                            WHERE individualID LIKE ? ", [searchr])
        get_db().commit()
        facs = cursor.fetchall()
            
        cursor.execute("SELECT individualID \
                    from rnaSeq \
                    WHERE individualID LIKE ? ", [searchr])
        get_db().commit()
        rna = cursor.fetchall()
            
        cursor.execute("SELECT individualID \
                    from atacSeq \
                    WHERE individualID LIKE ? ", [searchr])
        get_db().commit()
        atac = cursor.fetchall()
            
        cursor.execute("SELECT individualID \
                    from chipSeq \
                    WHERE individualID LIKE ? ", [searchr])
        get_db().commit()
        chip = cursor.fetchall()

            
        cursor.execute("SELECT individualID \
                    from dnaM \
                    WHERE individualID LIKE ? ", [searchr])
        get_db().commit()
        dnam = cursor.fetchall()
        if dnam == []:
            dnam = 'FALSE'
        else:
            dnam = 'TRUE'
        return render_template('table.html', data=data_pheno, facs=bool(facs), rna=bool(rna), atac=bool(atac), chip=bool(chip), dnam=bool(dnam))

@app.route('/search/<sample_name>/<table>')
def true(sample_name, table):
    cursor = get_db().cursor()
    cursor.execute("PRAGMA table_info({})".format(table))
    get_db().commit()
    colHead = cursor.fetchall()
    
    # return the camelcase table headings into normal format
    initial=[]
    headings=[]
    for x in range(len(colHead)):
        initial.append(colHead[x][1][0].upper()+colHead[x][1][1:])
        headings.append(re.findall('[A-Z][^A-Z]+|[A-Z][A-Z]+', initial[x]))
        headings[x]=(' '.join(headings[x]))
   
    cursor.execute("SELECT * FROM {} \
                        WHERE individualID LIKE ? ".format(table), [sample_name]) #give variable for both tablename and samplename
    get_db().commit()
    data = cursor.fetchall()
    return render_template('storage.html', data=data, headings=headings)



@app.route('/storage', methods=['GET', 'POST'])
def storage():
    title='Stock bulk samples'
    cursor = get_db().cursor()
    cursor.execute("PRAGMA table_info(bulk)")
    get_db().commit()
    colHead = cursor.fetchall()
    
    # return the camelcase table headings into normal format
    initial=[]
    headings=[]
    for x in range(len(colHead)):
        initial.append(colHead[x][1][0].upper()+colHead[x][1][1:])
        headings.append(re.findall('[A-Z][^A-Z]+|[A-Z][A-Z]+', initial[x]))
        headings[x]=(' '.join(headings[x]))

    cursor.execute("SELECT * \
                        from bulk")
    get_db().commit()
    data = cursor.fetchall()
    # get the bbnid and mass in one, possible vulnerable to attack
    if request.method == "POST":
        for key in request.form:
            BBNID = key.partition('.')[-1]
            newMass = request.form[key]
        cursor = get_db().cursor()
        cursor.execute("UPDATE bulk SET region = ? WHERE brainbankID = ?", [newMass, BBNID])  
        get_db().commit()
        
        #recall table from db
        cursor.execute("SELECT * \
                        from bulk")
        get_db().commit()
        data = cursor.fetchall()
        return render_template('storage.html', title = title, headings = headings, data=data, show_results=1, BBNID=BBNID, newMass=newMass)
    return render_template('storage.html', title = title, headings = headings, data=data, show_results=1)

if __name__ == '__main__':
    app.run(debug = True)
    
