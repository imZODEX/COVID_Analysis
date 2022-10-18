import email, re
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime
import os

# Create your models here.

class UserManager(models.Manager):

    def register_validator(self, postData):
        errors = {}
        # Validation Rules for First Name
        if len(postData['name']) < 1:
            errors["name"] = "Username is required"
        elif len(postData['email']) < 1:
            errors["email"] = "Email is required"
        elif len(postData['state']) < 1:
            errors["state"] = "State is required"
        # Validation Rules for Password
        elif len(postData['password']) < 1:
            errors["password"] = "Password is required"
        elif not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", postData['email']):
            errors["email"] = "Email should be in correct format"
        elif not re.findall('\d', postData['password']):
            errors["password"] = "Password must contain at least 1 number"
        elif not re.findall('[A-Z]', postData['password']):
            errors["password"] = "Password must contain at least 1 uppercase letter"
        elif not re.findall('[a-z]', postData['password']):
            errors["password"] = "Password must contain at least 1 lowercase letter"   
        elif not re.findall('[!@#&*_]', postData['password']):
            errors["password"] = "Password must contain at least 1 symbol [!@#&*_]"
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        elif postData['email'] in list(Authentications.objects.values_list('email', flat=True)):
            errors["email"] = "Email is already registered"
        

        # Validation Rules for Confirm Password
        elif postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Password and Password Confirmation did not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        # Validation Rules for Login Email
        if len(postData['email']) < 1:
            errors["email"] = "Username is required"

        # Validation Rules for Login Password
        elif len(postData['password']) < 1:
            errors["password"] = "Password is required"
            
        elif postData['email'] not in list(Authentications.objects.values_list('email', flat=True)):
            errors["email"] = "User does not exists"
        else:
            auth = Authentications.objects.get(email=postData['email'])
            
            check_pw = check_password(postData['password'], auth.password)

            if  not check_pw:
                errors["password"] = "Password is not correct"
            elif auth.isApproved == False:
                errors['email'] = "Admin hasnt approved your profile"
            

        return errors

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('covid_data/', filename)

class States(models.Model):
    state_id = models.IntegerField()
    state = models.CharField(primary_key=True ,max_length=50)
    data = models.FileField(upload_to=filepath,null=True)

    def __str__(self):
        return self.state

class Authentications(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=16)
    isApproved = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    state= models.ForeignKey(States,db_column='state', on_delete=models.CASCADE,null=True) 

    objects = UserManager()

    def __str__(self):
        return self.email

