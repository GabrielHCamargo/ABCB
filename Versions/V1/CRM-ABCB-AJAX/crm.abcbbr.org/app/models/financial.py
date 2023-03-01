from datetime import datetime

from app import db
from app.models.tables import Finance
from app.models.tools import generate_token


class Financial:
    def create_financial(data):
        for i in data:
            r = {
                "token": generate_token(),
                "nb": i["nb"],
                "month": i["month"],
                "discount": str(float(i["discount"][:3] + "." + i["discount"][3:])).replace(".", ","),
            }

            r = Finance(**r)

            try:
                db.session.add(r)
                db.session.commit()
            except:
                db.session.rollback()
        db.session.close()
        return True

    def consult_financial(value, method):
        if method == "nb":
            f = []
            for v in value:
                f.append(Finance.query.filter_by(nb=v.nb).all())
            return f
