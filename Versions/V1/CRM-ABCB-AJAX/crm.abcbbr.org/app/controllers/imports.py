from app import app
from flask import render_template, flash, redirect, request
from flask_login import login_required, current_user
from app.models.forms import ImportForm
from app.models.imports import Imports
from app.models.reports import Reports


@app.route("/import-records/<objective>")
@login_required
def import_records(objective):
    form = ImportForm()
    if objective == "select":
        return render_template("import-records-select.html")
    if objective == "base":
        i = [i for i in reversed(Reports.consult_reported("reports"))]
        return render_template("import-records-base.html", form=form, importeds=i)
    if objective == "remessa":
        return render_template("import-records-remessa.html", form=form)
    if objective == "repasse":
        return render_template("import-records-repasse.html", form=form)
    if objective == "document":
        return render_template("import-records-document.html", form=form)


@app.route("/import/<objective>", methods=["GET", "POST"])
@login_required
def import_file(objective):
    form = ImportForm()
    if objective == "import-base":
        Imports.base(form.files.data, current_user.name, current_user.institution)
        flash("REGISTRO < Importado com Sucesso.")
        return redirect("/import-records/base")
    if objective == "import-remessa":
        Imports.remessa(form.files.data, current_user.name)
        flash("REGISTRO < Importado com Sucesso.")
        return redirect("/import-records/remessa")
    if objective == "import-repasse":
        try:
            i = Imports.repasse(form.files.data, current_user.name)
            if i:
                flash("REGISTRO < Importado com Sucesso.")
            else:
                flash("ATENÇÃO < Arquivo já enviado.")
        except:
            flash("ERRO < Problema com seu Arquivo.")
        return redirect("/import-records/repasse")
    if objective == "import-document":
        try:
            Imports.document(form.files.data, current_user.name)
            flash("REGISTRO < Importado com Sucesso.")
        except:
            flash("ERRO < Problema com seu Arquivo.")
        return redirect("/import-records/document")