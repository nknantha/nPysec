import re

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import fields, validators


def wtf_is_hidden_field(field: fields.Field) -> bool:
    return isinstance(field, fields.HiddenField)


class PasswordValidator:
    VALIDATION_PARAMETERS = {
        'upper case': r'[A-Z]',
        'lower case': r'[a-z]',
        'digits': r'\d',
        'special character': "[%s]" % re.escape(
            " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    }

    ERROR_MSG = "Password must contain atleast a %s."

    def __init__(self, min=1, max=-1):
        self.min = min
        self.max = max

    def __call__(self, form, field):

        # Minimum password length
        if len(field.data) < self.min:
            raise validators.ValidationError(
                message=f"Password must be at least {self.min} characters long.")

        for msg, pattern in self.VALIDATION_PARAMETERS.items():
            if re.search(pattern, field.data) is None:
                raise validators.ValidationError(self.ERROR_MSG % msg)


class SeaSurfForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ss_csrf_name = current_app.config.get('CSRF_COOKIE_NAME')

        # For enabling seasurf CSRF while using in forms.
        ss_csrf_token = current_app.jinja_env.globals['csrf_token']()

        ss_csrf_field = fields.HiddenField(
            default=ss_csrf_token,
            render_kw=dict(
                value=ss_csrf_token,
            )
        )
        options = dict(name=ss_csrf_name, prefix=self._prefix)
        ss_csrf_field = self.meta.bind_field(self, ss_csrf_field, options)
        self._fields[ss_csrf_name] = ss_csrf_field


class SignupForm(SeaSurfForm):
    name = fields.StringField(label="Name",
                              validators=[validators.DataRequired()])
    email = fields.EmailField(label="Email",
                                    validators=[validators.DataRequired(),
                                                validators.Email()])
    password = fields.PasswordField(label="Password",
                                    validators=[validators.DataRequired(),
                                                PasswordValidator(min=8)])
    submit = fields.SubmitField(label="Sign Up")


class SigninForm(SignupForm):
    name = None
    password = fields.PasswordField(label="Password",
                                    validators=[validators.DataRequired()])
    submit = fields.SubmitField(label="Sign In")
