from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.widgets import TextInput

HEX_REGEXP = r"^[0-9, a-f, A-F]{2}$"
HEX_VALIDATORS = [
            DataRequired(),
            Regexp(HEX_REGEXP),
            Length(min=2, max=2)
        ]
HEX_STYLE = {'style': 'width: 4ch; text-align: center'}


class SintekMSGGenerate(FlaskForm):
    alphaconfig = FileField("alphaconfig: ", validators=[DataRequired()])
    externalobjects = FileField("externalobjects: ", validators=[DataRequired()])
    dp_in_prg = FileField("dp_in_prg: ", validators=[DataRequired()])
    submit = SubmitField("Генерировать сообщения")


class HEX2DEC(FlaskForm):
    hex1 = StringField(
        "hex1: ",
        validators=HEX_VALIDATORS,
        render_kw=HEX_STYLE,
    )
    hex2 = StringField(
        "hex2: ",
        validators=HEX_VALIDATORS,
        render_kw=HEX_STYLE,
    )
    hex3 = StringField(
        "hex3: ",
        validators=HEX_VALIDATORS,
        render_kw=HEX_STYLE,
    )
    hex4 = StringField(
        "hex4: ",
        validators=HEX_VALIDATORS,
        render_kw=HEX_STYLE,
    )
    submit = SubmitField("Submit")
