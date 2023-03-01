import os
import secrets
import pandas as pd
import csv
import shutil
import zipfile
from datetime import datetime
from app import app, db
from flask import flash, send_file
from app.models.tables import Imported, Exported, Client


class Upload:
    def upload_base(file, name):
        folder_name = Upload.folder("UPLOAD_FOLDER")
        token = secrets.token_hex(16)
        filename = token + "." + file.filename.rsplit(".", 1)[1]
        route = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
        Upload.save(file, filename, route)
        if (
            file.filename.rsplit(".", 1)[1] == "xls"
            or file.filename.rsplit(".", 1)[1] == "xlsx"
        ):
            len_file = Upload.convert_csv(file, token, route, filename)
        Upload.clients(route, token)
        Upload.imported(token, filename, "base", name, folder_name, str(len_file))
        return True

    def upload_return(file, referent, name):
        folder_name = Upload.folder("UPLOAD_FOLDER")
        route = os.path.join(app.config["UPLOAD_FOLDER"], folder_name)
        token = secrets.token_hex(16)
        Upload.save(file, file.filename, route)
        # Upload.imported(token, file.filename, referent, name, file.content_length)
        Upload.imported(
            token, file.filename, referent, name, folder_name, file.content_length
        )
        if referent == "remessa":
            list_update = Upload.update_remessa(os.path.join(route, file.filename))
            Upload.clients_update(list_update)
        if referent == "repasse":
            list_update = Upload.update_repasse(os.path.join(route, file.filename))
        return True

    def clients_update(list_update):
        result = ""
        for list in list_update:
            if list["result"] == "1":
                result = "activated"
            if list["result"] == "2":
                result = "pending"
            if list["result"] == "0":
                result = "automatic_movement"
            try:
                client = Clients.query.filter_by(nb=list["nb"]).first()
                client.status = result
                db.session.add(client)
                db.session.commit()
                db.session.close()
            except:
                pass

    def update_repasse(file):
        list_update = []
        with open(file, "r") as file:
            for line in file:
                if not line[1:11] == "REPASSE 20":
                    r = {
                        "nb": line[1:11],
                        "competence": line[11:17],
                        "discounted": line[21:26],
                    }
                    list_update.append(r)
        return list_update

    def update_remessa(file):
        list_update = []
        with open(file, "r") as file:
            for line in file:
                if not line[1:11] == "AMAR BRASI":
                    r = {
                        "nb": line[1:11],
                        "operation": line[11],
                        "result": line[12],
                        "error": line[13:16],
                        "discounted": line[16:21],
                        "start_date": line[21:29],
                    }
                    list_update.append(r)
        return list_update

    def upload_document(files, name):
        for file in files:
            folder_name = Upload.folder("DOCUMENT_FOLDER")
            route = os.path.join(app.config["DOCUMENT_FOLDER"], folder_name)
            token = secrets.token_hex(16)
            Upload.save(file, file.filename, route)
            Upload.imported(
                token, file.filename, "document", name, folder_name, file.content_length
            )
            client = Clients.query.filter_by(
                cpf=file.filename.rsplit(".", 1)[0]
            ).first()
            client.documents = True
            db.session.add(client)
            db.session.commit()
            db.session.close()
        return True

    def folder(url):
        folder_name = str(datetime.now().year) + str(datetime.now().month)
        if not os.path.isdir(os.path.join(app.config[url], folder_name)):
            os.mkdir(os.path.join(app.config[url], folder_name))
        return folder_name

    def convert_csv(file, token, route, filename):
        new_filename = token + ".csv"
        wb = pd.read_excel(os.path.join(route, filename))
        df = pd.DataFrame(wb)
        df.to_csv(new_filename, sep=",", index=False, encoding="utf-8")
        shutil.move(os.path.join(os.getcwd(), new_filename), route)
        return len(wb)

    def imported(token, filename, referent, name, folder_name, len_file):
        i = {
            "token": token,
            "filename": filename,
            "referent": referent,
            "date": datetime.now().strftime("%d/%m/%Y"),
            "hour": datetime.now().strftime("%H:%M:%S"),
            "amount": len_file,
            "folder": folder_name,
            "sender": name,
        }
        i = Imported(**i)
        db.session.add(i)
        db.session.commit()
        db.session.close()
        return True

    def save(file, filename, route):
        file.save(os.path.join(route, filename))
        return True

    def clients(route, filename):
        filename = filename + ".csv"
        with open(os.path.join(route, filename)) as file:
            linhas = csv.reader(file)
            for column in linhas: 
                if column[1] != "NB 1":
                    nb = [column[1], column[2], column[3]]
                    nb = Upload.model_nb(nb)
                    cpf = column[4]
                    if len(cpf) < 11:
                        cpf = Upload.model_cpf(cpf)
                    data = {
                        "documents": False,
                        "nb": str(nb).strip("[]"),
                        "cpf": cpf,
                        "rg": column[5],
                        "name": column[6],
                        "birth_date": column[7],
                        "mother": column[8],
                        "species": column[9],
                        "salary": column[10].replace(".", ","),
                        "address": column[11],
                        "neighborhood": column[12],
                        "cep": column[13],
                        "city": column[14],
                        "state": column[15],
                        "phone": column[16],
                        "dib": column[17],
                        "bank": column[18],
                        "agency": column[19],
                        "account": column[20],
                        "status": "inclusion",
                        "upload_date": datetime.now().strftime("%d/%m/%Y"),
                        "update_date": datetime.now().strftime("%d/%m/%Y"),
                        "obs": column[21],
                    }
                    try:
                        c = Clients(**data)
                        db.session.add(c)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        flash(
                            f'ATENÇÃO < O Cliente <{data["name"]}> está com o CPF idêntico ao de outro cliente. Por isso não foi importado.'
                        )
        db.session.close()
        return True

    def model_nb(nb):
        list_nb = []
        for i in nb:
            if i != "NB 1" and i != "NB 2" and i != "NB 3" and i != "":
                i = "{:0>10}".format(int(i))
                list_nb.append(i)
        return list_nb

    def model_cpf(cpf):
        return "{:0>11}".format(int(cpf))


