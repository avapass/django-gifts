from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib import messages

from .models import Product, Question, Answer, Questionnaire
from .forms import CustomLoginForm, CreateUserForm, QuestionnaireForm

# Create your views here.

def hello(request):
    return render(request, "index.html")

def products_list(request):
    products = Product.objects.all()
    products = products.order_by("-price", "title")

    return render(request, "products.html", {"products": products})

@login_required
def product(request, id):
    product = get_object_or_404(Product, id=id)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    context = {
        'product': product,
        'is_favourite': is_favourite
    }
    return render(request, "product.html", context)

@login_required
def favourite_list(request):
    user = request.user
    favourite_prod = user.favourite.all()
    return render(request, "favourite_list.html", {"favourite_prod": favourite_prod})

def favourite_prod(request, id):
    product = get_object_or_404(Product, id=id)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    return HttpResponseRedirect(product.get_absolute_url())

def custom_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect("login")

    context={"form": form}
    return render(request, 'register.html', context)

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomLoginForm()
        if request.method == "POST":
            form = CustomLoginForm(request.POST)
            if form.is_valid():
                login(request, form.authenticated_user)
                return redirect("/")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def questionnaire(request):
    questionnaire = Questionnaire.objects.first()

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            user_preferences = {}
            for question in questionnaire.questions.all():
                preference_id = form.cleaned_data.get('question_{}'.format(question.id))
                preference_text = question.answers.get(id=preference_id).text if preference_id is not None else None
                user_preferences[question.id] = preference_text

            products = Product.objects.all()

            search_words = [preference for preference in user_preferences.values() if preference is not None]

            selected_products = []
            for product in products:
                if all(word in product.description for word in search_words):
                    selected_products.append(product.title)

            return render(request, 'questionnaire_res.html', {'products': selected_products})
    else:
        form = QuestionnaireForm()
    return render(request, 'questionnaire.html', {'form': form})

