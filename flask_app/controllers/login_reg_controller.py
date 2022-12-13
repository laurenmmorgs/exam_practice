from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



@app.route('/')
def index():
   return render_template('login_reg.html')

@app.route('/register', methods=['POST'])
def register():
   if user.Users.validate_register(request.form):
      pw_hash =bcrypt.generate_password_hash(request.form['password'])
      data = {
         'first_name': request.form['first_name'],
         'last_name': request.form['last_name'],
         'email': request.form['email'],
         'password': pw_hash
      }
      session['user_id'] = user.Users.save(data)
      return redirect('/dashboard')
   return redirect('/')


@app.route('/login', methods = ['POST'])
def login():
   data = { 'email' : request.form['email']}
   user_in_db = user.Users.get_by_email(data)
   if user_in_db:
      if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            session['user_id'] = user_in_db.id
            print(user_in_db.id)
            return redirect('/dashboard')
   flash('Invalid Credentials!', 'loginError')
   return redirect('/')


@app.route('/logout')
def logout():
   print(session)
   session.clear()
   return redirect('/')


