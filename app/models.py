from . import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Numeric
from flask import current_app
from werkzeug.utils import secure_filename
import os
from PIL import Image
import re
from twilio.rest import Client
from flask_mail import Mail, Message
import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError, ClientError
from flask_login import UserMixin

# Tenant Model (Added)
class Tenant(db.Model):
    __tablename__ = 'tenants'  # Specify table name if it's different
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500), nullable=True)
    country = db.Column(db.String(150), nullable=True)
    state = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='tenant', lazy=True)  # Link with User model
    donations = db.relationship('Donation', backref='tenant', lazy=True)  # Link with Donation model
    pledges = db.relationship('Pledge', backref='tenant', lazy=True)  # Link with Pledge model
    attendances = db.relationship('Attendance', backref='tenant', lazy=True)  # Link with Attendance model
    invoices = db.relationship('Invoice', backref='tenant', lazy=True)  # Link with Invoice model

# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(500), nullable=True)
    country = db.Column(db.String(150))
    state = db.Column(db.String(150), nullable=True)
    church_branch = db.Column(db.String(150))
    birthday = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pledged_amount = db.Column(db.Float, default=0.0)
    pledge_currency = db.Column(db.String(3), default="USD")
    paid_status = db.Column(db.Boolean, default=False)
    medal = db.Column(db.String(100), nullable=True)
    partner_since = db.Column(db.Integer, nullable=True)
    donation_date = db.Column(db.Date, nullable=False, default=date.today)
    has_received_onboarding_email = db.Column(db.Boolean, default=False)
    has_received_onboarding_sms = db.Column(db.Boolean, default=False)

    # Relationships
    pledges = db.relationship('Pledge', back_populates='donor', cascade="all, delete-orphan")
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))  # Tenant relationship

    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)
    

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Multi-tenancy linkage
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"



class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Multi-tenancy linkage
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(50), default='USD')
    donation_date = db.Column(db.Date, nullable=False, default=date.today)
    payment_type = db.Column(db.String(20), nullable=False, default="full")
    receipt_filename = db.Column(db.String(255), nullable=True)
    amount_paid = db.Column(db.Float, nullable=False, default=0)
    pledged_amount = db.Column(db.Float, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    paid_status = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="donations")
    medal = db.Column(db.String(50))


class Pledge(db.Model):
    __tablename__ = 'pledges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Multi-tenancy linkage
    pledged_amount = db.Column(db.Numeric)
    pledge_currency = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    donor = db.relationship('User', back_populates='pledges')

    

# Attendance Model
class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Multi-tenancy linkage
    student_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)


# Invoice Model
class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)  # Multi-tenancy linkage
    customer_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, server_default=db.func.now())
