from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def gig_details(request, id):
    return render(request, 'gig_details.html',{})
