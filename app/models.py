from datetime import datetime

from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, Table, Date, Boolean, DateTime, MetaData
from werkzeug.security import check_password_hash, generate_password_hash

meta = MetaData()
db = SQLAlchemy(metadata=meta)


class Request(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    title = Column('title', String)
    desc = Column('desc', String)
    client = Column('client', Integer)
    priority = Column('priority', Integer)
    date = Column('date', Date)
    production = Column('production', Integer)
    poster = Column('poster', Integer)
    created = Column('created', DateTime, default=datetime.now().replace(microsecond=0))
    __table__ = Table('requests', meta, id, title, desc, client, priority, date, production, poster, created)

    def __init__(self):
        super(Request, self).__init__()
        self.poster = session['user']


class Role(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String, nullable=False)
    enabled = Column('enabled', Boolean)
    view = Column('view', Boolean)
    add = Column('add', Boolean)
    edit = Column('edit', Boolean)
    admin = Column('admin', Boolean)
    __table__ = Table('roles', meta, id, name, enabled, view, add, edit, admin)


class Client(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    __table__ = Table('clients', meta, id, name)


class Production(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    __table__ = Table('productions', meta, id, name)


class User(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    email = Column('email', String, unique=True)
    password = Column('password', String)
    role = Column('role', Integer, default=1)
    __table__ = Table('users', meta, id, name, email, password, role)

    def __init__(self):
        super(User, self).__init__()
        self.role = 1

    def set_username(self, username):
        self.name = username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_role(self):
        from app.data_manager import load_role
        return load_role(self.role)

    def has_permission(self, permission):
        role = self.get_role()
        if role is None:
            return self.id == 1
        return getattr(role, permission)
