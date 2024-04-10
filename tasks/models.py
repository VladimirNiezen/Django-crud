from django.db import models
from  django.contrib.auth.models import User
import re

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add = True)
    datacompleted = models.DateTimeField(null=True, blank = True)
    important = models.BooleanField(default=False)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by ' + self.user.username
    
    def title_is_duplicated (self,title,user):
        duplicated = Task.objects.filter(title=title,user=user).exists()
        return duplicated
    
    def clean_spaces(self,title):
        pattern1 = r"^\s{1,}|\s{1,}$"
        pattern2 = r"\s{2,}"
        result = re.sub (pattern1,"", title)
        result = re.sub (pattern2," ", title)
        return result
    



