#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify
from ebayapi import user_info, get_orders

app = Flask(__name__)
user = user_info()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/v1/user_info', methods=['GET'])
def user_info():
    return jsonify(user)

@app.route('/api/v1/totalsales', methods=['GET'])
def totalsales():
    totalsales = get_orders()
    print(totalsales)
    return jsonify(totalsales)


'''@app.route('/api/v1/get_messages', methods=['GET'])
def get_messages():
    messages = messages()
    return jsonify(messages)'''


if __name__ == '__main__':
    app.run(debug=True)