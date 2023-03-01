from app.models.tables import Users


class Default:
    def user_validation(value, form):
        user = Users.query.filter_by(username=value).first()
        if user and user.password == form.password.data:
            return user
        return None
    
    def fetch_user(value):
        return Users.query.filter_by(id=value).first()
