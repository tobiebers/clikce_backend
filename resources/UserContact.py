from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_mail import Message

def send_email(user_data, admin_email):
    # Benutzerinformationen extrahieren
    first_name = user_data.get('firstName')
    last_name = user_data.get('lastName')
    email = user_data.get('email')
    country = user_data.get('country')
    message_text = user_data.get('messageText')

    # E-Mail an den Admin mit allen Benutzerinformationen
    admin_msg = Message(
        "Neue Kontaktanfrage",
        recipients=[admin_email],
        body=f"Kontaktanfrage erhalten:\n\n"
             f"Vorname: {first_name}\n"
             f"Nachname: {last_name}\n"
             f"E-Mail: {email}\n"
             f"Land: {country}\n"
             f"Nachricht: {message_text}"
    )

    # Bestätigungs-E-Mail an den Benutzer
    user_msg = Message(
        "Bearbeitung Ihrer Kontaktanfrage",
        recipients=[email],
        body=f"Vielen Dank für Ihre Anfrage.\n\n"
             f"Ihre Nachricht: {message_text}\n\n"
             "Wir werden uns in Kürze bei Ihnen melden."
    )

    mail = current_app.extensions.get('mail')
    mail.send(admin_msg)
    mail.send(user_msg)



class Contact(Resource):
    def post(self):
        user_data = request.json
        admin_email = 'marketmaven.de@gmail.com'  # Setzen Sie hier Ihre Admin-E-Mail-Adresse ein

        try:
            send_email(user_data, admin_email)
            return jsonify(message="E-Mail erfolgreich gesendet.")
        except Exception as e:
            return jsonify(message=f"Fehler beim Senden der E-Mail: {str(e)}"), 500

