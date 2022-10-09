from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    db_name = "rideshare_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_new_user(user_data):
        is_valid = True
        if len(user_data["first_name"]) < 2 or not user_data["first_name"].isalpha():
            flash("First name must be at least 2 characters and may only contain letters.", "register")
            is_valid = False
        if len(user_data["last_name"]) < 2  or not user_data["last_name"].isalpha():
            flash("Last name must be at least 2 characters and may only contain letters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user_data["email"]):
            flash("Invalid email.", "register")
            is_valid = False
        if User.get_user_by_email(user_data):
            flash("Email is already in use!", "register")
            is_valid = False
        if user_data["password"] != user_data["confirm_password"]:
            flash("Passwords must match.", "register")
            is_valid = False
        if len(user_data["password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if not re.findall("[A-Z]", user_data["password"]):
            flash("Password must have at least one capital letter.", "register")
            is_valid = False
        if not re.findall("[0-9]", user_data["password"]):
            flash("Password must have at least one number", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_existing_user(user_data):
        found_user_or_none = User.get_user_by_email(user_data)
        if not found_user_or_none:
            flash("Invalid email/password.", "login")
            return False
        if not bcrypt.check_password_hash(found_user_or_none.password, user_data["password"]):
            flash("Invalid email/password.", "login")
            return False
        return True

    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])