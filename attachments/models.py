from django.db import models
from accounts.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField()
    nssf_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class Attachment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    supervisor_name = models.CharField(max_length=100)
    supervisor_email = models.EmailField(blank=True)
    supervisor_phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.student} at {self.company}"