# Streamlit version of the frontend

from flask import Flask, request, jsonify
import streamlit as st
import step1
import step2_base
import step3

app = Flask(__name__)

@app.route('/step1', methods=['POST'])
def run_step1():
    data = request.json
    queries = data['queries']
    result = step1.process(queries)
    return jsonify({"result": result})

@app.route('/step2', methods=['POST'])
def run_step2():
    data = request.json
    location = data['location']
    placetype = data['placetype']
    messageprompt = data['messageprompt']
    result = step2_base.process(location, placetype, messageprompt)
    return jsonify({"result": result})

@app.route('/step3', methods=['POST'])
def run_step3():
    data = request.json
    filename = data['filename']
    result = step3.process(filename)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
