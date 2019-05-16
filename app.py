import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

db.create_all()


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route("/create")
def create():
    # 1. params로 날라온 데이터를 각각에 저장해주고,
    form_title = request.args.get("title")
    form_content = request.args.get("content")

    # 2. 각각의 내용을 해당하는 데이터베이스 column에 맞게 저장해주면 됩니다.
    post = Post(title=form_title, content=form_content)
    db.session.add(post)

    # 3. 최종적으로 DB에 commit 해주시면 되요.
    db.session.commit()
    return render_template('create.html', title=form_title, content=form_content)

#app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

@app.route("/profile")
def profile():
    return send_file('profile.html')

@app.route("/lotto")
def lotto():
    name = "수달"
    numbers = str(sorted(random.sample(list(range(1,46)),6)))
    return render_template('lotto.html',lotto=numbers, name=name)
    
@app.route("/kospi")
def kospi():
    url = 'https://finance.naver.com/sise/'
    response = requests.get(url).text
    doc = BeautifulSoup(response,'html.parser')
    result=doc.select_one('#KOSPI_now').text
    
    return render_template('kospi.html',kospi=result)

@app.route("/webtoon")
def days():
    week=['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    weekurl=['/webtoon/mon','/webtoon/tue','/webtoon/wed','/webtoon/thu','/webtoon/fri','webtoon/sat','webtoon/sun']
    return render_template('days.html',number=range(0,7),week=week, url=weekurl)

@app.route("/webtoon/wed")
def webtoon():
    url = 'https://m.comic.naver.com/webtoon/weekday.nhn?week=wed'
    response = requests.get(url).text
    names=[]
    imagess=[]
    linking=[]
    web={}
    doc = BeautifulSoup(response, 'html.parser')
    for i in doc.findAll('ul',{'id': 'pageList'}):
        for webtoons in i.findAll('span',{'class': 'toon_name'}):
#           score = webtoons.select_one('.txt_score').text
            names.append(webtoons.text)
            #print(i,': ',webtoons.text)
        for images in i.findAll('span',{'class':'im_br'}):
            links = images.findAll('img')
            for link in links:
                #print(link['src'])
                imagess.append(link['src'])
                #webbrowser.open_new(link['src'])
        for webs in i.findAll('li'):
            webs2 = webs.findAll('a')
            for web3 in webs2:
                linking.append('https://m.comic.naver.com'+web3['href'])
    for i in range(len(names)):
        web[names[i]]=[imagess[i],linking[i]]
    
    #return render_template('webtoon.html',names=names,images=imagess)
    return render_template('webtoon.html',web=web)
    