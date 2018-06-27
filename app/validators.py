from wtforms import ValidationError

from app.models import User


class ExistingUsernameOrEmail:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(name=field.data).first()
        if user is not None:
            return
        user = User.query.filter_by(email=field.data).first()
        if user is None:
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
            return
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return
        if not user.check_password(field.value):
            raise ValidationError(self.message)
