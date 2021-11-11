from enum import unique
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import isbn_loc
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

data = {}


class b_db(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement = True)
  title = db.Column(db.String(150), nullable=False)
  author = db.Column(db.String(30))
  publisher = db.Column(db.String(50))
  Cagraphy = db.Column(db.String(100))
  isbn = db.Column(db.Integer())



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
  lo_s = b_db(
    title = data.get('t'),
    author = data.get('a'),
    publisher = data.get('p'),
    isbn = data.get('i'),
    Cagraphy= data.get('C')
  )
  db.session.add(lo_s)
  db.session.commit()
  return redirect('/')



@app.route('/bookshelf', methods=['POST', 'GET'])
def mybook():
    pop = b_db.query.all()
    return render_template('bookshelf.html', pop=pop)


#DELETE
@app.route('/delete/<int:id>')
def delete(id):
  del_book = b_db.query.get(id)
  db.session.delete(del_book)
  db.session.commit()
  return redirect(url_for('mybook'))



@app.route('/detail/<int:id>')
def detail(id):
  r_book = b_db.query.get(id)
  return render_template('book_detail.html', r_book=r_book)

    

@app.errorhandler(404)
def page_not_found(error):
  return render_template('nlb.html'), 404




@app.route('/change_isbn', methods=['POST', 'GET'])
def change_isbn():
  number = request.form.get('isbn13')
  number = isbn_loc.isbn_lll(number)
  return render_template('index.html', number=number) 



if __name__ == '__main__':
  app.run(debug=True)
