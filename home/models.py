from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class myuser (models.Model):
    Username = models.CharField ( max_length = 30, primary_key=True)
    Email = models.EmailField ( max_length = 50)
    Password = models.CharField ( max_length = 20 )
    FirstName = models.CharField ( max_length = 20, default="" )
    LastName = models.CharField ( max_length = 20, default="")
    vfmail = models.BooleanField ( default = False )
    history = models.TextField( default = None, null=True , blank = True )

    def __str__( self ) :
        return str ( self . Username )

