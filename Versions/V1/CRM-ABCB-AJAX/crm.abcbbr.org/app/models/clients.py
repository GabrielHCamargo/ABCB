from datetime import date, datetime
from app import db
from app.models.tables import Clients, Codes, Benefits
from app.models.tools import generate_token


class Client:
    def create_client(data, institution):
        new_clients = []
        error_clients = []
        for i in data:
            c = {
                "token": generate_token(),
                "documents": False,
                "cpf": i[1],
                "rg": i[2],
                "name": i[3],
                "birth_date": i[4],
                "mother": i[5],
                "address": i[8],
                "neighborhood": i[9],
                "cep": i[10],
                "city": i[11],
                "state": i[12],
                "phone": i[13],
                "institution": institution,
                "status": "inclusion",
                "description": "Aguardando inclusão",
                "upload_date": datetime.now(),
                "update_date": datetime.now(),
                "obs": i[18],
            }

            c = Clients(**c)

            try:
                db.session.add(c)
                db.session.commit()
                new_clients.append(f"NOME: {i[3]} | CPF: {i[1]} | NB: {i[0]}")
            except BaseException as response:
                db.session.rollback()
                err = response.__cause__
                client, client_name = Client.consult_client(cpf=i[1])
                if client is None:
                    error_clients.append(
                        f"NOME: {i[3]} | CPF: {i[1]} | NB: {i[0]} | ERRO: {err}"
                    )
                db.session.rollback()
        db.session.close()
        return new_clients, error_clients

    def consult_client(name=None, cpf=None, id=None):
        if name != None and name != "":
            client = Clients.query.filter_by(name=name).first()
            if client:
                return client, client.name.split()[0]
            return None, None
        if cpf != None and cpf != "":
            client = Clients.query.filter_by(cpf=cpf).first()
            if client:
                return client, client.name.split()[0]
            return None, None
        if id != None and id != "":
            client = Clients.query.filter_by(cpf=id).first()
            if client:
                return client, client.name.split()[0]
            return None, None
        return Clients.query.all(), None

    def update_client(data, method=None):
        if method == "remessa":
            for list in data:
                codes = Codes.query.all()
                description = ""
                status = ""
                for code in codes:
                    if (
                        code.operation == list["operation"]
                        and code.result == list["result"]
                        and code.error == list["error"]
                    ):
                        description = code.description
                        status = code.status
                try:
                    benefit = Benefits.query.filter_by(nb=list["nb"]).first()
                    benefit.discounted = list["discounted"]
                    benefit.start_date = list["start_date"]
                    benefit.status = status
                    benefit.description = description
                    db.session.add(benefit)
                    db.session.commit()
                    db.session.rollback()
                    client = Clients.query.filter_by(cpf=benefit.cpf).first()
                    client.status = status
                    client.description = description
                    db.session.add(client)
                    db.session.commit()
                    db.session.rollback()
                except:
                    db.session.rollback()
            db.session.close()
            return True
        if method == "document":
            try:
                client = Clients.query.filter_by(
                    cpf=data.filename.rsplit(".")[0]
                ).first()
                client.documents = True
                db.session.add(client)
                db.session.commit()
            except:
                db.session.rollback()
            db.session.close()
            return True

        client = Clients.query.filter_by(cpf=data["cpf"]).first()
    
        # codes = Codes.query.all()
        # description = ""
        # status = ""
        # for code in codes:
        #     if code.status == data["status"]:
        #         description = code.description
        #         status = code.status
    
        data["mother"] = client.mother
        data["institution"] = client.institution
        data["upload_date"] = client.upload_date
        data["update_date"] = datetime.now()
        data["obs"] = client.obs
        data["status"] = client.status
        data["description"] = client.description

        client.cpf = data["cpf"]
        client.rg = data["rg"]
        client.name = data["name"]
        client.birth_date = data["birth_date"]
        client.mother = data["mother"]
        client.address = data["address"]
        client.neighborhood = data["neighborhood"]
        client.cep = data["cep"]
        client.city = data["city"]
        client.state = data["state"]
        client.phone = data["phone"]
        client.status = data["status"]
        client.description = data["description"]
        client.institution = data["institution"]
        client.upload_date = data["upload_date"]
        client.update_date = data["update_date"]
        client.obs = data["obs"]

        db.session.add(client)
        db.session.commit()
        db.session.close()
        return True

    def consult_by_filter(start, end, records):
        try:
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
            clients = (
                Clients.query.filter(Clients.update_date <= end)
                .filter(Clients.update_date >= start)
                .all()
            )
            nb = []
            for client in clients:
                nb.append(client)
            return nb
        except:
            data = date.today()
            if records == "Novos - Mês atual":
                clients = Clients.query.all()
                nb = []
                for client in clients:
                    nb.append(client)
                return nb
                # start = date(data.year, data.month, 1)
                # end = date(data.year, data.month, 28)
                # clients = (
                #     Clients.query.filter(Clients.update_date <= end)
                #     .filter(Clients.update_date >= start)
                #     .all()
                # )
                # nb = []
                # for client in clients:
                #     nb.append(
                #         client
                #     )
                # return nb
            if records == "Antigos":
                clients = Clients.query.all()
                nb = []
                for client in clients:
                    nb.append(client)
                return nb
                # month = data.month - 1
                # if month < 1:
                #     month = 1
                # start = date(2022, 12, 1)
                # end = date(data.year, month, 28)
                # clients = (
                #     Clients.query.filter(Clients.update_date <= end)
                #     .filter(Clients.update_date >= start)
                #     .all()
                # )
                # nb = []
                # for client in clients:
                #     nb.append(
                #         client
                #     )
                # return nb
            if records == "Todos":
                clients = Clients.query.all()
                nb = []
                for client in clients:
                    nb.append(client)
                return nb
