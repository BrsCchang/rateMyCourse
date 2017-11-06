from django.shortcuts import render, get_list_or_404
from rateMyCourse.models import *
import json
from urllib import request, parse
# Create your views here.

from django.http import HttpResponse


#GET
def getIndex(request):
    return render(request, "rateMyCourse/index.html")


def signUp(request):
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username or mail or password',
            }))
    try:
        User(username=username, mail=mail, password=password).save()
    except Exception as err:
        errmsg = str(err)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': 'mail repeated',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': 'username repeated',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': 'other error, maybe out of length',
                }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

    '''
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)
    '''

def solrSearch(keywords, school, department):
    url = "http://127.0.0.1:8080/solr/collection1/select?q=%s&wt=json&indent=true"
    keys = dict()
    if(school != None):
        keys['school_name'] = school
    if(department != None):
        keys['department_name'] = department
    keys['course_name'] = keywords
    s = ' '.join([
        '+' + key + ':\"' + keys[key] + '\"' for key in keys
    ])
    print(url%parse.quote(s))
    try:
        t = request.urlopen(url%parse.quote(s)).read().decode('utf-8')
    except Exception:
        return [Course.objects.all()[0].number]
    t = json.loads(t)
    return {i['course_number'] for i in t['response']['docs']}

#GET
def search(request):
    keywords = request.GET['keywords']
    if('school' in request.GET):
        school = request.GET['school']
    else:
        school = None
    if('department' in request.GET):
        department = request.GET['department']
    else:
        department = None
    courselist = solrSearch(keywords, school, department)
    courses = []
    for c_number in courselist:
        cs = Course.objects.filter(number=c_number)
        x = getAvgScore(cs)
        courses.append({
            'name': cs[0].name,
            'ID': cs[0].number,
            'type': cs[0].coursetype,
            'credit': cs[0].credit,
            'school': cs[0].department.school.name,
            'department': cs[0].department.name,
            'rateScore': sum(x) / 4,
            'ratenumber': sum([i.rate_set.count() for i in cs])
            })

    return render(request, "rateMyCourse/searchResult.html", {'courses': courses})
    
#GET
def getAvgScore(courses):
    x = [0] * 4
    count = 0
    for c in courses:
        for rate in c.rate_set.all():
            x[0] += rate.A_score
            x[1] += rate.B_score
            x[2] += rate.C_score
            x[3] += rate.D_score
            count += 1
    if(count > 0):
        for i in range(4):
            x[i] /= count
    return x

def coursePage(request, course_number):
    courses = get_list_or_404(Course, number=course_number)
    # courses = Course.objects.filter(number=course_number)
    x = getAvgScore(courses)
    return render(request, "rateMyCourse/coursePage.html", {
        'course_name': courses[0].name,
        'course_credit': courses[0].credit,
        'course_profession': courses[0].department.name,
        'course_type': courses[0].coursetype,
        'course_scores': sum(x) / 4,
        'detail1': '有趣程度：%d'%(x[0]), 
        'detail2': '充实程度：%d'%(x[1]),
        'detail3': '课程难度：%d'%(x[2]),
        'detail4': '课程收获：%d'%(x[3]),
        'course_website': courses[0].website if courses[0].website != '' else 'we have no website',
        'profession_website': couses[0].department.website if courses[0].department.website != '' else 'we have no website',
        })

def ratePage(request, course_number):
    courses = get_list_or_404(Course, number=course_number)
    return render(request, "rateMyCourse/ratePage.html", {
            'course': {
                'name': courses[0].name,
                'school': courses[0].department.school.name,
                'department': courses[0].department.name,
            },
            'aspect1': '有趣程度',
            'aspect2': '充实程度',
            'aspect3': '课程难度',
            'aspect4': '课程收获',
        })

#POST
def signIn(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username or mail or password',
            }))
    try:
        u = User.objects.get(username=username)
    except Exception:
        try:
            u = User.objects.get(mail=username)
        except Exception:
            return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'username or mail mot exists',
            }))
    if(password != u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'wrong password',
            }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

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

#GET TMP IN INDEX
def getSchool(request):
    result = {
        'school': [s.name for s in School.objects.all()],
    }
    return HttpResponse(json.dumps(result))

def getDepartment(request):
    try:
        school = School.objects.get(name=request.GET['school'])
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school not found'
            }))
    return HttpResponse(json.dumps({
        'department': [d.name for d in school.department_set.all()]
        }))

def getCourse(request):
    try:
        school = School.objects.get(name=request.GET['school'])
        department = school.department_set.get(name=request.GET['department'])
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school or department not found'
            }))
    return HttpResponse(json.dumps({
        'course': [c.name for c in department.course_set.all()]
        }))

def getComment(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    cmtList = []
    for c in courses:
        for cmt in c.comment_set.all():
            cmtList.append({
                'userName': cmt.user.username if cmt.anonymous == False else '匿名用户',
                'text': cmt.content,
                'time': cmt.time.strftime('%y/%m/%d'),
                'iTerm': cmt.term,
                'iTeacher': '，'.join([t.name for t in cmt.course.teacher_set.all()]),
                'iTotal': cmt.total_score,
                })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))

def getTeachers(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    tList = []
    for c in courses:
        tList.append([
            t.name for t in c.teacher_set.all()
            ])
    return HttpResponse(json.dumps({
        'statCode': 0,
        'teachers': tList,
        }))

def getOverAllRate(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    return HttpResponse(json.dumps({
        'statCode': 0,
        'rate': getAvgScore(courses),
        }))
