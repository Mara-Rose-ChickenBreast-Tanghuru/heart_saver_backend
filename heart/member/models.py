from django.db import models


class Member(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nickname = models.CharField(null=False, max_length=50, unique=True)
    name = models.CharField(null=False, max_length=50)
    age = models.IntegerField(null=False)
    gender = models.CharField(null=False, max_length=10)
    medicalCondition = models.CharField(max_length=500, null=True)
    etc = models.CharField(max_length=500, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HeartRate(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    hrv = models.IntegerField(null=False)
    member = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name="heart_rates"
    )
    created_at = models.DateTimeField(auto_now_add=True)

# Location은 view에서 Redis를 이용
