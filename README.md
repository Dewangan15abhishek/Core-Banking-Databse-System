# Core Banking Database System

## Overview

This project is a full-stack Core Banking System with a data engineering pipeline. It supports customer management, account operations, and financial transactions, while streaming transaction data through Kafka and performing analytics using PySpark orchestrated by Airflow.

---

## Tech Stack

* **Backend:** Python Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Streaming:** Apache Kafka (KRaft mode)
* **Analytics:** Apache Spark (PySpark)
* **Orchestration:** Apache Airflow
* **Frontend:** HTML, CSS, JavaScript
* **Environment:** Windows 11 + WSL2 (Ubuntu)

---

## Features

* Customer and account management
* Deposit, withdrawal, and transfer operations
* Transaction ledger tracking
* Kafka-based real-time event streaming
* Spark-based transaction analytics (COUNT, SUM, AVG)
* Airflow DAG for pipeline orchestration
* Web dashboard for interaction

---

## Project Structure

```
Data/
│
├── app.py
├── db.py
├── models.py
├── kafka_producer.py
├── kafka_consumer.py
├── spark_analysis.py
├── dashboard.html
├── requirements.txt
├── README.md
│
├── routes/
│   ├── __init__.py
│   ├── account.py
│   ├── customer.py
│   └── transaction.py
│
├── dags/
│   └── banking_pipeline.py
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Start Flask Backend (Windows PowerShell)

```bash
cd C:\Users\KIIT0001\OneDrive\Documents\Data
venv\Scripts\activate
python app.py
```

---

### 3. Start Kafka (WSL)

```bash
cd ~/kafka_2.13-4.2.0
bin/kafka-server-start.sh config/server.properties
```

---

### 4. Start Kafka Consumer

**Option A — Windows**

```bash
cd C:\Users\KIIT0001\OneDrive\Documents\Data
venv\Scripts\activate
python kafka_consumer.py
```

**Option B — WSL**

```bash
cd /mnt/c/Users/KIIT0001/OneDrive/Documents/Data
python3 kafka_consumer.py
```

---

### 5. Run Spark Analytics

```bash
python spark_analysis.py
```

---

### 6. Start Airflow (WSL)

```bash
airflow standalone
```

---

## API Endpoints

| Method | Endpoint         | Description               |
| ------ | ---------------- | ------------------------- |
| POST   | /create_customer | Create new customer       |
| POST   | /create_account  | Create account            |
| POST   | /deposit         | Deposit money             |
| POST   | /withdraw        | Withdraw money            |
| POST   | /transfer        | Transfer between accounts |
| GET    | /ledger/{id}     | Get transaction history   |

---

## Data Pipeline Flow

1. User performs transaction via dashboard
2. Flask processes request and updates PostgreSQL
3. Transaction event sent to Kafka
4. Kafka consumer reads event in real-time
5. Spark processes transaction data
6. Airflow schedules and orchestrates pipeline

---

## Notes

* Kafka runs in KRaft mode (no Zookeeper)
* Airflow must be executed in WSL (Linux environment required)
* Ensure correct IP configuration between Windows and WSL

---

## Author

Abhishek Dewangan
B.Tech CSE
