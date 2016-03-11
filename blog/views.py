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
	
	
#---------------------------------------------------------------------------
# Test2
#---------------------------------------------------------------------------
import sys
sys.getfilesystemencoding()

from django.utils.encoding import iri_to_uri, uri_to_iri
from django.utils.http import urlquote

import os
import json
from django.core import serializers
from django.http import JsonResponse, FileResponse

def post_test2_1(request):
	#absname   = os.path.dirname(os.path.abspath(__file__)) + r'\static\text\test.txt'	# 절대경로
	#response  = FileResponse(open(absname, 'rb'))
	#return HttpResponse(response)
	
	#localname = 'blog/static/text/test.txt'											# 상대경로
	#response  = FileResponse(open(localname, 'rb'))
	#return HttpResponse(response)

	#request.encoding = 'koi8-r'
	text = '''name='김성환'&age=43'''
	url  = iri_to_uri(text)
	org  = uri_to_iri(url)
	print('text -> url : ', url)
	print('url -> text : ', org)
	return HttpResponse('')
	
	
def post_test2_2(request):	
	srcData  = {'Name':'김성환'}
	print(srcData)
	jsonData = json.dumps(srcData, ensure_ascii=False)	# utf-8로 생성하기
	print(jsonData)
	destData = json.loads(jsonData)
	print(destData)
	return HttpResponse(destData['Name'])
	
	
def post_test2_3(request):
	#data = {}
	#data['Name'] = '김성환'
	#return HttpResponse(json.dumps(data), content_type='application/json')

	tasks = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:2]
	data = serializers.serialize('json', tasks)
	return HttpResponse(data, content_type='application/json')
	
	
def post_test2_4(request):
	#srcData  = {'Name':'김성환'}
	#response = JsonResponse(srcData, safe=False)
	#print(response.content)
	#return HttpResponse(response.content)
	
	destData = json.loads(uri_to_iri(b'''{"Name": "\uae40\uc131\ud658"}'''))
	#destData = json.loads('''{"Name": "김성환"}''')
	print(destData)
	return HttpResponse(destData['Name'])

	
#---------------------------------------------------------------------------
# Test3
#---------------------------------------------------------------------------
# http://127.0.0.1:8000/post/test3_1/?name=%EA%B9%80%EC%84%B1%ED%99%98&age=43	
# http://127.0.0.1:8000/post/test3_1/?name=김성환&age=43
def post_test3_1(request):
	print(uri_to_iri('http://127.0.0.1:8000/post/test3_1/?name=%EA%B9%80%EC%84%B1%ED%99%98&age=43'))
	print(iri_to_uri('http://127.0.0.1:8000/post/test3_1/?name=김성환&age=43'))
	print('경로명 합치기 : ', os.path.join(r'D:\WorkRoom', r'Django', r'girls\blog'))			# D:\WorkRoom\Django\girls\blog
	print('중간 경로 슬래쉬 제거 : ', os.path.normpath(r'D:\WorkRoom\Django\..\girls\blog'))	# D:\WorkRoom\girls\blog
	
	currpath   = os.getcwd()
	absolutely = os.path.abspath(__file__)
	relatively = os.path.relpath(absolutely, currpath)
	dirname    = os.path.dirname(absolutely)
	filename   = os.path.basename(__file__)
	name       = request.GET.get('name', '')
	age        = request.GET.get('age', 0)
	template   = Template('''
	<html>
		<head>
			<title>{{ module_name }}</title>
		</head>
		<body>
			<ol>				
				<li><strong>현재 실행경로 : {{ currpath }}</strong></li>
				<li><strong>파일 절대경로 : {{ absolutely }}</strong></li>
				<li><strong>파일 상대경로 : {{ relatively }}</strong></li>
				<li><strong>폴더 절대경로 : {{ dirname }}</strong></li>
				<li><strong>파일명 : {{ filename }}</strong></li>
				<li><strong>이름 : {{ name }}</strong></li>
				<li><strong>나이 : {{ age }}</strong></li>
			</ol>
		</body>
	</html>
	''')
	context = Context({
		'module_name':__name__,
		'currpath':currpath.replace('\\', '/'),
		'absolutely':absolutely.replace('\\', '/'),
		'relatively':relatively.replace('\\', '/'),
		'dirname':dirname.replace('\\', '/'),
		'filename':filename,
		'name':name,
		'age':age})
	return HttpResponse(template.render(context))

	
import csv
from django.contrib.auth.models import User

# db테이블 정보로 csv파일 만들어 다운로드 받기.
def post_test3_2(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="posts.csv"'
	writer = csv.writer(response)
	posts  = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:10]
	for post in posts:
		user = User.objects.get(id=post.author_id)
		writer.writerow([post.id, post.title, post.created_date, post.published_date, user.username])
	return response


# csv파일을 웹페이지로 보여주기.
def post_test3_3(request):
	file  = open('blog/static/csv/test.csv', 'r', encoding='utf-8')
	datas = list()
	text  = file.readline()
	while text:
		data  = list()
		texts = text.split(',')
		for t in texts:
			data.append(t)
		if len(texts) > 0:
			datas.append(data)
		text = file.readline()
	file.close()
	print(datas)
	template = Template('''
	<html>
		<head>
			<title>{{ module_name }}</title>
		</head>
		<body>
			<ol>
				{% with ',' as split %}
				{% for data in datas %}
					<li><strong>
						{% for column in data %}
							{{ column }}
							{% if not forloop.last %}
								{{ split }}
							{% endif %}
						{% endfor %}
					</strong></li>
				{% endfor %}
				{% endwith %}
			</ol>
		</body>
	</html>
	''')
	context = Context({
		'module_name':__name__,
		'datas':datas})
	return HttpResponse(template.render(context))


# 이미지 파일을 읽어왔어 다운로드 할 수 있게 해준다.
def post_test3_4(request):
	file  = open('blog/static/image/rin01.png', 'rb')
	return HttpResponse(file.read(), content_type='image/png')

