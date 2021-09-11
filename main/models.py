from django.db import models, IntegrityError
from datetime import datetime, date

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['email']) < 4:
            errors["email"] = "El email de usuario debe tener al menos 4 letras"
        if len(postData['password']) < 8:
            errors["password"] = "La contraseña de usuario debe tener al menos 8 letras"
        if postData['password'] != postData['password_check']:
            errors["password"] = "Ambas contraseñas deben ser iguales"
        return errors

class TravelManager(models.Manager):
    def basic_validator(self, postData):
        today = str(date.today())
        errors = {}
        if len(postData['destination']) < 2:
            errors["destination"] = "Destination need to be at least 2 characters in length"
        if len(postData['description']) < 2:
            errors["description"] = "Description need to be at least 2 characters in length"
        if postData['date_from'] < today :
            errors["date_from"] = "Date From need to be at least today"
        if postData['date_to'] < postData['date_from'] :
            errors["date_to"] = "Date To need to be at least same day as Date From  "
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    alllowed = models.BooleanField(default=True)
    avatar = models.URLField(default='https://icon-library.com/images/coder-icon/coder-icon-26.jpg')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    # User Manager 
    objects = UserManager()
    def __str__(self) -> str:
        return f'{self.id} : {self.first_name} {self.last_name}'

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField()
    user = models.ForeignKey(User, related_name="created_travels", on_delete = models.CASCADE)
    travelers = models.ManyToManyField(User, related_name='travels')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    # Travel Manager
    objects = TravelManager()