from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

import os

username = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
database = os.environ["POSTGRES_DB"]
db_host = os.environ["DB_HOST"]

# PostgreSQL Database setup
DATABASE_URL = f"postgresql://{username}:{password}@{db_host}/{database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    payment_amount = Column(Float)
    coffee_type = Column(String)

Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

# Prometheus metrics
REQUEST_COUNT = Counter("coffee_requests_total", "Total number of coffee requests", ["method", "endpoint"])
TRANSACTION_COUNTER = Counter("coffee_transactions_total", "Total number of coffee transactions", ["coffee_type"])
REQUEST_LATENCY = Histogram("coffee_request_latency_seconds", "Request latency", ["method", "endpoint"])

# Payment model for request
class Payment(BaseModel):
    amount: Decimal

# Function to determine coffee type based on payment
def determine_coffee_type(amount: Decimal) -> str:
    if amount < Decimal('2.00'):
        return "Espresso"
    elif Decimal('2.00') <= amount < Decimal('3.00'):
        return "Latte"
    else:
        return "Cappuccino"

# API endpoint to process payment
@app.post("/buy_coffee/")
def buy_coffee(payment: Payment, request: Request):
    with REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).time():
        coffee_type = determine_coffee_type(payment.amount)
        transaction_id = str(uuid4())
        transaction = Transaction(
            id=transaction_id,
            payment_amount=float(payment.amount),
            coffee_type=coffee_type
        )

        db = SessionLocal()
        db.add(transaction)
        db.commit()
        db.close()

        # Increment metrics
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
        TRANSACTION_COUNTER.labels(coffee_type=coffee_type).inc()

        return {
            "transaction_id": transaction_id,
            "coffee_type": coffee_type,
            "payment_amount": payment.amount
        }

# Endpoint to expose Prometheus metrics
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
