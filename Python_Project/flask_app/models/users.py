from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_user( user ):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid


    @staticmethod
    def validate(data):
        is_valid = True

        # TODO add validations here
        if data["password"] != data["confirm_password"]:
            flash("Passwords Must Match!")
            is_valid = False 

        has_special_char = False
        for letter in data["password"]:
            if letter in ["!", "@", "#", "$", "%", "&", "*"]:
                has_special_char = True
        if not has_special_char:
            flash("needs a special character")
            is_valid = False

        
        if len(data["first_name"]) < 2:
            flash(" First Name must be at least 2 characters!")
            is_valid = False


        if len(data["last_name"]) < 2:
            flash(" Last Name must be at least 2 characters!")
            is_valid = False
        
        
        
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"

        user_id = connectToMySQL("python_project").query_db(query, data)

        return user_id

    @classmethod
    def find_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"

        results = connectToMySQL("python_project").query_db(query, data)
        print("results", results)
        if len(results) == 0:
            return False

        one_instance = cls(results[0])
        print(one_instance)
        return one_instance

    @classmethod
    def find_one_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"

        results = connectToMySQL("python_project").query_db(query, data)
        print("results", results)
        if len(results) == 0:
            return False

        one_instance = cls(results[0])
        print(one_instance)
        return one_instance  