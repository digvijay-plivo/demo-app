# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, Response, Flask, flash, redirect, render_template, request, session, abort
from flask_assets import Bundle, Environment

import plivo
from plivo import plivoxml

app = Flask(__name__, static_url_path='')

js = Bundle('', output = 'gen/main.js')
css = Bundle('bootstrap.css','chosen.css','style.css','Vbootstrap.css','Vchosen.css','Vstyle.css',output = 'gen/main.css')

assets = Environment(app)

assets.register('main_js','js')
assets.register('main_css','css')

auth_id = 'Auth_ID_HERE'
auth_token = 'Auth_TOKEN_HERE'


@app.route('/')
def index():
    return 'Index Page'

@app.route('/send_sms/', methods=['GET', 'POST'])
def outbound_sms():
    
    from_number= request.form.get("src_num")
    to_number= request.form.get("dst_num")
    content= request.form.get("text")

    
    if not content:
        content = "Test SMS with Plivo!"

    client = plivo.RestClient(auth_id, auth_token)
    try:
        response = client.messages.create(
                                          src= from_number,
                                          dst= to_number,
                                          text= content,
                                          )
        return render_template('result.html')
        print(response.__dict__)
        return response

    except plivo.exceptions.PlivoRestError as e:
        print(e)
#response = p.send_message(params)
# Prints the complete response

@app.route('/send_message/', methods=['GET', 'POST'])
def outbound_sms_template():
    return render_template('test.html')


#CALL STARTS HERE

@app.route('/success/', methods=['GET', 'POST'])
def call():
    
    from_number= request.form.get("src_num")
    to_number= request.form.get("dst_num")
    url= request.form.get("Answer_URL")

    if not url:
       url = "http://s3.amazonaws.com/static.plivo.com/answer.xml"
    
    client = plivo.RestClient(auth_id, auth_token)
    try:
        call_made = client.calls.create(
                                        from_= from_number,
                                        to_= to_number,
                                        answer_url= url,
                                        answer_method = 'GET',
                                        )
        return render_template('result_call.html')
        print(response.__dict__)
        return response

    except plivo.exceptions.PlivoRestError as e:
        print(e)
#response = p.send_message(params)
# Prints the complete response

@app.route('/call/', methods=['GET', 'POST'])

def outbound_call_template():
    return render_template('demoVoice.html')


if __name__ == "__main__":
    app.run(debug=True)
