from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Account

account_bp = Blueprint("account", __name__)

@account_bp.route("/create_account", methods=["POST"])
def create_account():
    data = request.get_json()
    customer_id = data.get("customer_id")
    account_type = data.get("account_type", "savings")

    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    db = SessionLocal()
    try:
        account = Account(customer_id=customer_id, balance=0.0, account_type=account_type)
        db.add(account)
        db.commit()
        return jsonify({"message": "Account created", "account_id": account.account_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()