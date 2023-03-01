from datetime import datetime
from app import db
from app.models.tables import Benefits, Codes
from app.models.tools import generate_token


class Benefit:
    def create_benefit(data):
        new_benefits = []
        error_benefits = []
        for i in data:
            b = {
                "token": generate_token(),
                "nb": i[0],
                "cpf": i[1],
                "dib": i[14],
                "species": i[6],
                "salary": i[7].replace(".", ","),
                "bank": i[15],
                "agency": i[16],
                "account": i[17],
                "discounted": None,
                "start_date": None,
                "status": "inclusion",
                "description": "Aguardando inclusão",
            }

            b = Benefits(**b)

            try:
                db.session.add(b)
                db.session.commit()
                new_benefits.append(
                    f"NOME: {i[3]} | CPF: {i[1]} | NB: {i[0]}"
                )
            except BaseException as response:
                db.session.rollback()
                err = response.__cause__
                error_benefits.append(
                    f"NOME: {i[3]} | CPF: {i[1]} | NB: {i[0]} | ERRO: {err}"
                )
        db.session.close()
        return new_benefits, error_benefits


    def update_benefit(data):
        benefit = Benefits.query.filter_by(nb=data["nb"]).first()

        codes = Codes.query.all()
        description = ""
        status = ""
        for code in codes:
            if data["status"] == code.status:
                description = code.description
                status = code.status

        benefit.salary = data["salary"]
        benefit.dib = data["dib"]
        benefit.bank = data["bank"]
        benefit.agency = data["agency"]
        benefit.account = data["account"]
        benefit.status = status
        benefit.description = description

        db.session.add(benefit)
        db.session.commit()
        db.session.close()
        return True
    

    def consult_benefit(nb=None, cpf=None, id=None, method=None):
        if nb != None and nb != "":
            benefit = Benefits.query.filter_by(nb=nb).first()
            if benefit:
                return benefit
            return None
        if cpf != None and cpf != "":
            if method == "all":
                benefit = Benefits.query.filter_by(cpf=cpf).all()
                if benefit:
                    return benefit
            benefit = Benefits.query.filter_by(cpf=cpf).first()
            if benefit:
                return benefit
            return None
        if id != None and id != "":
            benefit = Benefits.query.filter_by(id=id).first()
            if benefit:
                return benefit
            return None
        return Benefits.query.all()

    def consult_by_filter(clients):
        inclusion = []
        cancel = []
        for client in clients:
            nb = Benefits.query.filter_by(cpf=client.cpf).all()
            if client.status == "inclusion":
                for n in nb:
                    if n.status == "inclusion":
                        inclusion.append(n.nb)
            if client.status == "cancel":
                for n in nb:
                    cancel.append(n.nb)
            if client.status == "activated":
                for n in nb:
                    if n.status == "inclusion":
                        inclusion.append(n.nb)
                    if n.status == "cancel":
                        cancel.append(n.nb)
        return inclusion, cancel
