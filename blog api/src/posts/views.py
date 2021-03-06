from urllib.parse import quote_plus
from django.contrib import messages
from django.http import HttpResponse , HttpResponseRedirect ,Http404
from django.db.models import Q
from django.shortcuts import render , get_object_or_404 , redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timezone
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType



from comments.models import Comment
from comments.forms import CommentForm



from .forms import PostForm
from .models import Post
 

# Create your views here.


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	
	# if not request.user.is_authenticated():
	# 	raise Http404

	form = PostForm(request.POST or None , request.FILES or None)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()

		messages.success(request , "Successfully Created")

		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form": form,

	}
	return render(request, "post_form.html", context)

def post_detail(request , slug=None): #read
	instance = get_object_or_404(Post,slug=	slug)

	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string = quote_plus(instance.content)


	initial_data = {
		"content_type":instance.get_content_type,
		"object_id":instance.id,
	}
	form = CommentForm(request.POST or None, initial=initial_data)

	if form.is_valid() and request.user.is_authenticated():
		print(form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		
		parent_object = None
		try :
			parent_id = int(request.POST.get("parent_id"))
		except :
			parent_id = None

		if parent_id :
			parent_qs = Comment.objects.filter(id=parent_id)
			
			if parent_qs.exists() and parent_qs.count()==1 :
				parent_object = parent_qs.first()

		new_comment , created = Comment.objects.get_or_create(
			user=request.user,
			content_type = content_type,
			object_id = obj_id,
			content = content_data,
			parent = parent_object,
		)

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	# comments = Comment.objects.filter_by_instance(instance)
	comments = instance.comments

	context = {
		"title":instance.title,
		"instance": instance,
		"share_string":share_string,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()

	queryset_list = Post.objects.active()#filter(draft=False).filter(publish=timezone.now())#.order_by("-timestamp")

	# if request.user.is_staff or request.user.is_superuser :
	queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
		).distinct()

	paginator = Paginator(queryset_list, 2) # Show 2 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	index = queryset.number -1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index <= max_index - 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]


	context = {
		"object_list" : queryset,
		"queryset":queryset,
		"page_range": page_range,
		"title":"List",
		"today": today,
	}

	return render(request, "post_list.html", context)




def post_update(request , slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None ,instance=instance)


	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		messages.success(request, "<a>Item</a> Saved", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {
		"title":instance.title,
		"instance": instance,
		"form":form,
	}

	return render(request,"post_form.html", context)

def post_delete(request , slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post , slug=slug)
	instance.delete()

	messages.success(request , "Successfully Deleted")

	return redirect("posts:list")
