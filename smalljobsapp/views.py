from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Gig, Profile, Purchase, Reviews
from .forms import GigForm

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="db55y3xm47zg2dx8",
                                  public_key="2pdrwtdtb7dmq9t3",
                                  private_key="39043d37478c3142dce7e671ba6ff8bf")
                                  
# Create your views here.
def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, 'home.html', {"gigs": gigs})

@login_required(login_url="/")
def user_profile(request, username):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user_profile.about = request.POST['about']
        user_profile.slogan = request.POST['slogan']
        user_profile.save()
    else:
        try:
            user_profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')

    gigs = Gig.objects.filter(user=user_profile.user, status=True)
    return render(request, 'user_profile.html', {"user_profile": user_profile, "gigs": gigs})

@login_required(login_url="/")
def preview_profile(request, username):
        if request.method == 'POST':
            preview_profile = Profile.objects.get(user=request.user)
            preview_profile.about = request.POST['about']
            preview_profile.slogan = request.POST['slogan']
            preview_profile.save()
        else:
            try:
                preview_profile = Profile.objects.get(user__username=username)
            except Profile.DoesNotExist:
                return redirect('/')

        gigs = Gig.objects.filter(user=preview_profile.user, status=True)
        return render(request, 'preview_profile.html', {"preview_profile": preview_profile, "gigs": gigs})

def gig_details(request, id):
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
            Reviews.objects.create(review=request.POST['content'], gig_id=id, user=request.user)
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')
        
    if request.user.is_anonymous() or \
        Purchase.objects.filter(gig=gig, customer=request.user).count() == 0 or \
        Reviews.objects.filter(gig=gig, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, customer=request.user).count() > 0
            
    reviews = Reviews.objects.filter(gig=gig)    
    client_token = braintree.ClientToken.generate()
    return render(request, 'gig_details.html',{"show_post_review":show_post_review, "reviews":reviews, "gig":gig, "client_token":client_token})

@login_required(login_url="/")    
def create_gig(request):
    error = ''
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
            error = "You should check in on some of those fields below..."
        #print(gig_form.is_valid())
        #print(gig_form.errors())
        
    gig_form = GigForm()
    return render(request, 'create_gig.html', {"error":error})

@login_required(login_url="/")    
def edit_gig(request, id):
        try:
            gig = Gig.objects.get(id=id, user=request.user)
            error = ''
            if request.method == 'POST':
                gig_form = GigForm(request.POST, request.FILES, instance=gig)
                if gig_form.is_valid():
                    gig.save()
                    return redirect('my_gigs')
                else:
                    error = "Data is not valid"
            return render(request, 'edit_gig.html', {"gig":gig, "error":error})
        except Gig.DoesNotExist:
            return redirect('/')
        

@login_required(login_url="/")     
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})

@login_required(login_url="/")      
def create_purchase(request):
    errors=''
    if request.method == 'POST':
        try:
            gig =Gig.objects.get(id = request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('/')
            
        nonce_from_the_client = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": gig.price,
            "payment_method_nonce": nonce_from_the_client
        }) 
        
        if result.is_success:
            Purchase.objects.create(gig=gig, customer=request.user, transaction_id=result.transaction.id)
        else: 
            errors = ", ".join([e.message for e in result.errors.deep_errors])
            print(errors)
    
    return redirect('/')
    
@login_required(login_url="/")
def my_sales(request):
    purchases = Purchase.objects.filter(gig__user=request.user)
    return render(request, 'my_sales.html', {"purchases": purchases})

@login_required(login_url="/")
def my_purchases(request):
    purchases = Purchase.objects.filter(customer=request.user)
    return render(request, 'my_purchases.html', {"purchases": purchases})
    
def category(request, link):
    categories = {
        "graphics-design": "GD",
        "digital-marketing": "DM",
        "video-animations": "VA",
        "music-audio": "MA",
        "programming-tech": "PT"
    }
    try:
        gigs = Gig.objects.filter(category=categories[link])
        return render(request, 'home.html', {"gigs":gigs})
    except KeyError:
        return redirect('home')
        
def search(request):
    gigs = Gig.objects.filter(title__contains=request.GET['title'])
    return render(request, 'home.html', {"gigs": gigs})
