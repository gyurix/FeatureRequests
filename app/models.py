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
    area = Column('area', Integer)
    poster = Column('poster', Integer)
    created = Column('created', DateTime)
    __table__ = Table('requests', meta, id, title, desc, client, priority, date, area, poster, created)

    def __init__(self, poster, title, desc, client, priority, date, area):
        self.poster = poster
        self.title = title
        self.desc = desc
        self.client = client
        self.priority = priority
        self.date = date
        self.area = area


class Role(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String, nullable=False)
    enabled = Column('enabled', Boolean)
    view = Column('view', Boolean)
    add = Column('add', Boolean)
    edit = Column('edit', Boolean)
    admin = Column('admin', Boolean)
    __table__ = Table('roles', meta, id, name, enabled, view, add, edit, admin)

    def __init__(self, enabled, view, add, edit, admin):
        self.enabled = enabled
        self.view = view
        self.add = add
        self.edit = edit
        self.admin = admin


class Client(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    __table__ = Table('clients', meta, id, name)

    def __init__(self, name):
        self.name = name


class Production(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    __table__ = Table('productions', meta, id, name)

    def __init__(self, name):
        self.name = name


class User(db.Model):
    id = Column('id', Integer, autoincrement=True, unique=True, primary_key=True)
    name = Column('name', String)
    email = Column('email', String, unique=True)
    password = Column('password', String)
    role = Column('role', Integer, default=0)
    __table__ = Table('users', meta, id, name, email, password, role)

    def __init__(self, username, email, password):
        self.name = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(password, self.password)
