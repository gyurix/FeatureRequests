from wtforms import ValidationError

from app.models import User


class ExistingUsernameOrEmail:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(name=field.data).first()
        if user is not None:
            field.usedType = "Username"
            return
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            field.usedType = "Email"
            raise ValidationError(self.message)


class ExistingModelName:
    def __init__(self, model, message):
        self.model = model
        self.message = message

    def __call__(self, form, field):
        model = self.model.query.filter_by(name=field.data).first()
        if model is not None:
            raise ValidationError(self.message)


class NotExistingUsername:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(name=field.data).first()
        if user is not None:
            raise ValidationError(self.message)


class NotExistingEmail:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError(self.message)


class CorrectPassword:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(name=form.email.data).first()
        if user is not None:
            if not user.check_password(field.data):
                raise ValidationError(self.message)
            return
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or user.check_password(field.data):
            raise ValidationError(self.message)
