from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.models import User

def post_list(request):
	#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	posts = Post.objects.order_by('created_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
def post_detail(request, pk):
	#post = Post.objects.get(pk=pk)
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
	
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
	
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
	
#---------------------------------------------------------------------------
# Test1
#---------------------------------------------------------------------------
def post_test1_1(request):
	now  = timezone.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)
	
def post_test1_2(request):
	template = Template('''
	Total Info : {{ MyInfo|length }}<br>
	MyName : {{ MyInfo.name|lower }}<br>
	MyAge : {{ MyInfo.age }}<br>
	MyJob : {{ MyInfo.job|truncatewords:"2" }}<br>
	Address : {{ MyInfo.address|default:"Null Data" }}<br>
	DiskSize : {{ MyInfo.disksize|filesizeformat }}
	''')
	context = Context({'MyInfo': {'name':'KIM SUNG HWAN', 'age':42, 'job':'Game Program and Web Program', 'address':'', 'disksize':1234}})
	html = """
	<html>
		<head>
			<title>3dartmax</title>
		</head>
		<body>{0}</body>
	</html>
	"""
	return HttpResponse(html.format(template.render(context)))
	
def post_test1_3(request):
	template = Template('''
	Total Info : {{ info|length }}<br>
	MyName : {{ info.name|lower }}<br>
	MyAge : {{ info.age }}<br>
	Address : {{ info.address|default:"Null Data" }}
	''')
	class InfoClass: pass
	info         = InfoClass()
	info.name    = 'KIM SUNG HWAN'
	info.age     = 42
	info.address = ''
	context      = Context({'info': info})
	html         = """
	<html>
		<head>
			<title>3dartmax</title>
		</head>
		<body>{0}</body>
	</html>
	"""
	return HttpResponse(html.format(template.render(context)))
	
def post_test1_4(request):
	template = Template("""
	{% include "blog/test.html" with nickname="3dartmax" age=42 datas=posts auths=users %}
	
	{% if posts|length >= 3 %}
		{{ posts.0.title }} / {{ posts.1.title }} / {{ posts.2.title }}
	{% elif posts|length >= 2 %}
		{{ posts.0.title }} / {{ posts.1.title }}
	{% elif posts|length == 1 %}
		{{ posts.0.title }}
	{% endif %}	
	{% for post in posts %}
		{% if forloop.first %}
			<h1>Start - {{ post.title }}</h1>
		{% elif forloop.last %}
			<h1>End - {{ post.title }}</h1>
		{% else %}
			<h1>{{ forloop.counter }} - {{ post.title }}</h1>
		{% endif %}		
		{{ post.text|linebreaks }}
	{% endfor %}
	""")
	context = Context({"posts": Post.objects.order_by('created_date'), "users":User.objects.all()})
	html    = """
	<html>
		<head>
			<title>3dartmax</title>
		</head>
		<body>%s</body>
	</html>
	""" % template.render(context)
	return HttpResponse(html)

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	