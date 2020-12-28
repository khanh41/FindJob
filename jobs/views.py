from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import *
from .models import *
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers


def home(request):
    qs = JobListing.objects.all()
    jobs_count = JobListing.objects.all().count()
    user = User.objects.all().count()
    company_count = JobListing.objects.filter(company_name__startswith='P').count()
    paginator = Paginator(qs, 5)  # Show 5 jobs per page
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'query': qs,
        'job_qs': jobs_count,
        'company_name': company_count,
        'nav': 'home'
    }
    return render(request, "home.html", context)


def about_us(request):
    return render(request, "jobs/about_us.html", {'nav': 'about_us'})


def service(request):
    return render(request, "jobs/services.html", {'nav': 'services'})


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form,
        'nav': 'contact'
    }
    return render(request, "jobs/contact.html", context)


@login_required
def job_listing(request):
    query = JobListing.objects.all().count()

    qs = JobListing.objects.all().order_by('-published_on')
    paginator = Paginator(qs, 3)  # Show 3 jobs per page
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'query': qs,
        'job_qs': query,
        'nav': 'job_listing'
    }
    return render(request, "jobs/job_listing.html", context)


@login_required
def job_post(request):
    form = JobListingForm(request.POST or None)

    form.fields['vacancy'].required = False
    form.fields['description'].required = False
    form.fields['experience'].required = False
    form.fields['published_on'].required = False
    form.fields['Salary'].required = True

    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/jobs/job-listing/')
    context = {
        'form': form,
        'nav': 'job_listing'
    }
    return render(request, "jobs/job_post.html", context)


def job_single(request, id):
    job_query = get_object_or_404(JobListing, id=id)
    form = CommentForm()
    dem = job_query.number_of_comments
    if request.method == "POST":
        form = CommentForm(request.POST, author=request.user, jobpost_connected=job_query)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
            
    context = {
        'form': form,
        'q': job_query,
        'nav': 'job_listing',
        'dem': dem
    }
    return render(request, "jobs/job_single.html", context)


@login_required
def apply_job(request):
    form = JobApplyForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form,
        'nav': 'job_listing'
    }
    return render(request, "jobs/job_apply.html", context)


class SearchView(ListView):
    model = JobListing
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        print(self.request.GET['title'])
        print(self.request.GET['job_location'])
        print(self.request.GET['employment_status'])
        return self.model.objects.filter(title__icontains=self.request.GET['title'],
                                         job_location__icontains=self.request.GET['job_location'],
                                         employment_status__icontains=self.request.GET['employment_status'])


def count_list(data, check):
    if len(check) == 0:
        check = len(data) * [1]
    set_data = set(data)
    dict_data = {}
    for i in set_data:
        dict_data[i] = 0
    for x in set_data:
        for i in range(len(data)):
            if data[i] == x:
                dict_data[x] += check[i]
    return [list(dict_data.keys()), list(dict_data.values())]


def job_static(request):
    template_name = "jobs/job_static.html"
    kieu_lam = []
    loai_nghe = []
    cho_lam = []
    luong = []
    time = []
    for i in JobListing.objects.values_list():
        kieu_lam.append(i[4])
        loai_nghe.append(i[2])
        cho_lam.append(i[11])
        luong.append(int(i[12]))
        time.append(str(i[14].month) + "/" + str(i[14].year))

    tong_nghe_response = count_list(time, [])
    tong_luong_response = count_list(time, luong)

    kieu_lam_response = count_list(kieu_lam, [])
    loai_nghe_response = count_list(loai_nghe, [])
    cho_lam_response = count_list(cho_lam, [])
    set_data = set(cho_lam)
    dict_data = {}
    for i in set_data:
        dict_data[i] = 0
    for x in set_data:
        count = 0
        for i in range(len(cho_lam)):
            if cho_lam[i] == x:
                dict_data[x] += luong[i]
                count += 1
        dict_data[x] /= count
    cho_lam_luong_response = [
        list(dict_data.keys()),
        list(dict_data.values()),
    ]
    temp = list(zip(*sorted(zip(tong_nghe_response[0], tong_nghe_response[1]), key=lambda x: int(x[0].split("/")[0]) + 100 * int(x[0].split("/")[1]))))
    temp2 = list(zip(*sorted(zip(tong_luong_response[0], tong_luong_response[1]), key=lambda x: int(x[0].split("/")[0]) + 100 * int(x[0].split("/")[1]))))
    context = {
        "kieu_lam": kieu_lam_response,
        "cho_lam": cho_lam_response,
        "loai_nghe": loai_nghe_response,
        "cho_lam_luong": cho_lam_luong_response,
        "tong_nghe": [list(temp[0]),list(temp[1])],
        "tong_luong": [list(temp2[0]),list(temp2[1])],
        'nav' : 'job_static'
    }
    return render(request, template_name, context)
