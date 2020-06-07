from django.db import models


# Create your models here.
# models.py


class student(models.Model):
    sid = models.CharField('学号', max_length=10, unique=True)
    pwd = models.CharField('密码', max_length=20)

    def __unicode__(self):
        return self.name


class course(models.Model):
    cid = models.CharField('课程号', max_length=20, unique=True)
    rate = models.FloatField('分数')
    nums = models.IntegerField('评价人数', default=0)
    teacher = models.CharField('教师', max_length=20)
    name = models.CharField('课程名', max_length=20)

    def __unicode__(self):
        return self.name


class join(models.Model):
    rate = models.FloatField('评分')
    sid = models.CharField('学生学号', max_length=10)
    cid = models.CharField('课程号', max_length=20)  # 课程号长度有修改
    teacher = models.CharField('教师', max_length=20)
    cname = models.CharField('课程名', max_length=20)

    def __unicode__(self):
        return self.cname


class favor(models.Model):
    time = models.DateTimeField(auto_now=True)
    sid = models.CharField('学生学号', max_length=10)
    cid = models.CharField('课程号', max_length=20)
    teacher = models.CharField('教师', max_length=20)
    cname = models.CharField('课程名', max_length=20)

    def __unicode__(self):
        return self.cname


class comment(models.Model):
    text = models.CharField('文本', max_length=150)
    sid = models.CharField('学生学号', max_length=10)
    cid = models.CharField('课程号', max_length=20)
    rate = models.FloatField('评分')
    time = models.DateTimeField(auto_now=True)
    index1 = models.IntegerField('主讲教师', default=0)
    index2 = models.IntegerField('教学内容', default=0)
    index3 = models.IntegerField('教学条件', default=0)
    index4 = models.IntegerField('教学方法', default=0)
    index5 = models.IntegerField('教学效果', default=0)

    def __unicode__(self):
        return self.sid
