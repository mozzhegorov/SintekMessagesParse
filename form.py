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
    alphaconfig = FileField("alphaconfig.xmlcfg: ", validators=[DataRequired()])
    externalobjects = FileField("externalobjects.xml: ", validators=[DataRequired()])
    dp_in_prg = FileField("dp_in_prg.xsy: ", validators=[DataRequired()])
    dpa_in_prg = FileField("dpa_in_prg.xsy: ", validators=[])
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
