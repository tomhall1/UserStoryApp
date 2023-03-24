
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from UserStoryApp.models import UserStory, Persona, DevelopmentTask, RAIDS, Epic, US_Group, UserStoryVersion, Project, Platform, Estimates
from .forms import AddUserStoryForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .filters import UserStoriesFilter
from json import dumps
# Create your views here.

personaObjects = list(Persona.objects.values_list('Name'))
print(personaObjects)
personaObjects = dumps(personaObjects)
epicObjects = list(Epic.objects.values_list('versionName'))
epicObjects = dumps(epicObjects)


@login_required
def userStories_list(request):
    persona = []
    RAIDS = []
    DevTask = []
    Indicator = []
    epic = []
    soThat = []
    iWantTO = []
    userStories = UserStory.objects.all()
    iWantTOObjects = [i.iWantTO for i in userStories]
    iWantTOObjects = dumps(iWantTOObjects)
    soThatObjects = [i.soThat for i in userStories]
    soThatObjects = dumps(soThatObjects)
    devTasksObjects = []
    for i in userStories:
        for d in i.DevelopmentTask.all():
            devTasksObjects.append(d.description)
    devTasksObjects = dumps(devTasksObjects)
    RAIDSObjects = []
    for i in userStories:
        for d in i.RAIDS.all():
            RAIDSObjects.append(d.description)
    RAIDSObjects = dumps(RAIDSObjects)

    if request.GET.getlist("Persona"):
        if request.GET.getlist("Persona")[0]:
            persona = request.GET.getlist("Persona")
            persona = list(filter(None, persona))
            for p in persona:
                userStories = userStories.filter(
                    Persona__Name__contains=p)

    if request.GET.getlist("RAIDS"):
        if request.GET.getlist("RAIDS")[0]:
            RAIDS = request.GET.getlist("RAIDS")
            RAIDS = list(filter(None, RAIDS))
            for r in RAIDS:
                userStories = userStories.filter(
                    RAIDS__description__contains=r)

    if request.GET.getlist("DevTask"):
        if request.GET.getlist("DevTask")[0]:
            DevTask = request.GET.getlist("DevTask")
            DevTask = list(filter(None, DevTask))
            for d in DevTask:
                userStories = userStories.filter(
                    DevelopmentTask__description__contains=d)

    if request.GET.get("Indicator"):
        Indicator = request.GET.getlist("Indicator")
        Indicator = list(filter(None, Indicator))
        for i in Indicator:
            userStories = userStories.filter(
                US_Group__description__contains=i)

    if request.GET.getlist("Epic"):
        if request.GET.getlist("Epic")[0]:
            epic = request.GET.getlist("Epic")
            epic = list(filter(None, epic))
            for e in epic:
                userStories = userStories.filter(
                    Epic__versionName__contains=e)

    if request.GET.getlist("IWantTO"):
        if request.GET.getlist("IWantTO")[0]:
            iWantTO = request.GET.getlist("IWantTO")
            iWantTO = list(filter(None, iWantTO))
            for i in iWantTO:
                userStories = userStories.filter(
                    iWantTO__contains=i)

    if request.GET.getlist("SoThat"):
        if request.GET.getlist("SoThat")[0]:
            soThat = request.GET.getlist("SoThat")
            soThat = list(filter(None, soThat))
            for i in soThat:
                userStories = userStories.filter(
                    soThat__contains=i)

    return render(request, 'userStories/userStories.html', {'users': userStories, 'personaObjects': personaObjects, 'epicObjects': epicObjects, 'iWantTOObjects': iWantTOObjects, 'soThatObjects': soThatObjects, 'devTasksObjects': devTasksObjects, 'RAIDSObjects': RAIDSObjects, 'form': {'persona': persona, 'RAIDS': RAIDS, 'DevTask': DevTask, 'indicator': Indicator, 'Epic': epic, 'SoThat': soThat, 'IWantTO': iWantTO}})


