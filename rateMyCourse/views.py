from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

#GET
def searchSchool(request):
    school = request.GET.get('school');
    keyword = request.GET.get('keyword');
    return HttpResponse("searchSchool school:"+school+" keyword:"+keyword)

#GET
def getIndex(request):
    return HttpResponse("getIndex")

#GET
def getCourse(request, course_id):
    return HttpResponse("getCourse course_id:"+course_id)

#POST
def signIn(request):
    username = request.POST['username']
    password = request.POST['password']
    return HttpResponse("signIn username: "+username+" password:"+password)

#POST
def signUp(request):
    username = request.POST['username']
    password = request.POST['password']
    mail = request.POST['mail']
    return HttpResponse("signUp username: "+username+" password:"+password+" mail:"+mail)

#POST
def courseAddComment(request):
    username = request.POST['username']
    content = request.POST['content']
    parentId = request.POST['parentId']
    courseId = request.POST['courseId']

    return HttpResponse("courseAddComment: "+username+content+parentId+content)

#POST
def courseAddRate(request):
    username = request.POST['username']
    rate = request.POST['rate']
    courseId = request.POST['courseId']
    return HttpResponse("courseAddRate: "+username+rate+courseId)