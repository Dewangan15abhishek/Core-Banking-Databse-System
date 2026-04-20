from flask import Flask
from flask_cors import CORS
from db import Base, engine
from routes.customer import customer_bp
from routes.account import account_bp
from routes.transaction import transaction_bp

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)

app.register_blueprint(customer_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)