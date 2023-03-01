from datetime import datetime
import time

from flask import flash
from app import db
from app.models.tables import Importeds
from app.models.reports import Reports
from app.models.financial import Financial
from app.models.clients import Client
from app.models.benefits import Benefit
from app.models.tools import (
    generate_folder,
    generate_route,
    generate_token,
    generate_filename,
    file_size,
    save_files,
    open_xlsx,
    open_remessa,
    open_repasse,
    check_month,
    generate_reports,
)


class Imports:
    def imports(token, filename, referent, size, folder, user):
        i = Importeds(
            token,
            filename,
            referent,
            datetime.now().strftime("%d/%m/%Y"),
            datetime.now().strftime("%H:%M:%S"),
            size,
            folder,
            user,
        )
        db.session.add(i)
        db.session.commit()
        db.session.close()
        return True

    def base(files, user, institution):
        folder = generate_folder("UPLOAD_FOLDER")
        route = generate_route("UPLOAD_FOLDER", folder)
        for file in files:
            token = generate_token()
            filename = generate_filename(token, file)
            # size = file_size(file)
            size = "*"
            save_files(file, filename, route)
            Imports.imports(token, filename, "base", size, folder, user)
            ####
            data = open_xlsx(file)
            new_clients, error_clients = Client.create_client(data, institution)
            new_benefits, error_benefits = Benefit.create_benefit(data)
            token_reports = generate_reports(new_clients, error_clients, new_benefits, error_benefits)
            Reports.reports(token_reports, f"{token_reports}.txt", "reports", "*", "REPORTS", user)
            ####
        return True

    def remessa(files, user):
        for file in files:
            folder = generate_folder("UPLOAD_FOLDER")
            token = generate_token()
            filename = file.filename
            route = generate_route("UPLOAD_FOLDER", folder)
            size = "0"
            save_files(file, filename, route)
            Imports.imports(token, filename, "remessa", size, folder, user)
            ####
            data = open_remessa(route, file.filename)
            Client.update_client(data, "remessa")
            ####
        return True

    def repasse(files, user):
        for file in files:
            try:
                folder = generate_folder("UPLOAD_FOLDER")
                token = generate_token()
                filename = file.filename
                route = generate_route("UPLOAD_FOLDER", folder)
                size = "0"
                save_files(file, filename, route)
                imports = Imports.consult_imported("repasse") 
                month = check_month(route, filename, imports)
                if month:
                    ####
                    data = open_repasse(route, filename)
                    Financial.create_financial(data)
                    ####
                    Imports.imports(token, filename, "repasse", size, month, user)
                    return True
            except:
                flash("ERRO < Problema com seu Arquivo.")
        return False


    def document(files, user):
        for file in files:
            try:
                folder = generate_folder("UPLOAD_FOLDER")
                token = generate_token()
                filename = file.filename
                route = generate_route("UPLOAD_FOLDER", folder)
                size = "0"
                save_files(file, filename, route)
                Imports.imports(token, filename, "document", size, folder, user)
                Client.update_client(file, "document")
            except:
                flash("ERRO < Problema com seu Arquivo.")
        return True

    def document_by_cpf(file, user):
        folder = generate_folder("UPLOAD_FOLDER")
        token = generate_token()
        filename = file.filename
        route = generate_route("UPLOAD_FOLDER", folder)
        size = "0"
        save_files(file, filename, route)
        Imports.imports(token, filename, "document", size, folder, user)
        Client.update_client(file, "document")
        return True

    def consult_imported(value, method=None):
        if method == "token":
            return Importeds.query.filter_by(token=value).first()
        if method == "filename":
            return Importeds.query.filter_by(filename=f"{value}.zip").first()
        if method == "all":
            return Importeds.query.all()
        return Importeds.query.filter_by(referent=value).all()
