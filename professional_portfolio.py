from flask import Flask, render_template, request, send_from_directory
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


def connect_to_email_account():
    connection = smtplib.SMTP(host='smtp.gmail.com')
    connection.starttls()
    connection.login(
        user=os.getenv('email_user'),
        password=os.getenv('email_password')
    )
    return connection


def send_email(user_info):
    sender_email = os.getenv('email_user')
    recipient_email = os.getenv('email_user')

    subject = f'{user_info['name']} - {user_info['email']} accessed your profile!'
    message = (f'Name: {user_info['name']}\n'
               f'Email: {user_info['email']}\n'
               f'Phone: {user_info['phone']}\n'
               f'Message: {user_info['message']}')

    connection = connect_to_email_account()
    connection.sendmail(
        from_addr=sender_email,
        to_addrs=recipient_email,
        msg=f'Subject:{subject}\n\n{message}'.encode('utf-8')
    )
    connection.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')


@app.route('/')
def welcome():
    return render_template('index-svg.html')


@app.route('/Resume')
def download():
    return send_from_directory('static', path="files/Abhay's Updated Resume.pdf")


@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    if request.method == 'POST':
        user_info = {
            'name': request.form.get('Name'),
            'email': request.form.get('E-mail'),
            'phone': request.form.get('Phone'),
            'message': request.form.get('Message'),
        }
        send_email(user_info)
        return render_template('contact.html')
    return render_template('index-svg.html')


if __name__ == '__main__':
    app.run(debug=False, port=5003)
