from django.shortcuts import render, redirect
from django.http import HttpResponse


def testpage(request):
    return HttpResponse('Тестова сторінка')
