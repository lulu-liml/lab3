import bottle
from bottle import run, route, template, static_file, redirect, request
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
from beaker.middleware import SessionMiddleware
from collections import OrderedDict
import redis
import json
from bottle import error

print ("Start running server.py. Please make sure you have redis server started.")
    
# the record dict is used to store top 20 most popular keywords
record = OrderedDict()
user_email = ''
page_num = 1
keywords = ""

# lab2
session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': True,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

# lab3
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0) #connect to redis database
page_rank = redis_db.get('page_rank') #page rank result - page_rank[url_id] = score
inverted_index = redis_db.get('inverted_index') # word_id & its set of url_id -inverted_index[word_id]=set_of(url_ids)
resolved_inverted_index =redis_db.get('resolved_inverted_index') # word & its set of url-resolved_inverted_index[word]=set_of(urls)
lexicon = redis_db.get('url_id_lexicon') # lexicon[url]=url_id

# convert data from str to dict
page_rank = json.loads(page_rank)
inverted_index = json.loads(inverted_index)
resolved_inverted_index = json.loads(resolved_inverted_index)
lexicon = json.loads(lexicon)

def getUserEmail(credentials):
    token = credentials.id_token['sub']
        
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute() 
    user_email = user_document['email']
    return user_email
 
@error(404)
def error404(error):
    return template('error') 
    
@route('/change_page',method='POST')
def decide_page_num():
    global page_num,keywords
    new_page_num = request.forms.get('page_num')
    if new_page_num == "prev":
        page_num = int(page_num)-1
    elif new_page_num == "next":
        page_num = int(page_num)+1
    else:
        page_num = int(new_page_num)     
    return template('index',keywords=keywords,record=record, user_email=user_email,resolved_inverted_index=resolved_inverted_index, lexicon=lexicon,page_rank=page_rank,page_num=page_num)
          
@route('/',method='GET')
def index():
    global user_email,record
    session = bottle.request.environ.get('beaker.session')
    if user_email:
        record = session[user_email]
    else:
        record = OrderedDict()
        
    return template('index',keywords='',record=record,  user_email=user_email)

@route('/login_step1',method='POST')
def login_step1():
    return template('login')
    
@route('/login_step2',method='POST')
def login_step2():
    global user_email,record
    
    user_email = request.forms.get('email')
    session = bottle.request.environ.get('beaker.session')
    if  user_email not in session:
        flow = flow_from_clientsecrets("client_secret_236907109154-1us7tahjvssjcmtfk3orivipcjr4lult.apps.googleusercontent.com.json",scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri="http://localhost:80/redirect")
        auth_uri = flow.step1_get_authorize_url()
        bottle.redirect(str(auth_uri))
    else:
        record = session[user_email]
        return template('index',keywords='',record=record, user_email=user_email)
        

@route('/logout',method='POST')
def logout():
    global user_email
    user_email = ''
    record = OrderedDict()
    redirect("/")
    
    
@route('/redirect')
def redirect_page():
    global user_email,record
    CLIENT_ID = '236907109154-1us7tahjvssjcmtfk3orivipcjr4lult.apps.googleusercontent.com'
    CLIENT_SECRET = 'mvAagtXMQyUTMS0EMkTRhsOM'
    SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
    REDIRECT_URI = 'http://localhost:80/redirect'
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=SCOPE,redirect_uri=REDIRECT_URI)        
    credentials = flow.step2_exchange(code)
    
    session = bottle.request.environ.get('beaker.session')
    session[user_email] = OrderedDict()
    record = session[user_email]
    
    return template('index',keywords='',record=record, user_email=user_email)
# the route to load the logo image
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename,root='./static_file')
    
@route('/',method='POST')
def result():
    global user_email,record,keywords,page_num
    session = bottle.request.environ.get('beaker.session')
    if user_email in session:
        session[user_email]=record
    else:
        record = OrderedDict()
    keywords = request.forms.get('keywords')
    page_num = 1
    return template('index',keywords=keywords,record=record, user_email=user_email,resolved_inverted_index=resolved_inverted_index, lexicon=lexicon,page_rank=page_rank,page_num=page_num)

run(app=app, host='0.0.0.0', port=80)
