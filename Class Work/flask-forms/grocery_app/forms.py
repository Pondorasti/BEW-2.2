from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, URL, ValidationError
from .models import GroceryStore, ItemCategory
from .models import User


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already taken! Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField("Title", validators=[
                        DataRequired(), Length(min=3, max=16)])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Submit")


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField("Name", validators=[
                       DataRequired(), Length(min=3, max=16)])
    price = FloatField("Price $", validators=[
                       DataRequired(), NumberRange(min=0)])
    category = SelectField("Category", validators=[
                           DataRequired()], choices=ItemCategory.choices())
    photo_url = StringField("Photo URL", validators=[URL()])
    store = QuerySelectField("Store", validators=[
                             DataRequired()], query_factory=lambda: GroceryStore.query)
    submit = SubmitField("Submit")

    def validate_name(self, name):
        if "dragonegg" in name.data.lower().replace(" ", ""):
            raise ValidationError("Dragon eggs are not allowed!")
