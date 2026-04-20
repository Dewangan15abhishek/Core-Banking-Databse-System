from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Account, Transaction
from kafka_producer import publish_transaction
from datetime import datetime

transaction_bp = Blueprint("transaction", __name__)

@transaction_bp.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    account_id = data.get("account_id")
    amount = data.get("amount")

    if not account_id or not amount or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    db = SessionLocal()
    try:
        account = db.query(Account).filter_by(account_id=account_id).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404

        account.balance += amount
        txn = Transaction(to_account=account_id, amount=amount, type="deposit")
        db.add(txn)
        db.commit()
        publish_transaction({
            "type": "deposit",
            "account_id": account_id,
            "amount": amount,
            "timestamp": str(datetime.utcnow())
        })
        return jsonify({"message": "Deposit successful", "new_balance": account.balance}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@transaction_bp.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    account_id = data.get("account_id")
    amount = data.get("amount")

    if not account_id or not amount or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    db = SessionLocal()
    try:
        account = db.query(Account).filter_by(account_id=account_id).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        if account.balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        account.balance -= amount
        txn = Transaction(from_account=account_id, amount=amount, type="withdraw")
        db.add(txn)
        db.commit()
        publish_transaction({
            "type": "withdraw",
            "account_id": account_id,
            "amount": amount,
            "timestamp": str(datetime.utcnow())
        })
        return jsonify({"message": "Withdrawal successful", "new_balance": account.balance}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@transaction_bp.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    from_id = data.get("from_account")
    to_id = data.get("to_account")
    amount = data.get("amount")

    if not from_id or not to_id or not amount or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    db = SessionLocal()
    try:
        sender = db.query(Account).filter_by(account_id=from_id).first()
        receiver = db.query(Account).filter_by(account_id=to_id).first()

        if not sender or not receiver:
            return jsonify({"error": "One or both accounts not found"}), 404
        if sender.balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        sender.balance -= amount
        receiver.balance += amount
        txn = Transaction(from_account=from_id, to_account=to_id, amount=amount, type="transfer")
        db.add(txn)
        db.commit()
        publish_transaction({
            "type": "transfer",
            "from_account": from_id,
            "to_account": to_id,
            "amount": amount,
            "timestamp": str(datetime.utcnow())
        })
        return jsonify({"message": "Transfer successful"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@transaction_bp.route("/ledger/<int:account_id>", methods=["GET"])
def ledger(account_id):
    db = SessionLocal()
    try:
        txns = db.query(Transaction).filter(
            (Transaction.from_account == account_id) | (Transaction.to_account == account_id)
        ).all()
        result = [
            {
                "transaction_id": t.transaction_id,
                "type": t.type,
                "amount": t.amount,
                "from": t.from_account,
                "to": t.to_account,
                "timestamp": str(t.timestamp)
            }
            for t in txns
        ]
        return jsonify(result), 200
    finally:
        db.close()