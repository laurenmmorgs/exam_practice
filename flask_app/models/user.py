from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import sighting
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
mydb = 'belt_exam_sasquatch'



class Users:
      def __init__(self, data):
            self.id = data['id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.email = data['email']
            self.password = data['password']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.sightings = []

      @staticmethod
      def validate_register(request):
            is_valid = True # we assume this is true #! I forgot to add this after watching the solution video 
            query = '''
            SELECT * FROM users WHERE email = %(email)s;'''
            results = connectToMySQL(mydb).query_db(query,request)
            if len(results) >=1:
                  flash("Email already taken!", 'regError')
                  is_valid = False
            if len(request['first_name']) < 1:
                  flash("Please Enter A First Name.", 'regError')
                  is_valid = False
            elif len(request['first_name']) < 2:
                  flash("First Name Must Be Longer Than Two Characters", 'regError')
                  is_valid = False
            elif not NAME_REGEX.match(request['first_name']):
                  flash('First Name can only be letters','regError')
                  is_valid = False
            if len(request['last_name']) < 1:
                  flash("Please Enter A Last Name.", 'regError')
                  is_valid = False
            elif len(request['last_name']) < 2:
                  flash("Last Name Must Be Longer Than Two Characters", 'regError')
                  is_valid = False
            elif not NAME_REGEX.match(request['last_name']):
                  flash('Last Name can only be letters','regError')
                  is_valid = False
            if len(request['email']) < 1:
                  flash("Please Enter An Email.", 'regError')
                  is_valid = False
            elif not EMAIL_REGEX.match(request['email']):
                  flash("Please Enter A Valid Email Address", 'regError')
                  is_valid = False
            if len(request['password']) < 1:
                  flash("Please Enter A Password.", 'regError')
                  is_valid = False
            elif len(request['password']) < 9:
                  flash("Password Must Be Longer Than 8 Characters.", 'regError')
                  is_valid = False
            if len(request['pass_conf']) < 1:
                  flash("Please Confirm Your Password.", 'regError')
                  is_valid = False
            elif request['password'] != request['pass_conf']:
                  flash("Passwords Do Not Match.", 'regError')
                  is_valid = False
            return is_valid
            
      @classmethod
      def save(cls,data):
            print(data)
            query='''
            INSERT INTO users 
            (first_name,last_name,email, password, created_at, updated_at)
            VALUES(%(first_name)s,%(last_name)s,%(email)s, %(password)s, NOW(), NOW());'''
            return connectToMySQL(mydb).query_db(query,data)

      @classmethod 
      def get_all(cls):
            query = '''
            SELECT * FROM users;'''
            results = connectToMySQL(mydb).query_db(query)
            output = []
            for users in results:
                  output.append(cls(users))
            return output
      
      @classmethod
      def getByID(cls,data):
            query = '''
            SELECT * 
            FROM users
            WHERE users.id = %(id)s;'''
            results = connectToMySQL(mydb).query_db(query,data)
            return cls(results[0])

      @classmethod
      def get_by_email(cls,data):
            query = '''
            SELECT * FROM users 
            WHERE email = %(email)s'''
            results = connectToMySQL(mydb).query_db(query,data)
            if len(results) < 1:
                  return False
            return cls(results[0])
      
            
      @classmethod
      def get_report_with_creator(cls,data):
            query='''
            SELECT * FROM sightings JOIN users ON sightings.user_id = users.id WHERE sightings.id= %(id)s'''
            results = connectToMySQL(mydb).query_db(query,data)
            one_report = cls(results[0])
            for report in results:
                  one_user_with_report = {
                        'id': report['users.id'],
                        'first_name': report['first_name'],
                        'last_name': report['last_name'],
                        'location': report['location'],
                        'email': report['email'],
                        'password': report['password'],
                        'date': report['date'],
                        'event': report['event'],
                        'user_id': report['user_id'],
                        'num_of_sqatches': report['num_of_sqatches'],
                        'created_at': report['users.created_at'],
                        'updated_at': report['users.updated_at']
                  }
                  one_report.sightings.append(sighting.Sightings(one_user_with_report))
            return one_report
            


