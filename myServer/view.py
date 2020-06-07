from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world ! ")


# if __name__ == '__main__':
#     print(senta.func1())

