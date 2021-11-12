from enum import unique
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
import requests
from requests.sessions import session
from sqlalchemy.orm import query
from werkzeug.security import generate_password_hash, check_password_hash
import isbn_loc
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

data = {}


class B_db(db.Model):
  __tablename__ = 'b_db'
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  title = db.Column(db.String(150), nullable=False)
  author = db.Column(db.String(30))
  publisher = db.Column(db.String(50))
  Cagraphy = db.Column(db.String(100))
  isbn = db.Column(db.Integer(), unique=True)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/res_get', methods=['POST', 'GET'])
def get():
  isbn = request.form.get('isbn') 
  if (len(isbn) == 13) or (len(isbn) == 10):
    global data
    data = isbn_loc.bs(isbn)
    return render_template('detail.html', data=data)
  else:
    return render_template('nlb.html')

@app.route('/b', methods=['POST', 'GET'])
def ret ():
    lo_s = B_db(
      title = data.get('t'),
      author = data.get('a'),
      publisher = data.get('p'),
      isbn = data.get('i'),
      Cagraphy= data.get('C')
    )
    try:
      db.session.add(lo_s)
      db.session.commit()
      return redirect('/')
    except Exception as e:
      abort(405)



@app.route('/bookshelf', methods=['POST', 'GET'])
def mybook():
    pop = B_db.query.all()
    return render_template('bookshelf.html', pop=pop)


#DELETE
@app.route('/delete/<int:id>')
def delete(id):
  del_book = B_db.query.get(id)
  db.session.delete(del_book)
  db.session.commit()
  return redirect(url_for('mybook'))



@app.route('/detail/<int:id>')
def detail(id):
  r_book = B_db.query.get(id)
  return render_template('book_detail.html', r_book=r_book)

    

@app.errorhandler(404)
def not_book(error):
  return render_template('nlb.html'), 404


@app.errorhandler(405)
def overlap_book(error):
  return render_template('dfg.html'), 405



if __name__ == '__main__':
  app.run(debug=True)
