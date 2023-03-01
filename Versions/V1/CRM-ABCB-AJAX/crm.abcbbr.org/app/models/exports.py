import os
import shutil
import zipfile
from datetime import datetime

from app import app, db
from app.models.tables import Exporteds
from app.models.clients import Client
from app.models.benefits import Benefit
from app.models.imports import Imports
from app.models.tools import (
    search_document,
    folder_document,
    generate_folder,
    generate_token,
    generate_route,
    generate_base,
    download_file,
)


class Exports:
    def exported(token, filename, referent, size, period, folder, user):
        e = Exporteds(
            token,
            filename,
            referent,
            datetime.now().strftime("%d/%m/%Y"),
            datetime.now().strftime("%H:%M:%S"),
            size,
            period,
            folder,
            user,
        )
        db.session.add(e)
        db.session.commit()
        db.session.close()
        return True

    def base(start, end, records, user):
        folder = generate_folder("DOWNLOAD_FOLDER")
        filename = "D.SUB.GER.151." + folder
        token = generate_token()
        route = generate_route("DOWNLOAD_FOLDER", folder)
        clients = Client.consult_by_filter(start, end, records)
        inclusion, cancel = Benefit.consult_by_filter(clients)
        generate, size = generate_base(route, token, inclusion, cancel)
        if generate:
            # period = generate_period(clients)
            period = "*"
            Exports.exported(token, filename, "base", size, period, folder, user)
            return download_file(route, filename, token)
        return False

    def document(start, end, records, user):
        token = generate_token()
        list_documents = Imports.consult_imported("document")
        documents = search_document(list_documents, start, end, records)
        if len(documents) > 0:
            route, folder = folder_document(documents, token)
            zip = zipfile.ZipFile(token + ".zip", "w", zipfile.ZIP_DEFLATED)
            for document in documents:
                file = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    document["folder"],
                    document["filename"],
                )
                shutil.copy2(file, os.getcwd())
                zip.write(document["filename"])
                os.remove(document["filename"])
            zip.close()
            shutil.move(os.path.join(os.getcwd(), f"{token}.zip"), f"{route}.zip")
            # period = generate_period(documents)
            Exports.exported(
                token, document["filename"], "document", "*", "*", folder, user
            )
            return download_file(f"{route}.zip")
        return False

    def document_by_cpf(cpf, user):
        token = generate_token()
        document = Imports.consult_imported(cpf, "filename")
        filename = document.filename
        generate_folder("DOWNLOAD_FOLDER", document.folder)
        route = os.path.join(app.config["DOWNLOAD_FOLDER"], document.folder)
        file = os.path.join(
            app.config["UPLOAD_FOLDER"],
            document.folder,
            filename,
        )
        shutil.copy2(file, route)
        Exports.exported(
            token, filename, "document", "*", "*", document.folder, user
        )
        return download_file(os.path.join(route, filename))

    def model():
        return download_file(os.path.join(app.config["BASE_DIR"], "app", "static", "upload", "DATA", "MODELO-ABCB.xlsx"))

    def historic(token, folder, referent, user):
        if referent == "export-base":
            route = os.path.join(app.config["DOWNLOAD_FOLDER"], folder)
            file = Exporteds.query.filter_by(token=token).first()
            return download_file(route, file.filename, token)
        if referent == "export-base-upload":
            route = os.path.join(app.config["UPLOAD_FOLDER"], folder)
            return download_file(route, f"REPORTS {token}", token)
        if referent == "export-document":
            file = Imports.consult_imported(token, "token")
            route = os.path.join(app.config["UPLOAD_FOLDER"], folder, file.filename)
            # period = str(date.today()) + " - " + str(date.today())
            Exports.exported(token, token, "document", "*", "*", folder, user)
            new_route = os.path.join(
                app.config["DOWNLOAD_FOLDER"], folder, f"{token}.zip"
            )
            shutil.copy2(route, new_route)
            return download_file(new_route)

    def consult_exported(value):
        return Exporteds.query.filter_by(referent=value).all()
