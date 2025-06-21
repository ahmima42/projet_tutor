from django.db import models
from accounts.models import User, Professor

class Module(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='modules')
    semester = models.CharField(max_length=20)
    credits = models.IntegerField()
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class StudentModule(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='enrolled_modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='enrolled_students')
    enrollment_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'module')
    
    def __str__(self):
        return f"{self.student} in {self.module}"

class GradeType(models.Model):
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    student_module = models.ForeignKey(StudentModule, on_delete=models.CASCADE, related_name='grades')
    grade_type = models.ForeignKey(GradeType, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student_module.student} - {self.grade_type}: {self.value}"

class Session(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    session_type = models.CharField(max_length=20, choices=[
        ('lecture', 'Cours'),
        ('td', 'TD'),
        ('tp', 'TP'),
    ])
    topic = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.module} - {self.date} {self.start_time}-{self.end_time}"

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=[
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('excused', 'Excusé'),
    ])
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('session', 'student')
    
    def __str__(self):
        return f"{self.student} - {self.session}: {self.status}"