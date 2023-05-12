from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main_page(name=None):
    return render_template('index.html', name=name)
# `read-form` endpoint 
@app.route('/read-form', methods=['POST'])
def read_form():
  
    # Get the form data as Python ImmutableDict datatype 
    data = request.form
  
    ## Return the extracted information 
    return {
        'emailId'     : data['userEmail'],
        'phoneNumber' : data['userContact'],
        'password'    : data['userPassword'],
        'gender'      : 'Male' if data['genderMale'] else 'Female',
    }
  