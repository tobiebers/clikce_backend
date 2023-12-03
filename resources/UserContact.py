from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_mail import Mail, Message

def send_email(email, message_text):
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

    mail = Mail(app)

    with app.app_context():
        msg = Message("Bestätigung Ihrer Kontaktanfrage", recipients=[email])
        msg.body = f"Vielen Dank für Ihre Anfrage, {email}.\n\nIhre Nachricht: {message_text}"
        mail.send(msg)

class Contact(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        message_text = data.get('messageText')

        try:
            send_email(email, message_text)
            return jsonify(message="E-Mail erfolgreich gesendet.")
        except Exception as e:
            # Stellen Sie sicher, dass die Antwort serialisierbar ist
            return jsonify(message=f"Fehler beim Senden der E-Mail: {str(e)}"), 500