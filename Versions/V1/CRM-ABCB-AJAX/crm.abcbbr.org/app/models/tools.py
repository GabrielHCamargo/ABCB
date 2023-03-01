import os
import csv
import secrets
import pandas as pd
from datetime import date, datetime

from app import app
from flask import send_file, flash


def generate_folder(url, folder=None):
    month = str(date.today().month)
    if len(month) < 2:
        month = "{:0>2}".format(int(month))
    if folder is None:
        folder = str(date.today().year) + month
        if not os.path.isdir(os.path.join(app.config[url], folder)):
            os.mkdir(os.path.join(app.config[url], folder))
        return folder
    if not os.path.isdir(os.path.join(app.config[url], folder)):
        os.mkdir(os.path.join(app.config[url], folder))
    return folder


def folder_document(documents, token):
    list_folder = []
    for document in documents:
        list_folder.append(document["folder"])
    folder = max(list_folder)
    route = os.path.join(app.config["DOWNLOAD_FOLDER"], folder, token)
    return route, folder


def generate_token():
    return secrets.token_hex(16)


def generate_filename(token, file):
    return token + "." + file.filename.rsplit(".", 1)[1]


def generate_route(url, folder):
    return os.path.join(app.config[url], folder)


def save_files(file, filename, route):
    file.save(os.path.join(route, filename))
    return True


def convert_to_csv(file, filename):
    new_filename = filename.replace(filename.rsplit(".", 1)[1], "csv")
    wb = pd.read_excel(file)
    df = pd.DataFrame(wb)
    df.to_csv(new_filename, sep=",", index=False, encoding="utf-8")
    return True


def open_xlsx(file):
    list_data = []
    wb = pd.read_excel(file, converters={"DATA NASCIMENTO": str})
    for index, line in wb.iterrows():
        nb = line["NB"]
        try:
            nb = model_nb(nb)
            cpf = str(line["CPF"])
            if len(cpf) < 11:
                cpf = model_cpf(cpf)
            data = []
            data.append(nb)
            data.append(cpf)
            data.append(str(line["RG"]))
            data.append(str(line["NOME"]))
            data.append(str(line["DATA NASCIMENTO"]))
            data.append(str(line["MAE"]))
            data.append(str(line["ESPECIE"]))
            data.append(str(line["SALARIO"]))
            data.append(str(line["ENDERECO"]))
            data.append(str(line["BAIRRO"]))
            data.append(str(line["CEP"]))
            data.append(str(line["CIDADE"]))
            data.append(str(line["ESTADO"]))
            data.append(str(line["TELEFONE"]))
            data.append(str(line["DIB"]))
            data.append(str(line["BANCO"]))
            data.append(str(line["AGÊNCIA"]))
            data.append(str(line["CONTA"]))
            data.append(str(line["OBS"]))
            list_data.append(data)
        except:
            flash(f"ERRO < Confira o Cliente < NB: {nb}")
    return list_data


def open_csv(token):
    file_csv = os.path.join(app.config["BASE_DIR"], f"{token}.csv")
    list_data = []
    with open(file_csv) as file:
        wb = csv.reader(file)
        for line in wb:
            if line[0] != "#":
                nb = [line[1], line[2], line[3]]
                nb = model_nb(nb)
                cpf = line[4]
                if len(cpf) < 11:
                    cpf = model_cpf(cpf)
                data = line[5:22]
                data.insert(0, nb)
                data.insert(1, cpf)
                list_data.append(data)
    os.remove(file_csv)
    return list_data


def generate_base(route, token, inclusion, cancel):
    clients = []
    with open(os.path.join(route, token), "w") as file:
        file.write("0AMAR BRASIL      11\n")
        for nb in inclusion:
            file.write(f"1{nb}1000000250\n")
            clients.append(nb)
        for nb in cancel:
            file.write(f"1{nb}5000000250\n")
            clients.append(nb)
        size = "{:0>6}".format(int(len(clients)))
        file.write("9" + str(size))
    return True, str(size)


def generate_reports(new_clients, error_clients, new_benefits, error_benefits):
    token = generate_token()
    with open(
        os.path.join(app.config["UPLOAD_FOLDER"], "REPORTS", f"{token}.txt"), "w"
    ) as file:
        nc = len(new_clients)
        lec = len(error_clients)
        nb = len(new_benefits)
        leb = len(error_benefits)
        file.write(f"CLIENTES REGISTRADOS: {str(nc)}\n")
        file.write("------------------------------\n")
        file.write(f"CLIENTES NAO REGISTRADOS: {str(lec)}\n")

        file.write("------------------------------\n\n")

        file.write(f"BENEFICIOS REGISTRADOS: {str(nb)}\n")
        file.write("------------------------------\n")
        file.write(f"BENEFICIOS NAO REGISTRADOS: {str(leb)}\n")

        file.write("------------------------------\n\n\n")

        file.write(f"LISTA DE CLIENTES NAO REGISTRADOS:\n")
        for i in error_clients:
            file.write(f"{i}\n")

        file.write("\n------------------------------\n\n")

        file.write(f"LISTA DE BENEFICIOS NAO REGISTRADOS:\n")
        for i in error_benefits:
            file.write(f"{i}\n")
    return token


