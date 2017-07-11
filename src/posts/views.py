from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print(form.cleaned_data.get("title"))
		print(form.cleaned_data.get("content"))
		instance.save()
		messages.success(request, "Successfully created post", extra_tags='random_tag')
		return HttpResponseRedirect(instance.get_absolute_url())
	elif form.errors:
		messages.error(request, "Could not create post")
	else:
		pass
	context = {
		"form" : form
	}
	return render(request, "post_form.html", context)

def post_update(request, id=None):
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Post Saved</a>", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	elif form.errors:
		messages.error(request, "Could not edit post")
	else:
		pass
	context = {
		"title" : instance.title,
		"instance" : instance,
		"form" : form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	context = {
		"instance" : instance,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	# Ordering by latest post
	# Can also do this in the model directly
	querySet_list = Post.objects.all()#.order_by("-posted")

	paginator = Paginator(querySet_list, 10) # Show 25 querySet per page

	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		querySet = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		querySet = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		querySet = paginator.page(paginator.num_pages)

	context = {
		"listOfPosts" : querySet,
		"function" : "List"
	}
	return render(request, "post_list.html", context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Post deleted successfully")
	return redirect("posts:list")