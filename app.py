from enum import unique
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

data = {}
#dbの設定
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
    data = bs(isbn)
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
#一覧表示
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
#詳細表示
@app.route('/detail/<int:id>')
def detail(id):
  r_book = b_db.query.get(id)
  return render_template('book_detail.html', r_book=r_book)

#ISBNから書籍情報を取得する
def bs(isbn):
  
    apl = "https://api.openbd.jp/v1/get?isbn="
    result = requests.get(apl + isbn)
    res = result.json()
    #openBDから書籍情報が返って来たらdataにぶち込みそれ以外はエラー吐く
    try:
      data = {
        'i':(res[0]["summary"]["isbn"]),
        't':(res[0]["summary"]["title"]),
        'a':(res[0]["summary"]["author"]),
        'p':(res[0]["summary"]["publisher"]),
        'C':(res[0]["summary"]["cover"])
        }
      return data
    except Exception as e:
      abort(404)
        

@app.errorhandler(404)
def page_not_found(error):
  return render_template('nlb.html'), 404



if __name__ == '__main__':
  app.run()
