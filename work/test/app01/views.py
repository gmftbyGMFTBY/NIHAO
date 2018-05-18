from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .forms import AddForm

def home(request):
    odd = [i for i in range(100)]
    return render(request, 'home.html', {'odd': odd})

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a + b))

def index(request):
    if request.method == 'POST':# 当提交表单时

        form = AddForm(request.POST) # form 包含提交的数据

        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:# 当正常访问时
        form = AddForm()
    return render(request, 'index.html', {'form': form})
