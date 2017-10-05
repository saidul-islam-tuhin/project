from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    subject_list = ['CSE', 'LLB', 'BBA', 'EEE', 'ENGLISH',]
    context = {
        'subject_list': subject_list,
    }
    return render(request, 'TutionFee/home.html', context)


def subject_wise(request, subject):
    divisions_list = ['Dhaka', 'Chittagong', 'Rajshahi', 'Barisal', 'Khulna',
                     'Mymensingh', 'Rangpur', 'Sylhet']
    context = {
        'subject': subject,
        'divisions_list': divisions_list,
    }

    return render(request, 'TutionFee/tuition.html', context)
