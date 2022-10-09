from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, ride

@app.route("/rides/dashboard")
def dashboard_page():
    if not "user_id" in session:
        return redirect("/")
    user_data = { "id": session["user_id"] }
    this_user = user.User.get_user_by_id(user_data)
    ride_requests = ride.Ride.get_all_ride_requests()
    booked_rides = ride.Ride.get_all_booked_rides()
    return render_template("dashboard_page.html", this_user = this_user,
        all_requests = ride_requests, all_booked_rides = booked_rides)

@app.route("/rides/new")
def new_ride_page():
    if not "user_id" in session:
        return redirect("/")
    return render_template("new_ride_page.html")

@app.route("/rides/add_request", methods=["POST"])
def add_ride_request():
    if not "user_id" in session:
        return redirect("/")

    data = {
        "destination": request.form["destination"],
        "pickup_location": request.form["pickup_location"],
        "date_needed": request.form["date_needed"],
        "details": request.form["details"],
        "rider_id": session["user_id"]
    }

    if not ride.Ride.validate_request(data):
        return redirect("/rides/new")

    ride.Ride.create_ride_request(data)

    return redirect("/rides/dashboard")

@app.route("/rides/add_driver/<int:driver_id>/<int:ride_request_id>")
def add_driver_to_ride(driver_id, ride_request_id):
    data = {
        "driver_id": driver_id,
        "ride_request_id": ride_request_id
    }
    ride.Ride.add_driver_to_ride(data)
    return redirect("/rides/dashboard")

@app.route("/rides/<int:id>")
def view_ride_page(id):
    if not "user_id" in session:
        return redirect("/")
    data = {
        "ride_request_id": id
    }
    user_data = { "id": session["user_id"] }
    this_ride = ride.Ride.get_booked_ride(data)
    return render_template("view_ride_page.html", this_user = user.User.get_user_by_id(user_data), this_ride = this_ride)

@app.route("/rides/edit/<int:id>")
def edit_ride_page(id):
    if not "user_id" in session:
        return redirect("/")
    data = { "id": id }
    this_request = ride.Ride.get_request_by_id(data)
    return render_template("edit_ride_page.html", this_request = this_request)

@app.route("/rides/update/<int:id>", methods=["POST"])
def update_ride(id):
    if not "user_id" in session:
        return redirect("/")
    data = {
        "id": id,
        "pickup_location": request.form["pickup_location"],
        "details": request.form["details"]
    }
    if not ride.Ride.validate_update_request(data):
        return redirect(f"/rides/edit/{ id }")
    ride.Ride.update_ride_request(data)
    return redirect("/rides/dashboard")

@app.route("/rides/delete/<int:id>")
def delete_ride_request(id):
    if not "user_id" in session:
        return redirect("/")
    data = { "id": id }
    ride.Ride.delete_ride_request(data)
    return redirect("/rides/dashboard")

@app.route("/rides/cancel/<int:id>")
def cancel_booked_ride(id):
    if not "user_id" in session:
        return redirect("/")
    data = { "ride_request_id": id}
    ride.Ride.cancel_booked_ride(data)
    return redirect("/rides/dashboard")

@app.route("/rides/delete_booked_ride/<int:id>")
def delete_booked_ride(id):
    if not "user_id" in session:
        return redirect("/")
    data = { "ride_request_id": id}
    ride.Ride.delete_booked_ride(data)
    return redirect("/rides/dashboard")