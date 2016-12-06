# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from uzRequests import uzrequest
from urllib import unquote
app = Flask(__name__)


@app.route('/')
def hello_world():

    return 'hello'


@app.route('/get')
def check_route():
    response = uzrequest().postRequest('Киев', 'Ивано-Франковскdddddd', '31.12.2016')
    if response is not None:
        trains = uzrequest().parse_response(response.content)

    return render_template('index.html', trains=trains)


@app.route('/post', methods=['POST', 'GET'])
def return_data():
    if request.method =='POST':
        arrival = request.form.get('a')
        destination = request.form.get('d')
        date = request.form.get('dt')
    response = uzrequest().postRequest(arrival.encode('utf-8'), destination.encode('utf-8'), date)

    return response.content

@app.route('/geth')
def return_by_headers():
    if request.method == 'GET':
        arrival = request.args.get('a')
        destination = request.args.get('d')
        date = request.args.get('dt')
    response = uzrequest().postRequest(unquote(arrival).encode('utf-8'), unquote(destination).encode('utf-8') , date)

    return response.content

if __name__ == '__main__':
    app.run()
