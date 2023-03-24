from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from UserStoryApp.models import UserStory, Persona, DevelopmentTask, Estimates, Platform, RAIDS, Epic, US_Group, UserStoryVersion, Project, Business
from .forms import AddUserStoryVersionForm
from django.contrib.auth.decorators import login_required
from .filter import userStoryVersionsFilter
from json import dumps
# Create your views here.

userStories = []


@login_required
def userStoryVersions_list(request):
    PROJECT = ""
    CREATOR = ""
    userStoriesVersions = UserStoryVersion.objects.all()
    my_filter = userStoryVersionsFilter(
        request.GET, queryset=userStoriesVersions)
    userStoriesVersions = my_filter.qs
    if request.GET.get("PROJECT"):
        userStoriesVersions = userStoriesVersions.filter(
            Project__name__contains=request.GET.get("PROJECT"))
        PROJECT = request.GET.get("PROJECT")
    if request.GET.get("CREATOR"):
        userStoriesVersions = userStoriesVersions.filter(
            User__username__contains=request.GET.get("CREATOR"))
        CREATOR = request.GET.get("CREATOR")
    return render(request, 'userStoryVersions/userStoryVersions.html', {'users': userStoriesVersions, 'filter': my_filter, 'form': {'PROJECT': PROJECT, 'CREATOR': CREATOR}})


@login_required
def add_userStoryVersions(request):
    id = 0
    totalEstimates = []
    personaObjects = list(Persona.objects.values_list('Name'))
    print(personaObjects)
    personaObjects = dumps(personaObjects)
    epicObjects = list(Epic.objects.values_list('versionName'))
    epicObjects = dumps(epicObjects)
    project = Project.objects.all()
    business = Business.objects.all()
    projects = []
    current_user = request.user
    for p in project:
        projects.append({'id': p.id, 'name': p.name,
                        'business': p.Business.id})
    projectJson = dumps(projects)
    if request.method == 'GET' and 'Platform' in request.GET:
        Platform.objects.create(name=request.GET.get("Name"))
        print(request.GET.get("platform"))
        return redirect('/UserStoryVersion/addUserStoryVersion/')
    platforms = Platform.objects.all()
    if request.method == 'POST' and request.POST.get("project") != '0':
        persona = []
        platformIds = request.POST.getlist("platforms")
        platformIds = [eval(i) for i in platformIds]
        noOfHoursList = request.POST.getlist("estimate[]")
        estimates = []
        for i in range(len(platformIds)):
            platformObject = Platform.objects.get(id=platformIds[i])
            print(platformObject)
            estimates.append(
                Estimates.objects.create(noOfHours=noOfHoursList[i], Platform=platformObject))

        personas = request.POST.getlist("Persona")
        print(personas)
        for p in personas:
            if not bool(p.strip()):
                continue
            persona.append(Persona.objects.create(
                Name=p))
        devs = request.POST.getlist("Dev")
        devResult = []
        for dev in devs:
            if not bool(dev.strip()):
                continue
            devResult.append(DevelopmentTask.objects.create(description=dev))
        # estimates = request.POST.get("Estimates").splitlines()
        # for estimate in estimates:
        #     Estimates.objects.create()
        Raids = request.POST.getlist("RAIDS")
        RaidsResult = []
        for Raid in Raids:
            print(Raid, "dc")
            if not bool(Raid.strip()):
                print("dc")
                continue
            RaidsResult.append(RAIDS.objects.create(description=Raid))
        epic = Epic.objects.create(
            versionName=request.POST.get("Epic"))
        current_user = request.user
        project_id = request.POST.get("project")
        project = Project.objects.get(id=request.POST.get("project"))
        VersionName = request.POST.get("VersionName")
        VersionDescription = request.POST.get("VersionDescription")
        if int(request.POST.get("id")):
            print(int(request.POST.get("id")))
            userStoryVersion = UserStoryVersion.objects.get(
                id=int(request.POST.get("id")))
        else:
            userStoryVersion = UserStoryVersion.objects.create(
                name=VersionName, description=VersionDescription, Project=project, User=current_user)
        userStory = UserStory.objects.create(
            iWantTO=request.POST.get("IWantTO"),
            soThat=request.POST.get("SoThat"),
            priority=request.POST.get("Priority"),
            Epic=epic,
            userStoriesVersion=userStoryVersion,
        )
        userStory.Persona.set(persona)
        userStory.Estimates.set(estimates)
        print(RaidsResult)
        print(devResult)
        userStory.RAIDS.set(RaidsResult)
        userStory.DevelopmentTask.set(devResult)
        userStories.append(userStory)
        if not request.POST.get('AddAnother'):
            print("here")
            print(request.POST.get('AddAnother'))
            return redirect('/UserStoryVersion/list/', {'persona': persona, 'userStories': userStories})
        business = Business.objects.all()
        projects = Project.objects.all()
        platformIds = [{'id': i, 'name': Platform.objects.get(
            id=i).name} for i in platformIds]
        print(platformIds)
        id = userStoryVersion.id
        for u in userStories:
            for e in u.Estimates.all():
                status = next(
                    (True for i in totalEstimates if int(i['id']) == e.Platform.id), False)
                if status:
                    for estimate in totalEstimates:
                        if estimate['id'] == e.Platform.id:
                            estimate['hours'] = estimate['hours'] + e.noOfHours
                else:
                    totalEstimates.append(
                        {'id': e.Platform.id, 'name': e.Platform.name, 'hours': e.noOfHours})
        print(totalEstimates)
        return render(request, 'userStoryVersions/addUserStoryVersion.html', {'platforms': platforms, 'id': id, 'totalEstimates': totalEstimates, 'persona': projects, 'platformIds': platformIds, 'userStories': userStories, 'userStoryVersion': userStoryVersion, 'business': business, 'personaObjects': personaObjects, 'epicObjects': epicObjects, 'project': projectJson})
    del userStories[:]
    return render(request, 'userStoryVersions/addUserStoryVersion.html', {'platforms': platforms, 'id': id, 'totalEstimates': totalEstimates, 'persona': projects, 'userName': current_user.username, 'project': projectJson, 'business': business, 'personaObjects': personaObjects, 'epicObjects': epicObjects})


