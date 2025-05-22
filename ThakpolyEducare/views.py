from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


## Write your views here

class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'deshboard.html')
    
class IndexView(View):
    def get(self, request):

        cp={
            "active_id":"b001",
        }
        return render(request, 'public/index.html', context=cp)

class AboutView(View):
    def get(self, request):
        cp={
            "active_id":"b002",
        }
        return render(request, 'public/about.html', context=cp)

