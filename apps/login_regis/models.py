from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

email_valid = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
name_valid = r'^[a-zA-Z]{2,}$'
pass_valid = r'^[a-zA-Z0-9.+_-]{8,}$'



class UserManager(models.Manager):
    def login(self, logData):
        no_errors = True
        login_errors =[]
        # result = no_errors, login_errors
        try:
            email = User.objects.get(email=logData["email_login"].lower())
            if bcrypt.hashpw(logData["password_login"].encode(), email.password.encode()) == email.password:
                result = no_errors, login_errors, email.id
            else:
                no_errors = False
                login_errors.append("Password does not Match")
                result = no_errors, login_errors


        except:
            no_errors = False
            login_errors.append("User does not exist")
            result = no_errors, login_errors

        return result


    def register(self, postData):
        no_errors = True
        error_messages =[]
        if re.match(email_valid, postData["email"]):
            print "valid email"
            try:
                User.objects.get(email=postData["email"]).email
                no_errors = False
                error_messages.append("Email address already in use")
            except:
                print "New user"
        else:
            no_errors = False
            error_messages.append("Invalid Email Address")    
        if re.match(name_valid, postData["firstname"]):
            print "valid First Name"
        else:
            no_errors = False
            error_messages.append("Invalid First Name, please enter 2 or more Letters")
        if re.match(name_valid, postData["lastname"]):
            print "valid Last Name"
        else:
            no_errors = False
            error_messages.append("Invalid Last Name, please enter 2 or more Letters")
        if re.match(pass_valid, postData["password"]):
            print "valid Password"
        else:
            no_errors = False
            error_messages.append("Invalid Password, please enter 8 or more characters")
        if postData["password"]== postData["confirm"]:
            print "Password Confirmed"
        else:
            no_errors = False
            error_messages.append("Password confirmation did no match")
        if no_errors:
            hashed = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            User.objects.create(first_name=postData["firstname"].lower(), last_name=postData["lastname"].lower(), email=postData["email"].lower(), password=hashed)

        return no_errors, error_messages

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