def generate_period(data):
    list_day = []
    list_month = []
    list_year = []
    for i in data:
        list_day.append(int(i["date"].split("/")[0]))
        list_month.append(int(i["date"].split("/")[1]))
        list_year.append(int(i["date"].split("/")[2]))
    start_date = (
        str(min(list_day)) + "/" + str(min(list_month)) + "/" + str(min(list_year))
    )
    end_date = (
        str(max(list_day)) + "/" + str(max(list_month)) + "/" + str(max(list_year))
    )
    return start_date + " - " + end_date


def download_file(route, filename=None, token=None):
    if token is None and filename is None:
        return send_file(
            route,
            as_attachment=True,
            mimetype="application/*",
        )
    if token is None:
        return send_file(
            os.path.join(route, filename),
            as_attachment=True,
            mimetype="application/*",
        )
    return send_file(
        os.path.join(route, token),
        as_attachment=True,
        download_name=filename,
        mimetype="application/*",
    )


def file_size(file):
    wb = (pd.read_excel(file, converters={"DATA NASCIMENTO": str}),)
    return len(wb)


def model_nb(nb):
    if type(nb) != float:
        nb = "{:0>10}".format(int(nb))
    return nb


def model_cpf(cpf):
    return "{:0>11}".format(int(cpf))


def open_remessa(route, filename):
    list_update = []
    with open(os.path.join(route, filename), "r") as file:
        for line in file:
            if not line[1:11] == "AMAR BRASI":
                if not line[0] == "9":
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


def open_repasse(route, filename):
    list_data = []
    month = ""
    with open(os.path.join(route, filename), "r") as file:
        for line in file:
            if line[1:7] == "REPASS":
                month = line[9:15]
            if not line[1:7] == "REPASS":
                if not line[0] == "9":
                    r = {
                        "nb": line[1:11],
                        "discount": line[21:26],
                        "month": month,
                    }
                    list_data.append(r)
    return list_data


def search_document(documents, start_date, end_date, type_records):
    list_documents = []
    for document in documents:
        list_documents.append(
            {
                "filename": document.filename,
                "folder": document.folder,
                "date": document.date,
            }
        )
    return list_documents
    # if start_date == "" or start_date == None:
    #     start_date = ""
    # if end_date == "" or end_date == None:
    #     end_date = ""
    # if start_date == "" or end_date == "":
    #     if start_date == end_date:
    #         if type_records == "Novos - Mês atual":
    #             for document in documents:
    #                 print(document.date.split("/")[1])
    #                 print(str(datetime.now().month))
    #                 if document.date.split("/")[1] == str(datetime.now().month):
    #                     list_documents.append(
    #                         {
    #                             "filename": document.filename,
    #                             "folder": document.folder,
    #                             "date": document.date,
    #                         }
    #                     )
    #             return list_documents
    #         if type_records == "Antigos":
    #             for document in documents:
    #                 if document.date.split("/")[1] != str(datetime.now().month):
    #                     list_documents.append(
    #                         {
    #                             "filename": document.filename,
    #                             "folder": document.folder,
    #                             "date": document.date,
    #                         }
    #                     )
    #             return list_documents
    #         for document in documents:
    #             list_documents.append(
    #                 {
    #                     "filename": document.filename,
    #                     "folder": document.folder,
    #                     "date": document.date,
    #                 }
    #             )
    #         return list_documents
    #     if start_date != end_date:
    #         flash("Data Inicial e Final devem ser informados.")
    #         return None
    # if start_date != "" and end_date != "":
    #     start_date, end_date = start_date.split("-")[1], end_date.split("-")[1]
    #     for document in documents:
    #         if (
    #             document.date.split("/")[1] == start_date
    #             or document.date.split("/")[1] == end_date
    #         ):
    #             list_documents.append(
    #                 {
    #                     "filename": document.filename,
    #                     "folder": document.folder,
    #                     "date": document.date,
    #                 }
    #             )
    #     return list_documents
    # return None


def organize_status(benefit):
    for b in benefit:
        if b.status == "inclusion":
            return b.description
        pass
    for b in benefit:
        if b.status == "activated":
            return b.description
        pass
    for b in benefit:
        if b.status == "canceled":
            return b.description
        pass
    for b in benefit:
        if b.status == "cancel":
            return b.description
        pass
    for b in benefit:
        if b.status == "error":
            return b.description
        pass


def document_rename(document):
    if document == True:
        return "Enviados", True
    return "Pendente", False


def check_month(route, filename, imports):
    month = ""
    with open(os.path.join(route, filename), "r") as file:
        for line in file:
            if line[1:7] == "REPASS":
                month = line[9:15]
    for i in imports:
        if i.folder == month:
            return None
    return month


