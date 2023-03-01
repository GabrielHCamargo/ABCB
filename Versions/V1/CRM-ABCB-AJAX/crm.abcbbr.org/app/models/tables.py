from app import db, login_manager
from sqlalchemy import or_


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    hierarchy = db.Column(db.String(255))
    institution = db.Column(db.String(255))
    status = db.Column(db.String(255))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, token, username, password, name, hierarchy, institution, status):
        self.username = username
        self.token = token
        self.password = password
        self.name = name
        self.hierarchy = hierarchy
        self.institution = institution
        self.status = status

    def __repr__(self):
        return "<User %r>" % self.username


class Importeds(db.Model):
    __tablename__ = "importeds"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    referent = db.Column(db.String(255))
    date = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    folder = db.Column(db.String(255))
    sender = db.Column(db.String(255))

    def __init__(self, token, filename, referent, date, hour, amount, folder, sender):
        self.token = token
        self.filename = filename
        self.referent = referent
        self.date = date
        self.hour = hour
        self.amount = amount
        self.folder = folder
        self.sender = sender

    def __repr__(self):
        return "<Imported %r>" % self.token


class Exporteds(db.Model):
    __tablename__ = "exporteds"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    referent = db.Column(db.String(255))
    date = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    period = db.Column(db.String(255))
    folder = db.Column(db.String(255))
    requester = db.Column(db.String(255))

    def __init__(
        self, token, filename, referent, date, hour, amount, period, folder, requester
    ):
        self.token = token
        self.filename = filename
        self.referent = referent
        self.date = date
        self.hour = hour
        self.amount = amount
        self.period = period
        self.folder = folder
        self.requester = requester

    def __repr__(self):
        return "<Exported %r>" % self.token


class Reporteds(db.Model):
    __tablename__ = "reporteds"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    referent = db.Column(db.String(255))
    date = db.Column(db.String(255))
    hour = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    folder = db.Column(db.String(255))
    sender = db.Column(db.String(255))

    def __init__(self, token, filename, referent, date, hour, amount, folder, sender):
        self.token = token
        self.filename = filename
        self.referent = referent
        self.date = date
        self.hour = hour
        self.amount = amount
        self.folder = folder
        self.sender = sender

    def __repr__(self):
        return "<Reported %r>" % self.token


class Clients(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    documents = db.Column(db.Boolean, default=False)
    cpf = db.Column(db.String(255), unique=True, nullable=False)
    rg = db.Column(db.String(255))
    name = db.Column(db.String(255))
    birth_date = db.Column(db.String(255))
    mother = db.Column(db.String(255))
    address = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255))
    cep = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    institution = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.String(255))
    upload_date = db.Column(db.String(255))
    update_date = db.Column(db.String(255))
    obs = db.Column(db.String(255))

    def __init__(
        self,
        token,
        documents,
        cpf,
        rg,
        name,
        birth_date,
        mother,
        address,
        neighborhood,
        cep,
        city,
        state,
        phone,
        institution,
        status,
        description,
        upload_date,
        update_date,
        obs,
    ):
        self.token = token
        self.documents = documents
        self.cpf = cpf
        self.rg = rg
        self.name = name
        self.birth_date = birth_date
        self.mother = mother
        self.address = address
        self.neighborhood = neighborhood
        self.cep = cep
        self.city = city
        self.state = state
        self.phone = phone
        self.institution = institution
        self.status = status
        self.description = description
        self.upload_date = upload_date
        self.update_date = update_date
        self.obs = obs

    def __repr__(self):
        return "<Clients %r>" % self.name
    
    @classmethod
    def autocomplete_client(cls, name_or_cpf):
        return cls.query.with_entities(cls.name, cls.cpf).filter(
            or_(cls.name.ilike(f'%{name_or_cpf}%'), cls.cpf.ilike(f'%{name_or_cpf}%'))
        ).limit(5).all()


class Benefits(db.Model):
    __tablename__ = "benefits"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    nb = db.Column(db.String(255), unique=True, nullable=False)
    cpf = db.Column(db.String(255))
    dib = db.Column(db.String(255))
    species = db.Column(db.String(255))
    salary = db.Column(db.String(255))
    bank = db.Column(db.String(255))
    agency = db.Column(db.String(255))
    account = db.Column(db.String(255))
    discounted = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(
        self,
        token,
        nb,
        cpf,
        dib,
        species,
        salary,
        bank,
        agency,
        account,
        discounted,
        start_date,
        status,
        description,
    ):
        self.token = token
        self.nb = nb
        self.cpf = cpf
        self.dib = dib
        self.species = species
        self.salary = salary
        self.bank = bank
        self.agency = agency
        self.account = account
        self.discounted = discounted
        self.start_date = start_date
        self.status = status
        self.description = description

    def __repr__(self):
        return "<Benefits %r>" % self.nb
    
    @classmethod
    def autocomplete_client(cls, nb):
        query =  cls.query.with_entities(cls.nb).filter(
            cls.nb.ilike(f'%{nb}%')
        ).limit(5)
        return [client.nb for client in query]


class Finance(db.Model):
    __tablename__ = "finance"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    nb = db.Column(db.String(255))
    month = db.Column(db.String(255))
    discount = db.Column(db.String(255))

    def __init__(self, token, nb, month, discount):
        self.token = token
        self.nb = nb
        self.month = month
        self.discount = discount

    def __repr__(self):
        return "<Finance %r>" % self.nb


class Codes(db.Model):
    __tablename__ = "codes"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(255))
    result = db.Column(db.String(255))
    error = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.String(255))

    def __init__(self, operation, result, error, description, status):
        self.operation = operation
        self.result = result
        self.error = error
        self.description = description
        self.status = status

    def __repr__(self):
        return "<Codes %r>" % self.operation
