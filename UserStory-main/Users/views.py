from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import AddUserForm, EditUserForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from UserStoryApp.models import User, Project, Business, Role
from django.contrib.auth.decorators import login_required
from .filter import UsersFilter
from json import dumps
# Create your views here.


@login_required
def user_list(request):
    projectObject = []
    businessObject = []
    nameObject = []
    User = get_user_model()
    users = User.objects.all()
    my_filter = UsersFilter(request.GET, queryset=users)
    users = my_filter.qs
    print(users)

    roles = []
    role = request.GET.get("Role") if request.GET.get(
        "Role") else ""

    if role:
        for r in Role:
            if role in r.name:
                roles.append(r.value)
        print(roles)
        for r in roles:
            print(r)
            users = users.filter(Role=r)
    # [roles.append(name) for name in dir(Role) if not name.startswith('_')]
    # print(request.GET.get("Role"))
    # roles = filter(lambda x: role in x, roles)
    # roles = list(roles)
    projectValue = request.GET.get("Project") if request.GET.get(
        "Project") else ""
    businessValue = request.GET.get("Business") if request.GET.get(
        "Business") else ""
    UsersObjects = []
    for u in users:
        print(request.GET.get("Project"))
        project = Project.objects.filter(
            User=u)
        if projectValue:
            project = project.filter(name__contains=projectValue)
        if len(project) and projectValue:
            u.project = project
            UsersObjects.append(u)
        elif not projectValue:
            u.project = project
            UsersObjects.append(u)
        [projectObject.append(i.name) for i in project]
    projectObject = dumps(projectObject)
    finalUserObjects = []
    for u in UsersObjects:
        business = Business.objects.filter(User=u)
        if businessValue:
            business = business.filter(name__contains=businessValue)
        if len(business) and businessValue:
            u.business = business
            finalUserObjects.append(u)
        elif not businessValue:
            u.business = business
            finalUserObjects.append(u)
        [businessObject.append(i.name) for i in business]
        u.Role = Role(u.Role).name
    businessObject = dumps(businessObject)
    [nameObject.append(i.username) for i in finalUserObjects]
    nameObject = dumps(nameObject)
    return render(request, 'user/users.html', {'users': finalUserObjects, 'filter': my_filter, 'projectObject': projectObject, 'businessObject': businessObject, 'nameObject': nameObject, 'Role': role, 'Project': projectValue, 'Business': businessValue})


@ login_required
def add_user(request):
    if request.method == 'POST':
        print('done')
        form = AddUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], password=cd['password'],
                                            email=cd['email'], first_name=cd['first_name'], last_name=cd['last_name'], Role=cd['Role'])
            if user is not None:
                if user.is_active:
                    return redirect('/Users/list/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = AddUserForm()
    return render(request, 'user/addUser.html', {'form': form})


def userDetails(request, id):
    User = get_user_model()
    users = User.objects.get(id=id)
    projects = Project.objects.filter(User=users)
    business = Business.objects.filter(User=users)
    form = EditUserForm(
        initial={'first_name': users.first_name, 'last_name': users.last_name, 'username': users.username, 'Update_password': users.password,
                 'email': users.email, 'Role': (users.Role, Role(users.Role).name)})
    if request.method == 'POST':
        u_form = EditUserForm(request.POST, instance=users)
        print(u_form)
        if u_form.is_valid():
            cd = u_form.cleaned_data
            users = u_form.save()
            users.set_password(cd['Update_password'])
            users.save()
        return redirect('/Users/list/')
    return render(request, 'user/userDetails.html', {'form': form, 'projects': projects, 'business': business})
