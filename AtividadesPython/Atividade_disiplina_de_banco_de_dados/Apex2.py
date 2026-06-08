from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://faculdade:h8x1e0k7@localhost:3306/sistema_gestao-escolar"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)


