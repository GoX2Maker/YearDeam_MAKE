from django.shortcuts import render
from django.http import HttpResponse
from .models import ImageUpload
from .forms import ImageUploadForm

def image_upload(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return render(request, 'pybo/image_upload.html', {'form': form})
    else:
        form = ImageUploadForm()
    return render(request, 'pybo/image_upload.html', {'form': form})

def image_list(request):
    images = ImageUpload.objects.all()
    return render(request, 'pybo/image_list.html', {'images': images})




def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

# Create your views here.
