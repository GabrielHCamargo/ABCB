from app import app
from flask import render_template, flash, redirect, request, jsonify, abort
from flask_login import login_required, current_user
from app.models.clients import Client
from app.models.imports import Imports
from app.models.forms import ClientForm
from app.models.tools import organize_status, document_rename
from app.models.financial import Financial
from app.models.benefits import Benefit


from app.models.tables import Clients
from app.models.tables import Benefits


@app.route('/autocomplete-cliente', methods=['POST'])
@login_required
def autocomplete_cliente():
    nome_ou_cpf_ou_nb = request.form['nome_ou_cpf']
    clients = Clients.autocomplete_client(nome_ou_cpf_ou_nb)
    benefits = Benefits.autocomplete_client(nome_ou_cpf_ou_nb)
    data = []
    if clients:
        nomes, cpfs = zip(*[(nome, cpf) for nome, cpf in clients])
        data = nomes + cpfs
    if benefits:
        data = tuple(data) + tuple(benefits)
    return jsonify({'nomes': data})



@app.route("/consulta-cliente", methods=["POST"])
@login_required
def consulta_cliente():
    nome_ou_cpf = request.form["nome_ou_cpf"]
    if len(nome_ou_cpf) == 11:
        client, result = Client.consult_client(cpf=nome_ou_cpf)
    elif len(nome_ou_cpf) == 10:
        benefit = Benefit.consult_benefit(nb=nome_ou_cpf)
        if benefit:
            client, result = Client.consult_client(cpf=benefit.cpf)
    else:
        nome_ou_cpf = nome_ou_cpf.upper()
        client, result = Client.consult_client(name=nome_ou_cpf)
    
    # Verifica se a consulta encontrou um cliente válido
    if client is None:
        abort(404)
    
    benefit = Benefit.consult_benefit(cpf=client.cpf)
    
    # Verifica se a consulta encontrou benefícios válidos
    if benefit is None:
        abort(404)

    elif not isinstance(benefit, list):
        benefit = [benefit]

    # Renderiza o template com os dados do cliente
    document, status_document = document_rename(client.documents)
    status = organize_status(benefit)
    financial = Financial.consult_financial(benefit, "nb")
    form = ClientForm()
    form.status_benefit.data = status
    form.status.data = status
    html = render_template(
        "client.html", 
        client=client,
        benefit=benefit,
        firts_name=result,
        form=form,
        status=status,
        document=document,
        status_document=status_document,
        financial=financial,
        enumerate=enumerate,
    )
    # Retorna o HTML como uma resposta AJAX
    return jsonify({"html": html})


@app.route("/consult-clients")
@login_required
def consult_clients():
    return render_template("consult-clients.html")


@app.route("/consult-clients/client-data/<id>", methods=["GET"])
@app.route("/consult-clients/client-data", defaults={"id": None}, methods=["POST"])
@login_required
def client_data_read(id):
    name = request.form.get("name")
    cpf = request.form.get("cpf")
    nb = request.form.get("nb")
    form = ClientForm()
    if nb != None and nb != "":
        benefit = Benefit.consult_benefit(nb=nb)
        cpf = benefit.cpf
    client, result = Client.consult_client(name, cpf, id)
    if result is None:
        flash("ATENÇÃO < Dados informados não correspondem a nenhum cliente.")
        return redirect("/consult-clients")
    benefit = Benefit.consult_benefit(cpf=client.cpf, method="all")
    document, status_document = document_rename(client.documents)
    status = organize_status(benefit)
    form.status_benefit.data = status
    form.status.data = status
    financial = Financial.consult_financial(benefit[0].nb, "nb")
    return render_template(
        "client-data.html",
        client=client,
        benefit=benefit,
        firts_name=result,
        form=form,
        status=status,
        document=document,
        status_document=status_document,
        financial=financial,
        enumerate=enumerate,
    )


@app.route("/client-data/update", methods=["POST"])
@login_required
def client_data_update():
    form = ClientForm()
    document = request.files["document"]
    document = form.document.data
    if document:
        Imports.document_by_cpf(document, current_user.name)
    c = {
        "cpf": request.form.get("cpf"),
        "rg": request.form.get("rg"),
        "name": request.form.get("name"),
        "birth_date": request.form.get("birth_date"),
        "species": request.form.get("species"),
        "address": request.form.get("address"),
        "neighborhood": request.form.get("neighborhood"),
        "cep": request.form.get("cep"),
        "city": request.form.get("city"),
        "state": request.form.get("state"),
        "phone": request.form.get("phone"),
        "status": request.form.get("status"),
    }
    b = {
        "nb": request.form.get("nb"),
        "salary": request.form.get("salary"),
        "dib": request.form.get("dib"),
        "bank": request.form.get("bank"),
        "agency": request.form.get("agency"),
        "account": request.form.get("account"),
        "status": request.form.get("status"),
    }
    Client.update_client(c)
    Benefit.update_benefit(b)
    flash("CLIENTE < Atualizado com Sucesso.")
    return redirect(f"/consult-clients/client-data/{c['cpf']}")
