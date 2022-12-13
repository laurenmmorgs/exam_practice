from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
mydb = 'belt_exam_sasquatch'




class Sightings:
   def __init__(self, data):
      self.id = data['id']
      self.location = data['location']
      self.date = data['date']
      self.num_of_sqatches =data['num_of_sqatches']
      self.event = data['event']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']
      self.creator = None
   def full_name(self):
      return f"{self.first_name} {self.last_name}"


   @staticmethod
   def validate_report(request):
         is_valid = True # we assume this is true #! I forgot to add this after watching the solution video 
         if len(request['location']) < 1:
               flash("Please Enter A Location.")
               is_valid = False
         if len(request['event']) < 1:
               flash("Please Enter What Happened")
               is_valid = False
         if len(request['date']) < 1:
            flash("Please Enter A Date")
            is_valid = False
         if len(request['num_of_sqatches']) < 1:
            flash("Please Enter Number")
            is_valid = False
         return is_valid
   
   @classmethod
   def save(cls,data):
         print(data)
         query='''
         INSERT INTO sightings 
         (location,event,date, num_of_sqatches, user_id ,created_at, updated_at)
         VALUES(%(location)s,%(event)s,%(date)s, %(num_of_sqatches)s,  %(user_id)s, NOW(), NOW());'''
         return connectToMySQL(mydb).query_db(query,data)
         
   @classmethod
   def get_reports_with_users(cls):
      query='''
      SELECT * FROM sightings 
      JOIN users ON sightings.user_id = users.id;'''
      results = connectToMySQL(mydb).query_db(query)
      all_sightings =[]
      for sightings in results:
         one_sighting = cls(sightings)
         one_sighting_creators_info = {
            'id': sightings['users.id'],
            'first_name': sightings['first_name'],
            'last_name': sightings['last_name'],
            'location': sightings['location'],
            'email': sightings['email'],
            'password': sightings['password'],
            'date': sightings['date'],
            'event': sightings['event'],
            'user_id': sightings['user_id'],
            'num_of_sqatches': sightings['num_of_sqatches'],
            'created_at': sightings['users.created_at'],
            'updated_at': sightings['users.updated_at']
         }
         author = user.Users(one_sighting_creators_info)
         one_sighting.creator = author
         all_sightings.append(one_sighting)
      return all_sightings


   @classmethod
   def deleteById(cls, data):
         query = '''
         DELETE FROM sightings  
         WHERE id =(%(id)s);'''
         results = connectToMySQL(mydb).query_db(query,data)
   

   @classmethod
   def getByID(cls,data):
         query = '''
         SELECT * 
         FROM sightings
         WHERE id = %(id)s;'''
         results = connectToMySQL(mydb).query_db(query,data)
         return cls(results[0])
   @classmethod
   def edit(cls,data):
         query = '''
         UPDATE sightings
         SET
         location=%(location)s,
         event=%(event)s, date=%(date)s, num_of_sqatches=%(num_of_sqatches)s
         WHERE id=%(id)s;'''
         connectToMySQL(mydb).query_db(query,data)