def userStoryVersionDetails(request, id):
    platforms = Platform.objects.all()
    User = get_user_model()
    userStoryVersion = UserStoryVersion.objects.get(id=id)
    userStory = UserStory.objects.filter(
        userStoriesVersion=userStoryVersion).all()
    project = Project.objects.all()
    business = Business.objects.all()
    projects = []
    current_user = request.user
    for p in project:
        projects.append({'id': p.id, 'name': p.name,
                        'business': p.Business.id})
    projectJson = dumps(projects)
    platformIds = []
    for user in userStory:
        for e in user.Estimates.all():
            platformIds.append(e.Platform.id)
    totalEstimates = []
    for u in userStory:
        for e in u.Estimates.all():
            status = next(
                (True for i in totalEstimates if int(i['id']) == e.Platform.id), False)
            if status:
                for estimate in totalEstimates:
                    if estimate['id'] == e.Platform.id:
                        estimate['hours'] = estimate['hours'] + e.noOfHours
            else:
                totalEstimates.append(
                    {'id': e.Platform.id, 'name': e.Platform.name, 'hours': e.noOfHours})
    return render(request, 'userStoryVersions/userStoryVersionsDetails.html',
                  {'totalEstimates': totalEstimates, 'platformIds': platformIds, 'platforms': platforms, 'userStoryVersion': userStoryVersion, 'userStories': userStory, 'persona': project, 'userName': current_user.username, 'project': projectJson, 'business': business})


def Details(request, id):
    personaObjects = list(Persona.objects.values_list('Name'))
    print(personaObjects)
    personaObjects = dumps(personaObjects)

    epicObjects = list(Epic.objects.values_list('versionName'))
    epicObjects = dumps(epicObjects)
    platforms = Platform.objects.all()
    projects = Project.objects.all()
    userStoryVersion = UserStoryVersion.objects.get(id=id)
    userStory = UserStory.objects.filter(userStoriesVersion=userStoryVersion)
    platformIds = []
    selectedPlatforms = []
    allEstimate = []
    priority = []
    for u in userStory:
        for i in u.Estimates.all():
            allEstimate.append(i.Platform.id)
            # 0 if any(d['id'] ==
            #          i.id for d in selectedPlatforms) else
            if any(d['id'] == i.Platform.id for d in selectedPlatforms):
                for d in selectedPlatforms:
                    if d['id'] == i.Platform.id:
                        d['estimate'] = d['estimate'] + i.noOfHours
                        d['priority'].append(
                            {'name': u.priority, 'estimate': i.noOfHours})
                        break
            else:

                platformIds.append(i.Platform.id)
                selectedPlatforms.append(
                    {'id': i.Platform.id, 'name': i.Platform.name, 'priority': [{'name': u.priority, 'estimate': i.noOfHours}], 'estimate': i.noOfHours})

        u.platforms = allEstimate
        allEstimate = []
        priority.append(u.priority)
    print(selectedPlatforms)
    return render(request, 'userStoryVersions/Details.html', {'userStories': userStory, 'priority': priority, 'persona': projects, 'personaObjects': personaObjects, 'epicObjects': epicObjects, 'userStoriesVersion': userStoryVersion, 'platformIds': platformIds, 'platforms': platforms, 'selectedPlatforms': selectedPlatforms, 'jsonSelectedPlatforms': dumps(selectedPlatforms)})
