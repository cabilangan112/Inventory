import barcode
import os,sys
from .forms import CustomerForm,ItemForm,RegistrationForm
from .models import Item
from barcode.writer import ImageWriter
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate


# Create your views here.

class Home(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = Item.objects.all()
        context = {
            'post': post,
        }
        return render(request, 'stock/stock_list.html', context)

class Customerlist(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.all()
        context = {
            'customer': customer,
        }
        return render(request, 'customer_list.html', context)

class Releaselist(View):
    def get(self, request, *args, **kwargs):
        release = Release.objects.all()
        context = {
            'release':release,
        }
        return render(request, 'stock/release_list.html', context)

class ItemCreateView(LoginRequiredMixin, View):
    form_class = ItemForm
    initial = {'key': 'value'}
    template_name = 'stock/item-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            bcode = post.number
            ean = barcode.get('Code39', bcode, writer=ImageWriter())
            filename = ean.save('live-static/media-root/'+bcode)
            post.barcode = bcode + '.png'
            quantity = post.quantity
            unit_cost = post.unit_cost
            total_value = quantity * unit_cost
            post.total = total_value
            post.save()
            return redirect('stock:post-list')
        else:
            form = ItemForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class RegisterFormView(LoginRequiredMixin, View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        user_form = self.form_class(initial=self.initial)
        context = {
            'user_form': user_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('stock:post-list')
        else:
            form = RegistrationForm()
        context = {
            'user_form': user_form,
        }
        return render(request, self.template_name, context)