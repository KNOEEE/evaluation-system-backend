# -*- coding: utf-8 -*-

from django.http import HttpResponse

from Model.models import student, comment, course, join, favor
import json
import time
import random
import reCons

import senta


# 学生操作
def login(request):
    try:
        if request.method == 'POST':
            req = json.loads(request.body)
            sid = req['sid']
            pwd = req['pwd']
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    list1 = student.objects.filter(sid=sid, pwd=pwd)
    if len(list1) == 1:
        response = {"code": 0,
                    "sid": sid}
    else:
        response = {"code": 1}
    # print(pwd)
    json1 = json.dumps(response)
    return HttpResponse(json1)


def setPwd(request):
    req = json.loads(request.body)
    sid = req['sid']
    pwd = req['pwd']
    newPwd = req['newPwd']
    list1 = student.objects.filter(sid=sid, pwd=pwd)
    if len(list1) == 1:
        student.objects.filter(sid=sid).update(pwd=newPwd)
        response = {"code": 0}
    else:
        response = {"code": 1}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def browse(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        sid = req['sid']
    list1 = join.objects.filter(sid=sid)
    data1 = []
    for var in list1:
        data = {"cid": var.cid,
                "cname": var.cname,
                "teacher": var.teacher,
                "rate": var.rate}
        data1.append(data)
    response = {"code": 0,
                "datalist": data1}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def evaluate(request):
    req = json.loads(request.body)
    txt = req['text']  # 处理无评价，txt=‘’ rate=x 这里可能出错
    sid = req['sid']
    cid = req['cid']
    indexList = req['index']  # 满分10分，senta的满分是1，index满分是5
    indexRate = 0
    for index in indexList:
        indexRate += index
    if txt != '':
        totalRate = senta.predict_sentiment(txt)
        # print(totalRate)

        indexRate *= 9
        totalRate = ((4 * totalRate + 1) * 5 + indexRate) / 25
    else:
        totalRate = indexRate * 2 / 5
    try:
        opr0 = join.objects.get(sid=sid, cid=cid)
        opr0.rate = totalRate
        opr0.save()

        opr1 = comment(sid=sid, cid=cid, rate=totalRate,
                       text=txt, index1=indexList[0], index2=indexList[1],
                       index3=indexList[2], index4=indexList[3], index5=indexList[4])
        opr1.save()

        opr2 = course.objects.get(cid=cid)
        currRate = opr2.rate
        currNum = opr2.nums
        newRate = (currNum * currRate + totalRate) / (currNum + 1)
        opr2.rate = newRate
        opr2.nums = currNum + 1
        opr2.save()

        response = {"code": 0}
    except:
        response = {"code": 1}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def fav(request):
    req = json.loads(request.body)
    sid = req['sid']
    cid = req['cid']

    if req['fav'] == 1:
        opr0 = favor.objects.filter(sid=sid, cid=cid)
        if len(opr0) == 0:
            opr1 = course.objects.get(cid=cid)

            teacher = opr1.teacher
            opr2 = favor(sid=sid, cid=cid, teacher=teacher, cname=opr1.name)
            opr2.save()
            response = {"code": 0}
        else:
            response = {"code": 1}
    else:
        opr3 = favor.objects.get(sid=sid, cid=cid)
        opr3.delete()
        response = {"code": 0}
    # response = {"code": 0}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def hot(request):
    list1 = []
    req = course.objects.filter(rate__gte=5)
    list1Len = min(len(req), 5)
    while len(list1) < list1Len:
        var = random.choice(req)
        commList = comment.objects.filter(cid=var.cid).order_by("-rate")
        shortTxt = commList[0].text  # IndexError: list index out of range??
        rate = round(var.rate, 1)
        if rate > 9.1:
            stars = 5
        elif rate > 8.1:
            stars = 4.5
        else:
            stars = round(var.rate) / 2
        data = {"cid": var.cid,
                "stars": stars,
                "rate": rate,
                "cname": var.name,
                "shortTxt": shortTxt}
        list1.append(data)
        req = req.exclude(cid=var.cid)
    response = {"code": 0, "datalist": list1}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def search(request):
    dataRev = json.loads(request.body)
    keyword = dataRev['keyword']
    list1 = []
    teacherQs = course.objects.filter(teacher__contains=keyword)
    req = course.objects.filter(name__contains=keyword).union(teacherQs)
    for var in req:
        commList = comment.objects.filter(cid=var.cid).order_by("-rate")
        if len(commList) > 0:
            shortTxt = commList[0].text
        else:
            shortTxt = '暂无评价'
        rate = round(var.rate, 1)
        if rate > 9.1:
            stars = 5
        elif rate > 8.1:
            stars = 4.5
        else:
            stars = round(var.rate) / 2
        data = {"cid": var.cid,
                "stars": stars,
                "rate": rate,
                "cname": var.name,
                "shortTxt": shortTxt}
        list1.append(data)
    response = {"code": 0, "datalist": list1}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def getComm(request):
    req = json.loads(request.body)
    cid = req['cid']
    sid = req['sid']
    commList = []
    opr0 = course.objects.get(cid=cid)
    teacher = opr0.teacher
    opr1 = comment.objects.filter(cid=cid).order_by("-rate")
    for var in opr1:
        commList.append(var.text)
        if len(commList) > 4:
            break
    opr2 = favor.objects.filter(sid=sid, cid=cid)
    response = {"code": 0,
                "teacher": teacher,
                "textList": commList,
                "favored": len(opr2)}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def getMyFav(request):
    req = json.loads(request.body)
    sid = req['sid']
    datalist = []
    opr1 = favor.objects.filter(sid=sid)
    for var in opr1:
        cid = var.cid
        opr2 = course.objects.get(cid=cid)
        rate = round(opr2.rate, 1)
        if rate > 9.1:
            stars = 5
        elif rate > 8.1:
            stars = 4.5
        else:
            stars = round(opr2.rate) / 2
        dataRet = {"cid": cid,
                   "teacher": var.teacher,
                   "cname": var.cname,
                   "rate": rate,
                   "stars": stars,
                   "time": var.time}
        datalist.append(dataRet)
    response = {"code": 0,
                "courseList": datalist}
    json1 = json.dumps(response, cls=reCons.ComplexEncoder)
    return HttpResponse(json1)


def getMyComm(request):
    req = json.loads(request.body)
    sid = req['sid']
    datalist = []
    opr1 = comment.objects.filter(sid=sid)
    for var in opr1:
        cid = var.cid
        opr2 = course.objects.get(cid=cid)
        rate = round(var.rate, 1)
        teacher = opr2.teacher
        cname = opr2.name
        if rate > 9.1:
            stars = 5
        elif rate > 8.1:
            stars = 4.5
        else:
            stars = round(opr2.rate) / 2
        dataRet = {"cid": var.cid,
                   "teacher": teacher,
                   "cname": cname,
                   "rate": rate,
                   "stars": stars,
                   "time": var.time
                   }
        datalist.append(dataRet)
    response = {"code": 0,
                "courseList": datalist}
    json1 = json.dumps(response, cls=reCons.ComplexEncoder)
    return HttpResponse(json1)


def getATxt(request):
    req = json.loads(request.body)
    sid = req['sid']
    cid = req['cid']
    opr1 = comment.objects.get(sid=sid, cid=cid)
    response = {"code": 0,
                "text": opr1.text,
                "indexList": [opr1.index1, opr1.index2,
                              opr1.index3, opr1.index4,
                              opr1.index5]}
    json1 = json.dumps(response)
    return HttpResponse(json1)


def top10(request):
    list1 = []
    req = course.objects.filter(rate__gte=6).order_by("-nums").order_by("-rate")
    list1Len = min(len(req), 10)
    for var in req:
        commList = comment.objects.filter(cid=var.cid).order_by("-rate")
        shortTxt = commList[0].text
        rate = round(var.rate, 1)
        if rate > 9.1:
            stars = 5
        elif rate > 8.1:
            stars = 4.5
        else:
            stars = round(var.rate) / 2
        data = {"cid": var.cid,
                "stars": stars,
                "rate": rate,
                "cname": var.name,
                "shortTxt": shortTxt}
        list1.append(data)
        if len(list1) == list1Len:
            break
    response = {"code": 0, "datalist": list1}
    json1 = json.dumps(response)
    return HttpResponse(json1)
