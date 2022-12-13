from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models import user, sighting
from datetime import datetime
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
dateFormat = "%B %d %Y"
dateFormat_dashboard = "%m/%d/%Y"




@app.route('/dashboard')
def dashboard():
   if 'user_id' not in session:
      return redirect('/')
   data = {
         'id': session['user_id']
   }
   return render_template('dashboard.html', current_user = user.Users.getByID(data), sightings = sighting.Sightings.get_reports_with_users(), dates = dateFormat_dashboard)



@app.route('/new/sighting')
def new_sighting():
   if 'user_id' not in session:
      return redirect('/')
   data = {
         'id': session['user_id']
   }
   return render_template('new_report.html', current_user = user.Users.getByID(data))


@app.route('/sightings/new', methods=['POST'])
def reporting_sighting():
   print(request.form)
   if sighting.Sightings.validate_report(request.form):
      print(request.form)
      data = {
         'location': request.form['location'],
         'event': request.form['event'],
         'date': request.form['date'],
         'num_of_sqatches': request.form['num_of_sqatches'],
         'user_id': session['user_id']
      }
      sighting.Sightings.save(data)
      return redirect('/dashboard')
   return redirect('/new/sighting')


@app.route('/delete/<int:sighting_id>')
def destroy_sighting(sighting_id):
   sighting.Sightings.deleteById({'id':sighting_id})
   return redirect('/dashboard')



@app.route('/edit/<int:sightings_id>', methods=['POST'])
def editing_sighting(sightings_id):
   if sighting.Sightings.validate_report(request.form):
      data = {
         'location': request.form['location'],
         "event": request.form['event'], 
         "date": request.form['date'],
         'num_of_sqatches' : request.form['num_of_sqatches'],
         'id': sightings_id
      }
      sighting.Sightings.edit(data)
      return redirect('/dashboard')
   return redirect(f'/edit/{sightings_id}')


@app.route('/edit/<int:sighting_id>')
def edit_page(sighting_id):
   if 'user_id' not in session:
      return redirect('/')
   data = {
         'id': session['user_id']
   }
   return render_template('edit_report.html', sighting = sighting.Sightings.getByID({'id': sighting_id}), current_user = user.Users.getByID(data))


@app.route('/show/<int:sighting_id>')
def view_report(sighting_id):
   if 'user_id' not in session:
      return redirect('/')
   data = {
      'id': session['user_id']
   }
   return render_template('view_report.html', current_user = user.Users.getByID(data),sightings = user.Users.get_report_with_creator({'id':sighting_id}), sighting = sighting.Sightings.getByID({'id': sighting_id})  , dates = dateFormat)