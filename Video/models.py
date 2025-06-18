from django.db import models

# Create your models here.
class Login_table(models.Model):
    username=models.CharField(max_length=700)
    password=models.CharField(max_length=700)
    type=models.CharField(max_length=600)

class Expert(models.Model):
    LOGIN=models.ForeignKey(Login_table,on_delete=models.CASCADE)
    Firstname=models.CharField(max_length=700)
    Lastname= models.CharField(max_length=700)
    Place=models.CharField(max_length=700)
    Post=models.CharField(max_length=700)
    Pin=models.IntegerField()
    Email=models.CharField(max_length=700)
    Phone=models.BigIntegerField()
    Image=models.FileField()




class Study_material(models.Model):
    studymaterial=models.FileField()
    EXPERT=models.ForeignKey(Expert,on_delete=models.CASCADE)
    date=models.DateField()
    Details=models.CharField(max_length=700)

class Parent(models.Model):
    LOGIN=models.ForeignKey(Login_table,on_delete=models.CASCADE)
    Parentname=models.CharField(max_length=700)
    Studentname=models.CharField(max_length=700)
    Place=models.CharField(max_length=700)
    Post=models.CharField(max_length=700)
    Pin=models.IntegerField()
    Email=models.CharField(max_length=700)
    Phone=models.BigIntegerField()
    Image=models.FileField()

class Feedback(models.Model):
    Parent=models.ForeignKey(Parent,on_delete=models.CASCADE)
    Feedback=models.CharField(max_length=700)
    Date=models.DateField()

class Medical_Report(models.Model):
    Medical_Reportfile = models.FileField()
    Parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    Expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    Date = models.DateField()
    Status = models.CharField(max_length=700)

class Guidlines(models.Model):
     Guidlines=models.CharField(max_length=700)
     Expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
     MEDICAL = models.ForeignKey(Medical_Report, on_delete=models.CASCADE)
     Date = models.DateField()




class Tips(models.Model):
      Tips=models.CharField(max_length=700)
      Expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
      Date = models.DateField()

class Chat(models.Model):
    From= models.ForeignKey(Login_table, on_delete=models.CASCADE,related_name='From')
    TO = models.ForeignKey(Login_table, on_delete=models.CASCADE, related_name='TO')
    Date = models.DateField()
    time=models.TimeField()
    msg=models.CharField(max_length=100)





class qustions(models.Model):
      file=models.FileField()
      type=models.CharField(max_length=700)




class video_frame(models.Model):
      fileid = models.ForeignKey(qustions,on_delete=models.CASCADE)
      std = models.ForeignKey(Parent,on_delete=models.CASCADE)
      ratio=models.CharField(max_length=700)







