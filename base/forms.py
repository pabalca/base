from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class SecretForm(FlaskForm):
    text = StringField(
        "Secret", validators=[DataRequired()], render_kw={"autofocus": True}
    )
    submit = SubmitField("Send")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    challenge = PasswordField("Challenge", render_kw={"autofocus": True})
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    submit = SubmitField("Generate")
