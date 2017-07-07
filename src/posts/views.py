from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm

# Create your views here.

def post_create(request):
	form = PostForm()
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		print("Title: " + title)
		print("Content: " + content)
		Post.objects.create(title)
	context = {
		"form" : form
	}
	return render(request, "post_form.html", context)

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_detail(request, id):
	# instance = Post.objects.get(id=101)
	instance = get_object_or_404(Post, id=id)
	context = {
		"instance" : instance,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	querySet = Post.objects.all()
	context = {
		"listOfPosts" : querySet,
		"function" : "List"
	}

	# if request.user.is_authenticated():
	# 	context = {
	# 		"function" : "Authenticated"
	# 	}
	# else:
	# 	context = {
	# 		"function" : "Not Authenticated. Please login."
	# 	}

	return render(request, "index.html", context)
	# return HttpResponse("<h1>List</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")