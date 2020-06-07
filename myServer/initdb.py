# -*- coding: utf-8 -*-

from django.http import HttpResponse

from Model.models import student, comment, course, join, favor


# 数据库操作
def create(request):
    test1 = student(sid='2016211208',
                    pwd='123456')
    test1.save()
    test1 = student(sid='2016211209',
                    pwd='111222')
    test1.save()
    test1 = course(name='软件工程方法',
                   rate=0,
                   cid='00001',
                   teacher='王洪',
                   nums=0)
    test1.save()
    test1 = course(name='计算机系统结构',
                   rate=0,
                   cid='00002',
                   teacher='李亮',
                   nums=0)
    test1.save()
    test1 = join(rate=0,
                 sid='2016211208',
                 cid='00002',
                 teacher='李亮',
                 cname='计算机系统结构')
    test1.save()
    test1 = join(rate=0,
                 sid='2016211208',
                 cid='00001',
                 teacher='王洪',
                 cname='软件工程方法')
    test1.save()
    return HttpResponse("数据添加成功")
