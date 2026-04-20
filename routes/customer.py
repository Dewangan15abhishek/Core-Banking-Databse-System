from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Customer

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/create_customer", methods=["POST"])
def create_customer():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    db = SessionLocal()
    try:
        customer = Customer(name=name, email=email, phone=phone)
        db.add(customer)
        db.commit()
        return jsonify({"message": "Customer created", "customer_id": customer.customer_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
