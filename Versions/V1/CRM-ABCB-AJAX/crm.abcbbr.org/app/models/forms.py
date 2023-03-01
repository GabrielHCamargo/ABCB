from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    MultipleFileField,
    DateField,
    SelectField,
    FileField,
)
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class ImportForm(FlaskForm):
    files = MultipleFileField("files[]", validators=[DataRequired()])


class ExportForm(FlaskForm):
    start = DateField("start", format="%d/%m/%Y", validators=[Optional()])
    end = DateField("end", format="%d/%m/%Y", validators=[Optional()])
    records = SelectField(
        choices=("Novos - Mês atual", "Antigos", "Todos"), validators=[Optional()]
    )


class ClientForm(FlaskForm):
    nb = StringField("nb")
    cpf = StringField("cpf")
    rg = StringField("rg")
    name = StringField("name")
    birth_date = StringField("birth_date")
    mother = StringField("mother")
    species = StringField("species")
    salary = StringField("salary")
    address = StringField("address")
    neighborhood = StringField("neighborhood")
    cep = StringField("cep")
    city = StringField("city")
    state = StringField("state")
    phone = StringField("phone")
    dib = StringField("dib")
    bank = StringField("bank")
    agency = StringField("agency")
    account = StringField("account")
    status = SelectField(
        "status",
        choices=[
            ("inclusion", "Aguardando Inclusão"),
            ("activated", "Ativado"),
            ("canceled", "Cancelado"),
            ("cancel", "A Cancelar"),
            ("error", "Erro"),
        ],
    )
    status_benefit = SelectField(
        "status_benefit",
        choices=[
            ("inclusion", "Aguardando Inclusão"),
            ("activated", "Ativado"),
            ("canceled", "Cancelado"),
            ("cancel", "A Cancelar"),
            ("error", "Erro"),
        ],
    )
    upload_date = StringField("upload_date")
    update_date = StringField("update_date")
    obs = StringField("obs")
    document = FileField("document")
