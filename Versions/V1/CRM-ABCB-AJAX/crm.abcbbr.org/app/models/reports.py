from datetime import datetime

from app import db
from app.models.tables import Reporteds


class Reports:
    def reports(token, filename, referent, size, folder, user):
        r = Reporteds(
            token,
            filename,
            referent,
            datetime.now().strftime("%d/%m/%Y"),
            datetime.now().strftime("%H:%M:%S"),
            size,
            folder,
            user,
        )
        db.session.add(r)
        db.session.commit()
        db.session.close()
        return True

    def consult_reported(value, method=None):
        if method == "token":
            return Reporteds.query.filter_by(token=value).first()
        if method == "filename":
            return Reporteds.query.filter_by(filename=f"{value}.zip").first()
        if method == "all":
            return Reporteds.query.all()
        if method == "referent":
            return Reporteds.query.filter_by(referent=value).all()
        return Reporteds.query.all()