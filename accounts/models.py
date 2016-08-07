from __future__ import unicode_literals
from django.db import models
from django.conf import settings

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	cellphone_number = models.IntegerField(blank=True, null=True)
	date_of_birth = models.DateField(blank=True,null=True)
	photo = models.ImageField(upload_to = "user/%Y/%m/%d", blank=True, null=True)

	def __str__(self):
		return 'Perfil del usuario {}'.format(self.user.username)

# Create your models here.