class Download: 
    def model_base():
        return send_file(
            os.path.join(os.getcwd(), "upload/DATA/MODELO ABCB.xlsx"),
            as_attachment=True,
            mimetype="application/*",
        )

    def download_base(start_date, end_date, type_records, name):
        folder_name = Download.folder()
        token = secrets.token_hex(16)
        clients = Download.search_client(start_date, end_date, type_records)
        generate, size, route = Download.generate_base(clients, token, folder_name)
        if generate:
            period = Download.period(clients) 
            Download.exported(token, "base", size, period, folder_name, name)
            return Download.download(route, token, folder_name)
        return False

    def download_document_imported(token, folder, name):
        route = os.path.join(app.config["UPLOAD_FOLDER"], folder, f"{token}.zip")
        period = (
            datetime.now().strftime("%d/%m/%Y")
            + " - "
            + datetime.now().strftime("%d/%m/%Y")
        )
        Download.exported(token, "document", "*", period, folder, name)
        new_route = os.path.join(app.config["DOWNLOAD_FOLDER"], folder)
        shutil.copy2(route, new_route)
        return send_file(route, as_attachment=True, mimetype="application/*")

    def download_document(start_date, end_date, type_records, name):
        token = secrets.token_hex(16)
        documents = Download.search_document(start_date, end_date, type_records) 
        if len(documents) > 0:
            Download.folder()
            route, folder = Download.folder_document(documents, token)
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
            period = Download.period(documents)
            Download.exported(token, "document", "*", period, folder, name)
            return send_file(
                f"{route}.zip", as_attachment=True, mimetype="application/*"
            )
        return False

    def folder_document(documents, token):
        list_folder = []
        for document in documents:
            list_folder.append(document["folder"])
        folder = max(list_folder)
        route = os.path.join(app.config["DOWNLOAD_FOLDER"], folder, token)
        return route, folder
        # if not os.path.isdir(route):
        #     os.mkdir(os.path.join(route))
        # return route, folder

    def search_document(start_date, end_date, type_records):
        list_documents = []
        documents = Imported.query.filter_by(referent="document").all()
        if start_date == "" or start_date == None:
            start_date = ""
        if end_date == "" or end_date == None:
            end_date = ""
        if start_date == "" or end_date == "":
            if start_date == end_date:
                if type_records == "Novos - Mês atual":
                    for document in documents:
                        if document.date.split("/")[1] == str(datetime.now().month):
                            list_documents.append(
                                {
                                    "filename": document.filename,
                                    "folder": document.folder,
                                    "date": document.date,
                                }
                            )
                    return list_documents
                if type_records == "Antigos":
                    for document in documents:
                        if document.date.split("/")[1] != str(datetime.now().month):
                            list_documents.append(
                                {
                                    "filename": document.filename,
                                    "folder": document.folder,
                                    "date": document.date,
                                }
                            )
                    return list_documents
                for document in documents:
                    list_documents.append(
                        {
                            "filename": document.filename,
                            "folder": document.folder,
                            "date": document.date,
                        }
                    )
                return list_documents
            if start_date != end_date:
                flash("Data Inicial e Final devem ser informados.")
                return None
        if start_date != "" and end_date != "":
            start_date, end_date = start_date.split("-")[1], end_date.split("-")[1]
            for document in documents:
                if (
                    document.date.split("/")[1] == start_date
                    or document.date.split("/")[1] == end_date
                ):
                    list_documents.append(
                        {
                            "filename": document.filename,
                            "folder": document.folder,
                            "date": document.date,
                        }
                    )
            return list_documents
        return None

    def download(route, token, folder):
        filename = "D.SUB.GER.151." + folder
        return send_file(
            os.path.join(route, token),
            as_attachment=True,
            download_name=filename,
            mimetype="application/*",
        )

    def period(clients):
        list_day = []
        list_month = []
        list_year = []
        for client in clients:
            list_day.append(int(client["date"].split("/")[0]))
            list_month.append(int(client["date"].split("/")[1]))
            list_year.append(int(client["date"].split("/")[2]))
        start_date = (
            str(min(list_day)) + "/" + str(min(list_month)) + "/" + str(min(list_year))
        )
        end_date = (
            str(max(list_day)) + "/" + str(max(list_month)) + "/" + str(max(list_year))
        )
        return start_date + " - " + end_date

    def exported(token, referent, size, period, folder_name, name):
        e = {
            "token": token,
            "filename": token,
            "referent": referent,
            "date": datetime.now().strftime("%d/%m/%Y"),
            "hour": datetime.now().strftime("%H:%M:%S"),
            "amount": size,
            "period": period,
            "folder": folder_name,
            "requester": name,
        }
        e = Exported(**e)
        db.session.add(e)
        db.session.commit()
        db.session.close()

    def generate_base(clients, token, folder_name):
        route = os.path.join(app.config["DOWNLOAD_FOLDER"], folder_name)
        with open(os.path.join(route, token), "w") as file:
            file.write("0AMAR BRASIL      11\n")
            for client in clients:
                if client["status"] == "inclusion":
                    file.write(f'1{client["nb"]}1000000250\n')
                if client["status"] == "canceled":
                    file.write(f'1{client["nb"]}5000000250\n')
            size = "{:0>6}".format(int(len(clients)))
            file.write("9" + str(size))
        return True, str(size), route

    def search_client(start_date, end_date, type_records):
        list_clients = []
        clients = Clients.query.all()
        
        if start_date == "" or end_date == "":
            if start_date == end_date:
                if type_records == "Novos - Mês atual":
                    for client in clients:
                        if client.update_date.split("/")[1] == str(
                            datetime.now().month
                        ):
                            list_clients.append(
                                {
                                    "nb": client.nb,
                                    "status": client.status,
                                    "date": client.update_date,
                                }
                            )
                    return list_clients
                if type_records == "Antigos":
                    for client in clients:
                        if client.update_date.split("/")[1] != str(
                            datetime.now().month
                        ):
                            list_clients.append(
                                {
                                    "nb": client.nb,
                                    "status": client.status,
                                    "date": client.update_date,
                                }
                            )
                    return list_clients
                for client in clients:
                    list_clients.append(
                        {
                            "nb": client.nb,
                            "status": client.status,
                            "date": client.update_date,
                        }
                    )
                return list_clients
            if start_date != end_date:
                flash("Data Inicial e Final devem ser informados.")
                return None
        if start_date != "" and end_date != "":
            start_date, end_date = start_date.split("-")[1], end_date.split("-")[1]
            for client in clients:
                if (
                    client.update_date.split("/")[1] == start_date
                    or client.update_date.split("/")[1] == end_date
                ):
                    list_clients.append(
                        {
                            "nb": client.nb,
                            "status": client.status,
                            "date": client.update_date,
                        }
                    )
            return list_clients
        return None

    def folder():
        folder_name = str(datetime.now().year) + str(datetime.now().month)
        if not os.path.isdir(os.path.join(app.config["DOWNLOAD_FOLDER"], folder_name)):
            os.mkdir(os.path.join(app.config["DOWNLOAD_FOLDER"], folder_name))
        return folder_name
