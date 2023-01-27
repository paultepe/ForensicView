from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login


def registerpage(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect('http://127.0.0.1:8000')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('first_name')
                messages.success(request, 'Ein Konto wurde für ' + user + ' erstellt.')
                return HttpResponseRedirect('http://127.0.0.1:8000/admin')

    context = {'form': form, 'title':'Neues Konto anlegen'}
    return render(request, "account/signup.html", context)

