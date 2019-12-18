
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ImageForm
from .models import Image


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    print(form)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.user = request.user
        new_item.save()
        return JsonResponse({'status':"1"})
    else:
        return JsonResponse({'status':"0"})


@login_required(login_url='/account/login/')
def list_images(request):
    images_list = Image.objects.filter(user=request.user)
    paginator = Paginator(images_list, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        images = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        images = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        images = current_page.object_list

    return render(request, 'image/list_images.html', {"images": images , "page":current_page})

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id = image_id)
        image.delete()
        return JsonResponse({"status":"1" })
    except:
        return JsonResponse({"status":"2"})

def falls_images(request):
    images = Image.objects.all()
    return render(request , 'image/falls_images.html' , {"images":images})