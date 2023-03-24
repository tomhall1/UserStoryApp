from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.


class Role(Enum):
    Customer = 1
    InternalUser = 2


class User (AbstractUser):
    Role = models.IntegerField(blank=True, null=True, default=2)
    project = []
    business = []

    def get_projects(self):
        return "\n".join([f'{p.name} , ' for p in self.project])

    def get_businesses(self):
        return "\n".join([f'{p.name} , ' for p in self.business])


def __str__(self):
    return self.name


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)

    class Meta:
        db_table = "Platform"


def __str__(self):
    return self.name


class BusinessCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)

    class Meta:
        db_table = "BusinessCategory"


def __str__(self):
    return self.name


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    businessIndustry = models.ManyToManyField(
        BusinessCategory)
    hourlyRate = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    LegalEntityName = models.TextField(blank=True)
    Address = models.TextField(blank=True)
    BusinessNumber = models.IntegerField(blank=True, null=True)
    BusinessEmail = models.TextField(blank=True)
    User = models.ManyToManyField(User)
    ABN = models.IntegerField(blank=True, null=True)

    def get_categories(self):
        return "\n".join([f'{p.name} , ' for p in self.businessIndustry.all()])

    def get_users(self):
        return "\n".join([f'{p.username} , ' for p in self.User.all()])

    class Meta:
        db_table = "Business"


def __str__(self):
    return self.name


class BusinessUsers(models.Model):
    id = models.AutoField(primary_key=True)
    Role = models.TextField(blank=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Business = models.ForeignKey(
        Business, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "BusinessUsers"


def __str__(self):
    return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    Business = models.ForeignKey(Business, on_delete=models.CASCADE)
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    project = ""

    class Meta:
        db_table = "Project"


def __str__(self):
    return self.name


class UserStoryVersion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    Project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "UserStoryVersion"


def __str__(self):
    return self.name


class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField(blank=True)

    class Meta:
        db_table = "Persona"


def __str__(self):
    return self.name


class RAIDS(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "RAIDS"


def __str__(self):
    return self.name


class DevelopmentTask(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "DevelopmentTask"


def __str__(self):
    return self.name


class US_Group(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "US_Group"


def __str__(self):
    return self.name


class Epic(models.Model):
    id = models.AutoField(primary_key=True)
    versionName = models.TextField(blank=True)

    class Meta:
        db_table = "Epic"

    def get_categories(self):
        return "\n".join([f'{p.name} , ' for p in self.Category.all()])


def __str__(self):
    return self.name


class Estimates(models.Model):
    id = models.AutoField(primary_key=True)
    noOfHours = models.IntegerField(blank=True, null=True)
    Platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    class Meta:
        db_table = "Estimates"


def __str__(self):
    return self.name


class UserStory(models.Model):
    id = models.AutoField(primary_key=True)
    iWantTO = models.TextField(blank=True)
    soThat = models.TextField(blank=True)
    priority = models.TextField(blank=True)
    userStoriesVersion = models.ForeignKey(
        UserStoryVersion, on_delete=models.CASCADE, blank=True, null=True)
    Persona = models.ManyToManyField(Persona)
    RAIDS = models.ManyToManyField(RAIDS)
    DevelopmentTask = models.ManyToManyField(DevelopmentTask)
    Estimates = models.ManyToManyField(Estimates)
    US_Group = models.ForeignKey(
        US_Group, on_delete=models.CASCADE, blank=True, null=True)
    Epic = models.ForeignKey(Epic, on_delete=models.CASCADE, null=True)
    platforms = []

    class Meta:
        db_table = "UserStory"

    def get_Persona(self):
        return "\n".join([f'{p.Name} , ' for p in self.Persona.all()])

    def get_RAIDS(self):
        print("g\r\ng")
        return "\n".join([f'{p.description} \r\n' for p in self.RAIDS.all()])

    def get_DevTask(self):
        return "\n".join([f'{p.description} \r\n' for p in self.DevelopmentTask.all()])

    def get_UsGroupState(self):
        return True if self.US_Group.description else False

    def get_UsGroup(self):
        if self.US_Group:
            return self.US_Group.description
        return False


def __str__(self):
    return self.name
