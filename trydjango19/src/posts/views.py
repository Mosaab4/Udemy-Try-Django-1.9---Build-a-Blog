from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404

from .forms import PostForm
from .models import Post

# Create your views here.


def post_create(request):
	form = PostForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit = False)
		print form.cleaned_data.get("title")
		print form.cleaned_data.get("content")
		instance.save()

	# if request.method == "POST":
	# 	content = request.POST.get("content")
	# 	title = request.POST.get("title")

	# 	Post.objects.create(title=title,content=content)
	context = {
		"form": form,

	}
	return render(request, "post_form.html", context)

def post_detail(request , id): #read
	instance = get_object_or_404(Post,id=id)

	context = {
		"title":"Detail",
		"instance": instance,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	queryset = Post.objects.all()
	context = {
		"object_list" : queryset,
		"title":"My User List"
	}

	return render(request, "index.html", context)

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")
