from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Ride:

    db_name = "rideshare_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.destination = data["destination"]
        self.date_needed = data["date_needed"]
        self.details = data["details"]
        self.pickup_location = data["pickup_location"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.rider = None
        self.driver = None

    @staticmethod
    def validate_request(data):
        is_valid = True
        if len(data["destination"]) < 3:
            flash("Destination must be at least 3 characters.", "request")
            is_valid = False
        if len(data["pickup_location"]) < 3:
            flash("Pick-up location must be at least 3 characters.", "request")
            is_valid = False
        if len(data["details"]) < 10:
            flash("Details must be at least 10 characters.", "request")
            is_valid = False
        if len(data["date_needed"]) < 1:
            flash("Rideshare date must not be blank.", "request")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update_request(data):
        is_valid = True
        if len(data["pickup_location"]) < 3:
            flash("Pick-up location must be at least 3 characters.", "request")
            is_valid = False
        if len(data["details"]) < 10:
            flash("Details must be at least 10 characters.", "request")
            is_valid = False
        return is_valid

    @classmethod
    def create_ride_request(cls, data):
        query = """
        INSERT INTO ride_requests
        (destination, date_needed, pickup_location, details, rider_id)
        VALUES (%(destination)s, %(date_needed)s, %(pickup_location)s, 
        %(details)s, %(rider_id)s)
        ;"""
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_ride_requests(cls):
        query = """
        SELECT * FROM ride_requests
        JOIN users as riders ON riders.id = ride_requests.rider_id
        WHERE ride_requests.id NOT IN (
            SELECT ride_request_id FROM booked_rides
        );
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if len(results) == 0:
            return []
        rides_list = []
        for ride_dictionary in results:
            ride_obj = cls(ride_dictionary)
            rider_data = {
                "id": ride_dictionary["riders.id"],
                "first_name": ride_dictionary["first_name"],
                "last_name": ride_dictionary["last_name"],
                "email": ride_dictionary["email"],
                "password": ride_dictionary["password"],
                "created_at": ride_dictionary["riders.created_at"],
                "updated_at": ride_dictionary["riders.updated_at"]
            }
            rider_obj = user.User(rider_data)
            ride_obj.rider = rider_obj
            rides_list.append(ride_obj)
        return rides_list

    @classmethod
    def get_all_booked_rides(cls):
        query = """
        SELECT * FROM booked_rides
        JOIN users AS drivers ON booked_rides.driver_id = drivers.id
        JOIN ride_requests ON booked_rides.ride_request_id = ride_requests.id
        JOIN users AS riders ON ride_requests.rider_id = riders.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if len(results) == 0:
            return []
        rides_list = []
        for ride_dictionary in results:
            ride_data = {
                "id": ride_dictionary["ride_requests.id"],
                "destination": ride_dictionary["destination"],
                "date_needed": ride_dictionary["date_needed"],
                "details": ride_dictionary["details"],
                "pickup_location": ride_dictionary["pickup_location"],
                "created_at": ride_dictionary["ride_requests.created_at"],
                "updated_at": ride_dictionary["ride_requests.updated_at"]
            }
            ride_obj = cls(ride_data)
            rider_data = {
                "id": ride_dictionary["riders.id"],
                "first_name": ride_dictionary["riders.first_name"],
                "last_name": ride_dictionary["riders.last_name"],
                "email": ride_dictionary["riders.email"],
                "password": ride_dictionary["riders.password"],
                "created_at": ride_dictionary["riders.created_at"],
                "updated_at": ride_dictionary["riders.updated_at"]
            }
            rider_obj = user.User(rider_data)
            ride_obj.rider = rider_obj

            driver_data = {
                "id": ride_dictionary["drivers.id"],
                "first_name": ride_dictionary["first_name"],
                "last_name": ride_dictionary["last_name"],
                "email": ride_dictionary["email"],
                "password": ride_dictionary["password"],
                "created_at": ride_dictionary["drivers.created_at"],
                "updated_at": ride_dictionary["drivers.updated_at"]
            }
            driver_obj = user.User(driver_data)
            ride_obj.driver = driver_obj
            rides_list.append(ride_obj)
        return rides_list

    @classmethod
    def get_booked_ride(cls, data):
        query = """
        SELECT * FROM booked_rides
        JOIN users AS drivers ON booked_rides.driver_id = drivers.id
        JOIN ride_requests ON booked_rides.ride_request_id = ride_requests.id
        JOIN users AS riders ON ride_requests.rider_id = riders.id
        WHERE ride_request_id = %(ride_request_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        ride_dictionary = results[0]
        ride_data = {
            "id": ride_dictionary["ride_requests.id"],
            "destination": ride_dictionary["destination"],
            "date_needed": ride_dictionary["date_needed"],
            "details": ride_dictionary["details"],
            "pickup_location": ride_dictionary["pickup_location"],
            "created_at": ride_dictionary["ride_requests.created_at"],
            "updated_at": ride_dictionary["ride_requests.updated_at"]
        }
        ride_obj = cls(ride_data)
        driver_data = {
            "id": ride_dictionary["drivers.id"],
            "first_name": ride_dictionary["first_name"],
            "last_name": ride_dictionary["last_name"],
            "email": ride_dictionary["email"],
            "password": ride_dictionary["password"],
            "created_at": ride_dictionary["drivers.created_at"],
            "updated_at": ride_dictionary["drivers.updated_at"]
        }
        driver_obj = user.User(driver_data)
        ride_obj.driver = driver_obj
        rider_data = {
            "id": ride_dictionary["riders.id"],
            "first_name": ride_dictionary["riders.first_name"],
            "last_name": ride_dictionary["riders.last_name"],
            "email": ride_dictionary["riders.email"],
            "password": ride_dictionary["riders.password"],
            "created_at": ride_dictionary["riders.created_at"],
            "updated_at": ride_dictionary["riders.updated_at"]
        }
        rider_obj = user.User(rider_data)
        ride_obj.rider = rider_obj
        
        return ride_obj

    @classmethod
    def add_driver_to_ride(cls, data):
        query = """
        INSERT INTO booked_rides
        (driver_id, ride_request_id)
        VALUES (%(driver_id)s, %(ride_request_id)s)
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_request_by_id(cls, data):
        query = "SELECT * FROM ride_requests WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])

    @classmethod
    def update_ride_request(cls, data):
        query = """
        UPDATE ride_requests
        SET pickup_location = %(pickup_location)s,
        details = %(details)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_ride_request(cls, data):
        query = "DELETE FROM ride_requests WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_booked_ride(cls, data):
        query = "DELETE FROM ride_requests WHERE ride_request_id = %(ride_request_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def cancel_booked_ride(cls, data):
        query = "DELETE FROM booked_rides WHERE ride_request_id = %(ride_request_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)