from django.db import models

from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True , auto_now_add=False)	#when it updated in the DB
	timestamp = models.DateTimeField(auto_now=False , auto_now_add=True)	#when it first crated in the DB

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id":self.id})

	class Meta:
		ordering = ["-timestamp" , "-updated"]