from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from random import sample

from django.contrib import messages

from .models import Product, Question, Answer, Questionnaire, UserProduct, Friend
from .forms import CustomLoginForm, CreateUserForm, QuestionnaireForm, FriendRequestForm

# Create your views here.

def hello(request):
    return render(request, "index.html")

def products_list(request):
    products = Product.objects.all().order_by("-price", "title").prefetch_related('favourite')
    return render(request, 'products.html', {'products': products})

@login_required
def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product.html', {'product':product})
    
@login_required
def favourite_list(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user

    favourite_prod = user.favourite.all()
    
    return render(request, 'favourite_list.html', {'user': user, 'favourite_prod': favourite_prod})

@login_required
def toggle_favourite(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user in product.favourite.all():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    return redirect('products-list')

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
            user_id = request.user.id

            UserProduct.objects.filter(user=request.user).delete()

            user_preferences = {}
            for question in questionnaire.questions.all():
                preference_id = form.cleaned_data.get(f'question_{question.id}')
                preference_text = question.answers.get(id=preference_id).text if preference_id is not None else None
                user_preferences[question.id] = preference_text

            selected_keywords = [keyword for keyword in user_preferences.values() if keyword is not None]

            if len(selected_keywords) > 2:
                selected_keywords = sample(selected_keywords, 2)

            filters = []
            
            for keyword in selected_keywords:
                q_obj = Q(keywords__text=keyword)
                filters.append(q_obj)
            
            combined_filters = Q()
            for q_obj in filters:
                combined_filters |= q_obj

            selected_products = Product.objects.filter(combined_filters)

            for product in selected_products:
                UserProduct.objects.get_or_create(user_id=user_id, product=product)

            return redirect(reverse('questionnaire_res', kwargs={'user_id': user_id}))

    else:
        form = QuestionnaireForm()
    return render(request, 'questionnaire.html', {'form': form})

@login_required
def questionnaire_res(request, user_id):
    user = get_object_or_404(User, id=user_id)
    selected_products = UserProduct.objects.filter(user_id=user_id)

    return render(request, 'questionnaire_res.html', {'products': selected_products, 'user': user})

@login_required
def friends_page(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            friend_username = form.cleaned_data['friend_username']
            friend = User.objects.get(username=friend_username)

            if friend != request.user:
                if not Friend.objects.filter(user=request.user, friend=friend).exists():
                    Friend.objects.create(user=request.user, friend=friend)
                    return redirect('friends-page')
                else:
                    messages.error(request, 'You are already friends with this user')
            else:
                messages.error(request, 'You cannot add yourself as a friend.')
    else:
        form = FriendRequestForm()

    friends = Friend.objects.filter(user=request.user)
    return render(request, 'friends_page.html', {'form': form, 'friends': friends})

@login_required
def delete_friend(request, friend_id):
    friend = get_object_or_404(Friend, id=friend_id)
    if request.method == 'POST':
        if friend.user == request.user:
            friend.delete()
        return redirect('friends-page')

