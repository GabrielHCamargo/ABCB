from app import app
from flask import render_template, flash, redirect, request
from flask_login import login_required, current_user
from app.models.forms import ExportForm
from app.models.exports import Exports
from app.models.imports import Imports


@app.route("/export-records/<objective>")
@login_required
def export_records(objective):
    form = ExportForm()
    if objective == "select":
        return render_template("export-records-select.html")
    if objective == "base":
        e = Exports.consult_exported(objective)
        return render_template("export-records-base.html", form=form, exporteds=e)
    if objective == "document":
        i = Imports.consult_imported(objective)
        return render_template("export-records-document.html", form=form, importeds=i)


@app.route("/export/<objective>", methods=["GET", "POST"])
@login_required
def export_file(objective):
    start = request.form.get("start")
    end = request.form.get("end")
    records = request.form.get("records")
    if objective == "export-base":
        response = Exports.base(start, end, records, current_user.name)
        if response:
            return response
        flash("Não foi possível gerar o arquivo.")
        return redirect("/export-records/base")
    if objective == "export-document":
        response = Exports.document(start, end, records, current_user.name)
        if response:
            return response
        flash("Não foi possível gerar o arquivo.")
        return redirect("/export-records/document")
    if objective == "model-base":
        return Exports.model()


@app.route("/export/export-document/<cpf>", methods=["GET"])
@login_required
def export_document_client(cpf):
    response = Exports.document_by_cpf(cpf, current_user.name)
    if response:
        return response
    flash("Não foi possível gerar o arquivo.")
    return redirect(f"/consult-clients/client-data/{cpf}")


@app.route("/export/historic/<objective>/<token>/<folder>")
@login_required
def export_historic(objective, token, folder):
    return Exports.historic(token, folder, objective, current_user.name)
