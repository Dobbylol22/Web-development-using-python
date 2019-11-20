from flask import Flask ,render_template,redirect,url_for,request,flash
from db_setup import Owner,Item,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker,scoped_session)
from flask import session as login_session
from functools import wraps
engine=create_engine('sqlite:///mydb.db')
Base.metadata.bind=engine
session=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)
def login_required(f):
	@wraps(f)
	def x(*args,**kwargs):
		if 'email' not in login_session:
			return redirect(url_for('login'))
		return f(*args,**kwargs)
	return x


# @app.route('/hello/<name>')
# def name(name):
# 	return ("<h1><i>welcome to "+name+"</i></h1>")
# @app.route('/Myname/<name1>/<rollno>')
# def Myname(name1,rollno):
# 	return ("<h1><i>My name is "+name1+"<br>My rollno is "+rollno+"</i></h1>")
# @app.route('/Mynames/<name1>/<rollno>')
# def Mynames(name1,rollno):
# 	return ("<h1><i>hello! %s"%name1+""+"<br>Your rollno is %s"%rollno+""+"</i></h1>")
# @app.route('/Adds/<int:num1>/<int:num2>')
# def Adds(num1,num2):
# 	num1=num1+num2
# 	return ("<h1><i>Addition of two numbers {}:</i></h1>".format(num1))
# @app.route('/Add/<int:num1>/<int:num2>')
# def Add(num1,num2):
# 	num1=num1+num2
# 	return ("<h1><i>Addition of two numbers %d:" % num1+""+"</i></h1>")
# @app.route('/')
# def sample():
# 	return render_template('index.html')
# @app.route('/message/<name>')
# def mess(name):
# 	return render_template('message.html',name=name)
# @app.route('/fl/<fname>/<lname>')
# def flnam(fname,lname):
# 	return render_template('fnamelname.html',fname=fname,lname=lname)
# @app.route('/for/<int:lower>/<int:upper>')
# def forloop(lower,upper):
# 	return render_template('for.html',lower=lower,upper=upper)	
# @app.route('/admin/<name>')
# def admin_name(name):
# 	return 'hey this is %s' %name
# @app.route('/guest/<name>')
# def guest_name(name):
# 	return '%s is a guest' %name
# @app.route('/user')
# def user(user):
# 	if user==admin_name:
# 		return redirect(url_for(user))
# 	else:
# 		return redirect(url_for(guest_name))
# @app.route('/Multi/<int:n>/<int:m>')
# def multi(n,m):
# 	return render_template('Multi.html',n=n,m=m)
# @app.route('/leap/<int:l>/<int:m>')
# def leap(l,m):
# 	return render_template('leap.html',l=l,m=m)
# @app.route('/EorO/<int:l>')
# def evenorodd(l):
# 	lst=[]
# 	for i in range(l):
# 		lst.append(i)
# 	return render_template('eoro.html',l=lst)
# @app.route('/table/<int:row>/<int:col>')
# def table(row,col):
# 	lst1=[]
# 	n=1;
# 	for i in range(1,row+1):
# 		lst2=[]
# 		for j in range(1,col+1):
# 			lst2.append(n)
# 			n=n+1
# 		lst1.append(lst2)	
# 	return render_template('table.html',lst1=lst1,row=row,col=col)
@app.route('/')
def home():
	items=session.query(Item).all()
	return render_template('items.html',items=items)
	# return render_template('home.html')
@app.route('/register',methods=['POST','GET'])
def register():
	if request.method=="POST":
		name=request.form['name']
		email=request.form['email']
		password=request.form['pass']
		owner=Owner(name=name,email=email,password=password)
		session.add(owner)
		session.commit()
		flash('Successfully register','success')
	return render_template('register.html')
@app.route('/newitem',methods=['POST','GET'])
@login_required
def newitem():

	if request.method=="POST":
		brandname=request.form['brandname']
		image=request.form['image']
		model=request.form['model']
		cost=request.form['cost']
		description=request.form['desc']
		owner_id=1
		item=Item(brandname=brandname,image=image,model=model,cost=cost,description=description,owner_id=owner_id)
		session.add(item)
		session.commit()
		flash('Successfully added','success')
	return render_template('newitem.html')
@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=="POST":
		email=request.form['email']
		password=request.form['pass']
		owner=session.query(Owner).filter_by(email=email,password=password).one_or_none()
		if owner==None:
			flash("Invalid Credentials.........",'danger')
			return redirect(url_for('login'))
		login_session['email']=email
		login_session['name']=owner.name
		flash('welcome'+str(owner.name),'success')
		return redirect(url_for('home'))
	return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
	del login_session['email']
	del login_session['name']
	flash('Successfully logout thank you visit again......','success')
	return redirect(url_for('home'))
@app.route('/Item/<int:item_id>/edit',methods=['POST','GET'])
@login_required
def edititem(item_id):
	if request.method=="POST":
		brandname=request.form['brandname']
		image=request.form['image']
		model=request.form['model']
		cost=request.form['cost']
		description=request.form['desc']
		item=session.query(Item).filter_by(id=item_id).one_or_none()
		item.brandname=brandname
		item.image=image
		item.model=model
		item.cost=cost
		item.description=description
		session.add(item)
		session.commit()
		flash ('Successfully updated!!!','success')
		return render_template('items.html')
	else:
	    item=session.query(Item).filter_by(id=item_id).one_or_none()
	    return render_template("update.html",item=item)  
@app.route('/Item/<int:item_id>/delete')
@login_required
def deleteitem(item_id):
	item=session.query(Item).filter_by(id=item_id).one_or_none()
	session.delete(item)
	session.commit()
	flash("Item is deleted!!","danger")
	return render_template('home.html')
#always last
if __name__=='__main__':
	app.secret_key='123asdfaw'
	app.run(debug=True,port=5000,host="localhost")

 