from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import AddBusinessForm1, AddBusinessForm2
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from UserStoryApp.models import Business, BusinessCategory, Project, User, UserStoryVersion
from django.contrib.auth.decorators import login_required
from .filter import BusinessFilter
# Create your views here.


@login_required
def business_list(request):
    Industry = ""
    Projects = ""
    user = ""
    business = Business.objects.all()
    my_filter = BusinessFilter(request.GET, queryset=business)
    business = my_filter.qs
    if request.GET.get("Industry"):
        business = business.filter(
            businessIndustry__name__contains=request.GET.get("Industry"))
        Industry = request.GET.get("Industry")
    if request.GET.get("Projects"):
        business = business.filter(
            project__name__contains=request.GET.get("Projects"))
        Projects = request.GET.get("Projects")
    if request.GET.get("user"):
        business = business.filter(
            User__username__contains=request.GET.get("user"))
        user = request.GET.get("user")
    for b in business:
        project = Project.objects.filter(Business=b)
        b.project = "\n".join([f'{p.name} , ' for p in project])

    return render(request, 'Business/Business.html', {'businesses': business, 'filter': my_filter, 'form': {'industry': Industry, 'user': user, 'projects': Projects}})


@login_required
def add_business(request):
    businessIndustries = BusinessCategory.objects.all()
    internal_User = User.objects.filter(Role=2)
    Customer = User.objects.filter(Role=1)

    if request.method == 'POST':
        form = AddBusinessForm1(request.POST)
        form2 = AddBusinessForm2(request.POST)
        businessIndustry = []
        try:
            for b in request.POST.get("businessIndustry"):
                businessIndustry.append(
                    BusinessCategory.objects.get(id=int(b)))
        except:
            pass
        users = []
        try:
            for u in request.POST.get("Customer"):
                users.append(User.objects.get(id=int(u)))
        except:
            pass
        try:
            for u in request.POST.get("Internal_User"):
                users.append(User.objects.get(id=int(u)))
        except:
            pass
        print(users)
        print(businessIndustry)
        if form.is_valid() and form2.is_valid():
            cd = form.cleaned_data
            cd2 = form2.cleaned_data
            user = Business.objects.create(hourlyRate=cd['hourlyRate'], name=cd['name'],
                                           LegalEntityName=cd2['LegalEntityName'], Address=cd2['Address'],
                                           BusinessNumber=cd2['BusinessNumber'],
                                           BusinessEmail=cd2['BusinessEmail'], ABN=cd2['ABN'])
            user.businessIndustry.set(businessIndustry)
            user.User.set(users)
            if user is not None:
                return redirect('/Business/list/')
        return render(request, 'Business/addBusiness.html', {'form': form, 'form2': form2, 'internal_User': internal_User, 'customer': Customer, 'businessIndustries': businessIndustries})
    form = AddBusinessForm1()
    form2 = AddBusinessForm2()
    return render(request, 'Business/addBusiness.html', {'form': form, 'form2': form2, 'internal_User': internal_User, 'customer': Customer, 'businessIndustries': businessIndustries})


def BusinessDetails(request, id):
    businessIndustries = BusinessCategory.objects.all()
    internal_User = User.objects.filter(Role=2)
    Customer = User.objects.filter(Role=1)
    business = Business.objects.get(id=id)
    industriesIds = [i.id for i in business.businessIndustry.all()]
    customerIds = []
    internalUserIds = []
    projects = Project.objects.filter(Business=business).all()
    # userStoriesVersion = UserStoryVersion.objects.filter(
    #     Business=business).all()
    userStoryVersions = UserStoryVersion.objects.filter(
        Project__Business=business).all()
    for i in business.User.all():
        if i.Role == 1:
            customerIds.append(i.id)
        elif i.Role == 2:
            internalUserIds.append(i.id)
    print(industriesIds)
    print(business.User.all())
    form = AddBusinessForm1(
        initial={'name': business.name, 'businessIndustry': business.businessIndustry.all(), 'hourlyRate': business.hourlyRate,
                 'Internal_User': business.User.filter(Role=2), 'Customer': business.User.filter(Role=1)})
    form2 = AddBusinessForm2(
        initial={'LegalEntityName': business.LegalEntityName, 'Address': business.Address,
                 'BusinessNumber': business.BusinessNumber, 'BusinessEmail': business.BusinessEmail, 'ABN': business.ABN})
    return render(request, 'Business/BusinessDetails.html', {'form': form, 'form2': form2, 'projects': projects, 'userStoryVersions': userStoryVersions, 'internal_User': internal_User, 'customer': Customer, 'businessIndustries': businessIndustries, 'form3': {'name': business.name, 'industriesIds': industriesIds,
                                                                                                                                                                                                                                                                   'internalUserIds': internalUserIds, 'customerIds': customerIds}})
