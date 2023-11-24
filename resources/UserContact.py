from flask import Flask, request
from flask_restful import Resource, Api

class Contact(Resource):
    def post(self):
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        address = data.get('address')
        country = data.get('country')
        password = data.get('password')

        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Email: {email}")
        print(f"Phone Number: {phone_number}")
        print(f"Address: {address}")
        print(f"Country: {country}")
        print(f"Password: {password}")

        return {'message': 'Data received', 'data': data}, 200
