from flask import Flask, request, jsonify
import functions

app = Flask(__name__)


@app.route("/")
def welcome():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to FNR API!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to FNR API!</h1>
            <p>This is a Flask API for handling FNR (Fødselsnummer) operations.</p>
        </div>
    </body>
    </html>
    """


@app.route("/validate", methods=['POST'])
def validate_fnr():
    return process_request(functions.validate_fnr_json)


@app.route("/get_age", methods=['POST'])
def get_age():
    return process_request(functions.calculate_age)


@app.route("/get_gender", methods=['POST'])
def get_gender():
    return process_request(functions.define_gender)


def process_request(process_function):
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        fnr = data.get('fnr')
        response = process_function(fnr)
        return jsonify(response), 200
    else:
        return "<h1>405 Method Not Allowed</h1>", 405
