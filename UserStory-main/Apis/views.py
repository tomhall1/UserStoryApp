from UserStoryApp.models import UserStory, UserStoryVersion, Business, BusinessCategory, Persona, User, DevelopmentTask, RAIDS, Epic, Estimates, Platform, Project
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from json import dumps
import json
from django.http import QueryDict
import pandas as pd
import re
# Create your views here.


def del_userStroy(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    print(id)
    instance = UserStory.objects.get(id=id)
    instance.delete()
    return JsonResponse({"dc": id}, safe=False)


def related_userStory(request):
    dataObject = []
    print(type(dataObject))
    persona = request.GET.get("Persona")
    epic = request.GET.get("Epic")

    if bool(persona.strip()):
        userStories = UserStory.objects.filter(
            Persona__Name__contains=persona)
        print(len(userStories))
    else:
        userStories = UserStory.objects.all()
    if bool(epic.strip()):
        userStories = userStories.filter(
            Epic__versionName__contains=epic)
        print(len(userStories))
    print(len(userStories))
    for userStory in userStories.all():
        iWantTO = userStory.iWantTO
        soThat = userStory.soThat
        priority = userStory.priority
        id = userStory.id
        personaObject = []
        [personaObject.append(i.Name) for i in userStory.Persona.all()]
        RAIDS = []
        [RAIDS.append(i.description) for i in userStory.RAIDS.all()]
        DevelopmentTask = []
        [DevelopmentTask.append(i.description)
         for i in userStory.DevelopmentTask.all()]
        try:
            epicObject = userStory.Epic.versionName
        except:
            epicObject = ""
        dataObject.append(
            {'iWantTO': iWantTO, 'soThat': soThat, 'priority': priority, 'id': id, 'persona': personaObject,
             'RAIDS': RAIDS, 'devTask': DevelopmentTask, 'epic': epicObject})
    dataObject = dumps(dataObject)
    print(dataObject)
    return JsonResponse(dataObject, safe=False)


def editPersona(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'PUT':
        data = json.loads(request.body)
        persona = Persona.objects.get(id=id)
        # persona.Name = request.
        print(persona)
        print(data['persona'])
        persona.Name = data['persona']
        persona.save()
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addPersona(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'POST':
        userStory = UserStory.objects.get(id=id)
        data = json.loads(request.body)
        persona = Persona.objects.create(
            Name=data['persona'])
        # persona.Name = request.
        userStory.Persona.add(persona)
        userStory.save()
        return JsonResponse({'id': persona.id}, safe=False)
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def editDevTask(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'PUT':
        data = json.loads(request.body)
        devTask = DevelopmentTask.objects.get(id=id)
        # persona.Name = request.
        devTask.description = data['devTask']
        devTask.save()
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addDevTask(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'POST':
        userStory = UserStory.objects.get(id=id)
        data = json.loads(request.body)
        devTask = DevelopmentTask.objects.create(
            description=data['devTask'])
        # persona.Name = request.
        userStory.DevelopmentTask.add(devTask)
        userStory.save()
        return JsonResponse({'id': devTask.id}, safe=False)
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def editRaids(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'PUT':
        data = json.loads(request.body)
        raids = RAIDS.objects.get(id=id)
        # persona.Name = request.
        raids.description = data['raids']
        raids.save()
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addRaids(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'POST':
        userStory = UserStory.objects.get(id=id)
        data = json.loads(request.body)
        raids = RAIDS.objects.create(
            description=data['raids'])
        # persona.Name = request.
        userStory.RAIDS.add(raids)
        userStory.save()
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addSelectedUserStory(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        newUserStory = UserStory.objects.get(id=id)
        print(newUserStory.id)
        print(data['id'])
        userStory = UserStory.objects.get(id=data['id'])
        try:
            epic = Epic.objects.get(id=newUserStory.Epic.id)
            epic.delete()
        except:
            pass
        try:
            newUserStory.Persona.all().delete()
        except:
            pass
        try:
            newUserStory.RAIDS.all().delete()
        except:
            pass
        try:
            newUserStory.DevelopmentTask.all().delete()
        except:
            pass
        newEpic = Epic.objects.create(versionName=userStory.Epic.versionName)
        UserStory.objects.update_or_create(
            id=id,
            defaults={'iWantTO': userStory.iWantTO,
                      'soThat': userStory.soThat, 'Epic': newEpic},
        )
        print("done")
        devData = userStory.DevelopmentTask.all()
        newPersona = []
        for p in userStory.Persona.all():
            newPersona.append(Persona.objects.create(Name=p.Name))
        newRaids = []
        for p in userStory.RAIDS.all():
            newRaids.append(addRaidsLocal(p.description))
        newDev = []
        for p in devData:
            newDev.append(addDevTaskLocal(p.description))
        newUserStory.Persona.set(newPersona)
        newUserStory.RAIDS.set(newRaids)
        newUserStory.DevelopmentTask.set(newDev)
        newUserStory = UserStory.objects.get(id=id)
        personaObject = []
        [personaObject.append({'id': i.id, 'name': i.Name})
         for i in newUserStory.Persona.all()]
        RAIDS = []
        [RAIDS.append({'id': i.id, 'name': i.description})
         for i in newUserStory.RAIDS.all()]
        DevelopmentTask = []
        [DevelopmentTask.append({'id': i.id, 'name': i.description})
         for i in newUserStory.DevelopmentTask.all()]
        print(DevelopmentTask)
        dataObject = {'iWantTO': newUserStory.iWantTO, 'soThat': newUserStory.soThat, 'id': id, 'persona': personaObject,
                      'RAIDS': RAIDS, 'devTask': DevelopmentTask, 'epic': newUserStory.Epic.versionName}
        dataObject = dumps(dataObject)
        print(dataObject)
        return JsonResponse(dataObject, safe=False)
        # persona.Name = request.
    return JsonResponse({'id': 0, 'name': 0}, safe=False)


def addDevTaskLocal(des):
    return DevelopmentTask.objects.create(
        description=des)


def addRaidsLocal(des):
    return RAIDS.objects.create(description=des)


def editUserStory(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    print("dc")
    if request.method == 'PUT':
        userStory = UserStory.objects.get(id=id)
        data = json.loads(request.body)
        if data['name'] == 'epic':
            newEpic = Epic.objects.create(
                versionName=data['value'])
            try:
                epic = Epic.objects.get(id=userStory.Epic.id)
                epic.delete()
            except:
                pass
            obj, created = UserStory.objects.update_or_create(
                id=id,
                defaults={'Epic': newEpic},
            )

        elif data['name'] == 'iWantTo':
            UserStory.objects.update_or_create(
                id=id,
                defaults={'iWantTO': data['value']},
            )
        elif data['name'] == 'soThat':
            UserStory.objects.update_or_create(
                id=id,
                defaults={'soThat': data['value']},
            )
        elif data['name'] == 'Priority':
            obj, created = UserStory.objects.update_or_create(
                id=id,
                defaults={'priority': data['value']},
            )
            print(obj.priority)
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def editEstimate(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data['estimate'])
        Estimates.objects.update_or_create(
            id=id, defaults={'noOfHours': data['estimate']})
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addEstimate(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'POST':
        userStory = UserStory.objects.get(id=id)
        data = json.loads(request.body)
        platformObject = Platform.objects.get(id=data['id'])
        estimate = Estimates.objects.create(
            noOfHours=data['estimate'], Platform=platformObject)
        userStory.Estimates.add(estimate)
        userStory.save()
        return JsonResponse({'id': estimate.id}, safe=False)
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def editProject(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    if request.method == 'PUT':
        data = json.loads(request.body)
        project = Project.objects.get(id=data['projectId'])
        UserStoryVersion.objects.update_or_create(
            id=id,
            defaults={'Project': project},
        )
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def editUserStoryVersion(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    print("dc")
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data['name'] == 'VersionName':
            obj, created = UserStoryVersion.objects.update_or_create(
                id=id,
                defaults={'name': data['value']},
            )
        elif data['name'] == 'VersionDescription':
            UserStoryVersion.objects.update_or_create(
                id=id,
                defaults={'description': data['value']},
            )
    return JsonResponse({'dataObject': 'dc'}, safe=False)


def addUserStory(request, id):
    if id == 0:
        return JsonResponse({'dataObject': 'dc'}, safe=False)
    userStoryVersion = UserStoryVersion.objects.get(id=id)
    print(id)
    userStory = UserStory.objects.create(
        iWantTO="",
        soThat="",
        priority="",
        userStoriesVersion=userStoryVersion)
    print("UserStoryVersion")
    print(userStory.userStoriesVersion.id)
    return JsonResponse({'id': userStory.id}, safe=False)


def getAllfilters(request):
    personaObjects = list(set(Persona.objects.values_list('Name')))
    epicObjects = list(set(Epic.objects.values_list('versionName')))
    iWantToObjects = list(set(UserStory.objects.values_list('iWantTO')))
    soThatObjects = list(set(UserStory.objects.values_list('soThat')))
    devTasksObjects = list(
        set(DevelopmentTask.objects.values_list('description')))
    RAIDSObjects = list(set(RAIDS.objects.values_list('description')))
    userNameObjects = list(set(User.objects.values_list('username')))
    projectObjects = list(set(Project.objects.values_list('name')))
    businessObjects = list(set(Business.objects.values_list('name')))
    return JsonResponse({'epic': epicObjects, 'persona': personaObjects, 'iWantTo': iWantToObjects,
                         'soThat': soThatObjects, 'devTask': devTasksObjects, 'raids': RAIDSObjects,
                         'username': userNameObjects, 'project': projectObjects, 'business': businessObjects}, safe=False)


def addNewUserStory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data['VersionName'])
        print(data['VersionDescription'])
        userStoryVersion = UserStoryVersion.objects.create(
            name=data['VersionName'], description=data['VersionDescription'])
        print(id)
        if data['project'] and data['project'] != 0:
            project = Project.objects.get(id=data['project'])
            UserStoryVersion.objects.update_or_create(
                id=userStoryVersion.id,
                defaults={'Project': project},
            )
            print(project)
        userStory = UserStory.objects.create(
            iWantTO="",
            soThat="",
            priority="",
            userStoriesVersion=userStoryVersion)
        print("UserStoryVersion")
        print(userStory.userStoriesVersion.id)
        return JsonResponse({'id': userStory.id, 'versionId': userStoryVersion.id}, safe=False)
    return JsonResponse({'id': 0, 'versionId': 0}, safe=False)


def addPlatform(request):
    if request.method == 'POST':
        print("dc")
        data = json.loads(request.body)
        platform = Platform.objects.create(name=data["platform"])
        return JsonResponse({'id': platform.id, 'name': platform.name}, safe=False)
    return JsonResponse({'id': 0, 'versionId': 0}, safe=False)


def addIndustry(request):
    if request.method == 'POST':
        print("dc")
        data = json.loads(request.body)
        cate = BusinessCategory.objects.create(name=data["name"])
        print(cate)
        return JsonResponse({'id': cate.id, 'name': cate.name}, safe=False)
    return JsonResponse({'id': 0, 'name': 0}, safe=False)


def RemoveField(request):
    data = json.loads(request.body)
    name = data['name']
    id = data['id']
    if name == "Persona":
        instance = Persona.objects.get(id=id)
        instance.delete()
    elif name == "Dev":
        instance = DevelopmentTask.objects.get(id=id)
        instance.delete()
    else:
        instance = RAIDS.objects.get(id=id)
        instance.delete()
    return JsonResponse({'id': 0, 'name': 0}, safe=False)
# def dataEntry(request):
#     dfs = pd.read_excel('sum sheet.xlsx', sheet_name="Sheet2")
#     persona = []
#     epic = []
#     soThat = []
#     iWantTo = []
#     finalDevTask = []
#     finalRaids = []
#     row = [{}]
#     for table, df in dfs.items():
#         if table == "Persona":
#             for data in df[70:90]:
#                 persona.append(data)
#                 row.append({'persona': persona})
#         if table == "Epic":
#             for data in df[70:90]:
#                 epic.append(data)
#                 row.append({'ep': persona})
#         if table == "I want to":
#             for data in df[70:90]:
#                 iWantTo.append(data)
#         if table == "So that":
#             for data in df[70:90]:
#                 soThat.append(data)
#         if table == "DevTasks & RAIDs (Risk, Assumption, Issue & Dependency)":
#             for data in df[70:90]:
#                 print(data)
#                 listData = re.split(
#                     '----------------RAIDs----------------', data)
#                 print(listData)
#                 devTask = listData[0]
#                 raids = []
#                 finalDevTask.append(re.split('\n-', devTask))
#                 if len(listData) == 2:
#                     raids = listData[1]
#                     finalRaids.append(re.split(r'[()]', raids))
#                 else:
#                     finalRaids.append([])

#     print(len(persona))
#     print(len(epic))
#     print(len(soThat))
#     print(len(iWantTo))
#     print(len(finalDevTask))
#     print(len(finalRaids))
#     for x in range(len(persona)):
#         personaDb = []
#         personaDb.append(Persona.objects.create(
#             Name=persona[x]))
#         print(epic[x])
#         epicDb = Epic.objects.create(
#             versionName=epic[x])
#         devTaskDb = []
#         for dev in finalDevTask[x]:
#             devTaskDb.append(DevelopmentTask.objects.create(description=dev))
#         raidsDb = []
#         try:
#             for Raid in finalRaids[x]:
#                 if len(Raid) > 2:
#                     raidsDb.append(RAIDS.objects.create(description=Raid))
#         except:
#             pass
#         userStory = UserStory.objects.create(
#             iWantTO=iWantTo[x],
#             soThat=soThat[x],
#             Epic=epicDb
#         )
#         userStory.Persona.set(personaDb)
#         userStory.RAIDS.set(raidsDb)
#         userStory.DevelopmentTask.set(devTaskDb)
#     return JsonResponse({'id': 0, 'versionId': 0}, safe=False)
