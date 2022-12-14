from django.shortcuts import render, redirect
from random import randint
from bakery.models import Bakeries
from bakery.forms import Form_bakeries
from django.templatetags.static import static
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# this function was made to create the first products.
def bakeries(request):
    rand = randint(0, 2000)
    al1 = Bakeries.objects.create(name = 'Pan Frances', description = 'baguette', sku = rand, price = 50)
    context = {
        'bakery': al1
    }
    return render(request, 'bakery/bakeries.html/', context=context)


def list_bakeries(request):
    all = Bakeries.objects.all()
    context ={
        'list' : all
    }
    return render(request,'bakery/bakeries.html/', context = context)

def create_bakeries(request):
    if request.method == 'POST':
        form = Form_bakeries(request.POST, request.FILES)
        if form.is_valid():
            Bakeries.objects.create (
			     name = form.cleaned_data['nombre'],
			     price = form.cleaned_data['precio' ],
                 description = form.cleaned_data['descripcion'],
                 stock = form.cleaned_data['stock'],
                 image = form.cleaned_data['imagen']
							)
        return redirect(list_bakeries)
    elif request.method == 'GET':
        if request.user.is_superuser:
            form = Form_bakeries
            context = {
                'form': form
            }
            return render(request, 'bakery/create_bakeries.html/', context=context)
        else:
            return redirect('login')
class Update_bakeries(LoginRequiredMixin, UpdateView):
    model = Bakeries
    fields = ['name','description', 'sku', 'price','image']
    template_name = 'bakery/edit_bakeries.html'
    success_url = '/all/'
# @login_required
# def edit_bakeries(request, pk):
#         if request.method == 'POST':
           
#             form = Form_bakeries(request.POST, request.FILES)
#             if form.is_valid():
#                 product = Bakeries.objects.get(id=pk)
#                 product.name = form.cleaned_data['nombre']
#                 product.price = form.cleaned_data['precio']
#                 product.description = form.cleaned_data['descripcion']
#                 product.stock = form.cleaned_data['stock']
#                 product.image = form.cleaned_data['imagen']
#                 product.save()

#                 return redirect(list_bakeries)
            
#         elif request.method == 'GET':
#             if request.user.is_superuser:
#                 product = Bakeries.objects.get(id=pk)
#                 form = Form_bakeries(initial={
#                     'nombre': product.name,
#                     'precio': product.price,
#                     'descripcion': product.description,
#                     'stock': product.stock,
#                     'imagen': product.image,})
#                 context = {'form': form}
#                 return render(request, 'bakery/edit_bakeries.html/', context=context)
#             else:
#                 return redirect('login')
@login_required
def delete_bakeries(request, pk):
    if request.method == 'GET':
        if request.user.is_superuser:
            product = Bakeries.objects.get(pk=pk)
            context = {'product': product}
            return render(request, 'bakery/delete_bakeries.html', context=context)
        else:
            return redirect('login')
    elif request.method == 'POST':
        product = Bakeries.objects.get(pk=pk)
        product.delete()
        return redirect(list_bakeries)

class Detail_bakeries(LoginRequiredMixin, DetailView):
    model = Bakeries
    template_name = 'bakery/detail_bakeries.html'