# -*- coding: utf-8 -*-
import io, codecs
import os
import xml.etree.ElementTree as tree
from flask import Flask, request, redirect, render_template, url_for, send_file, Response
from wtforms import StringField

from form import SintekMSGGenerate, HEX2DEC
from main import generate_messages_file

app = Flask(__name__, template_folder='templates')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/sintekmsg/', methods=['get', 'post'])
def sintekmsg():
    form = SintekMSGGenerate()
    if form.validate_on_submit():
        alphaconfig = form.alphaconfig.data.read().decode('utf-8')
        externalobjects = form.externalobjects.data.read()
        dp_in_prg = form.dp_in_prg.data.read().decode('utf-8')
        messages = generate_messages_file(alphaconfig, externalobjects, dp_in_prg)
        mem = io.BytesIO()
        StreamWriter = codecs.getwriter('utf-8')
        wrapper_file = StreamWriter(mem)
        print(messages.getvalue(), file=wrapper_file)
        mem.seek(0)
        return Response(
            mem,
            mimetype="text/csv; charset=UTF-8",
            headers={"Content-disposition":
                         "attachment; filename=myplot.csv"}
        )
        # return send_file(os.path.join(app.root_path, path), as_attachment=True)

    return render_template('sintek_msg_generate.html', form=form)


@app.route('/hex2dec/', methods=['get', 'post'])
def hex2dec():
    form = HEX2DEC()
    if form.validate_on_submit():
        hexs = []
        for item in form:
            if "hex" in item.name:
                hexs.append(int(item.data, 16))
        return render_template(
            'hex_to_dec.html',
            form=form,
            decresult=hexs
        )

    return render_template('hex_to_dec.html', form=form)


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
