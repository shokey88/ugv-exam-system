from django.db import models


# =========================
# STUDENT MODEL
# =========================
class Student(models.Model):

    fullname = models.CharField(max_length=100)

    username = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField(unique=True)

    department = models.CharField(max_length=50)

    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


# =========================
# EXAM MODEL
# =========================
class Exam(models.Model):

    subject = models.CharField(max_length=100)

    exam_date = models.DateField()

    exam_time = models.TimeField()

    room = models.CharField(max_length=50)

    department = models.CharField(max_length=50)

    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subject} - {self.department}"