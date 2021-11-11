import requests
from flask import abort

def isbn_lll(isbn):
  isbn10 = ''
  isbn = 0
  digit = 0 
  isbn10 = isbn[3:12]

  for i in range(len(isbn10)):
    digit += int(isbn10[i]) * (10 - i)

  digit =  11 - digit % 11

  if digit == 11:
    digit = 0
  elif digit == 10:
    digit = 'a'
  else:
    digit = digit

  isbn10 += str(digit)
  return int(isbn10)

def bs(isbn):
    apl = "https://api.openbd.jp/v1/get?isbn="
    result = requests.get(apl + isbn)
    res = result.json()
    #書籍情報が返って来たらdataにぶち込みそれ以外はエラー吐く
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


def change_digit():
  
  return 

        