@login_required
@csrf_protect
def add_userStory(request):
    platforms = Platform.objects.all()
    current_user = request.user
    print("dc")
    if request.method == 'GET' and 'Platform' in request.GET:
        print("here")
        Platform.objects.create(name=request.GET.get("Name"))
        print(request.GET.get("platform"))
        return redirect('/UserStories/addUserStory/')
    if request.method == 'POST':
        platformIds = request.POST.getlist("platforms")
        platformIds = [eval(i) for i in platformIds]
        noOfHoursList = request.POST.getlist("estimate[]")
        estimates = []
        for i in range(len(platformIds)):
            platformObject = Platform.objects.get(id=platformIds[i])
            print(platformObject)
            estimates.append(
                Estimates.objects.create(noOfHours=noOfHoursList[i], Platform=platformObject))
        uS_Group = US_Group.objects.create(
            description=request.POST.get("US_Group"))
        persona = []
        personas = request.POST.getlist("Persona")
        for p in personas:
            persona.append(Persona.objects.create(
                Name=p))
        devs = request.POST.getlist("Dev")
        devResult = []
        for dev in devs:
            devResult.append(DevelopmentTask.objects.create(description=dev))
        # estimates = request.POST.get("Estimates").splitlines()
        # for estimate in estimates:
        #     Estimates.objects.create()
        Raids = request.POST.getlist("RAIDS")
        RaidsResult = []
        for Raid in Raids:
            RaidsResult.append(RAIDS.objects.create(description=Raid))
        epic = Epic.objects.create(
            versionName=request.POST.get("Epic"))
        userStory = UserStory.objects.create(
            iWantTO=request.POST.get("IWantTO"),
            soThat=request.POST.get("SoThat"),
            Epic=epic,
            US_Group=uS_Group
        )
        userStory.Persona.set(persona)
        userStory.RAIDS.set(RaidsResult)
        userStory.DevelopmentTask.set(devResult)
        userStory.Estimates.set(estimates)
    return render(request, 'userStories/addUserStory.html', {'platforms': platforms, 'personaObjects': personaObjects, 'epicObjects': epicObjects})


def userStoryDetails(request, id):
    if request.method == 'GET' and 'Platform' in request.GET:
        print("here")
        Platform.objects.create(name=request.GET.get("Name"))
        print(request.GET.get("platform"))
        param = str(id)
        return redirect('/UserStories/userStoryDetails/'+param+'')
    platforms = Platform.objects.all()
    User = get_user_model()
    users = UserStory.objects.get(id=id)
    print()
    platformIds = [i.Platform.id for i in users.Estimates.all()]
    print(platformIds)
    return render(request, 'userStories/userStoryDetails.html', {'platforms': platforms, 'userStory': users, 'personaObjects': personaObjects, 'platformIds': platformIds, 'epicObjects': epicObjects})


def Details(request, id):
    if request.method == 'POST':
        userStory = UserStory.objects.get(id=id)
        userStory.iWantTO = request.POST.get("IWantTO")
        userStory.soThat = request.POST.get("SoThat")
        newEpic = Epic.objects.create(
            versionName=request.POST.get("Epic"))
        epic = Epic.objects.get(id=userStory.Epic.id)
        userStory.Epic = newEpic
        epic.delete()
        newPersona = []
        personas = request.POST.getlist("Persona")
        for p in personas:
            if p:
                newPersona.append(Persona.objects.create(
                    Name=p))
        userStory.save()
        userStory.Persona.remove()
        userStory.Persona.add(*newPersona)
        userStory.save()
        devs = request.POST.getlist("Dev")
        newDevResult = []
        for dev in devs:
            if dev:
                newDevResult.append(
                    DevelopmentTask.objects.create(description=dev))
        userStory.DevelopmentTask.remove()
        userStory.DevelopmentTask.add(*newDevResult)
        userStory.save()

        Raids = request.POST.getlist("RAIDS")
        newRaidsResult = []
        for Raid in Raids:
            if Raid:
                newRaidsResult.append(RAIDS.objects.create(description=Raid))
        userStory.RAIDS.remove()
        userStory.RAIDS.add(*newRaidsResult)
        userStory.save()

        platformIds = request.POST.getlist("platforms")
        platformIds = [eval(i) for i in platformIds]
        noOfHoursList = request.POST.getlist("estimate[]")
        estimates = []
        for i in range(len(platformIds)):
            platformObject = Platform.objects.get(id=platformIds[i])
            print(platformObject)
            estimates.append(
                Estimates.objects.create(noOfHours=noOfHoursList[i], Platform=platformObject))
        userStory.Estimates.remove()
        userStory.Estimates.add(*estimates)
        userStory.save()
    platforms = Platform.objects.all()
    userStory = UserStory.objects.get(id=id)
    platformIds = [i.Platform.id for i in userStory.Estimates.all()]
    if userStory.userStoriesVersion:
        if userStory.userStoriesVersion.Project:
            userStory.userStoriesVersion.Project.project = len(
                UserStoryVersion.objects.filter(Project=userStory.userStoriesVersion.Project).all())
    return render(request, 'userStories/Details.html', {'userStory': userStory, 'platformIds': platformIds, 'platforms': platforms})
