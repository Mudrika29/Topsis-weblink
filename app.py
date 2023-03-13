from flask import Flask , render_template, request
import os
from email.message import EmailMessage
import ssl
import smtplib
import io
import zipfile
import glob
# import csv
from func import download_videos
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def getValue():
    x=request.form['Singer']
    n=request.form['Number']
    email=request.form['email']
    d = request.form['Duration']

    # try:
    #     download_videos(x,n,d)
    # except:
    #     return render_template('error.html')
    try:
        download_videos(x,n,d)
    except:
        return render_template("error.html")
    # app = Flask(__name__, template_folder='templates')
    # buffer = io.BytesIO()
    # with zipfile.ZipFile(buffer, 'w') as myzip:
    #     myzip.write("static/mashup.mp3", arcname="mashup.mp3")
    # buffer.seek(0)

    # with open("static/mashup.zip", "wb") as f:
    #     f.write(buffer.read())

    email_sender = 'mudrika587@gmail.com'
    email_password = 'jibargttqhobsrzr'

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as myzip:
        myzip.write(f"static/{x}/mashup.mp3", arcname="mashup.mp3")
    buffer.seek(0)

    with open(f"static/{x}/mashup.zip", "wb") as f:
        f.write(buffer.read())

    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = 'Mail'
    em.set_content("Hey! Here is your mashup file.")

    with open(f"static/{x}/mashup.zip", 'rb') as fp:
        file_data = fp.read()
    em.add_attachment(file_data, maintype='application',subtype='mp3',filename="mashup.zip")

    context = ssl.create_default_context()
    email_receiver = email
    em['To'] = email_receiver
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    n=int(n)
    for i in range(0,n):
        os.remove(f"static/{x}/{i}.mp3")
        os.remove(f"static/{x}/{i}.mp4")
    os.remove(f"static/{x}/mashup.mp3")
    os.remove(f"static/{x}/mashup.zip")
    os.rmdir(f"static/{x}")
    
    # os.remove(f"static/mashup.zip")
    return render_template('pass.html')

    # return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)