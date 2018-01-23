# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page 
from rango.forms import CategoryForm
from rango.forms import PageForm

def add_page(request, category_name_url):

	context = RequestContext(request)
	category_name = decode_url(category_name_url)

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)
			cat = Category.objects.get(name=category_name)
			page.category = cat
			page.views = 0
			page.save()

			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response('rango/add_page.html', {'category_name_url': category_name_url, 'category_name': category_name, 'form': form}, context)

def add_category(request):

	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():

			form.save(commit=True)

			return index(request)

		else:
			print form.errors

	else:
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form':form}, context)

def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]

	context_dict = {'categories': category_list, 'pages': page_list}

	for category in category_list:
		category.url = category.name.replace(' ', '_')

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	context_dict = {'boldmessage': "Here is the about page."}
	return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):

	context = RequestContext(request)
	category_name = category_name_url.replace('_', ' ')
	context_dict = {'category_name': category_name}

	try:
		category = Category.objects.get(name=category_name)

		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
		context_dict['category_name_url'] = category_name_url

	except Category.DoesNotExist:
		pass

	return render_to_response('rango/category.html', context_dict, context)

def decode_url(category_name_or_url):
	if '_' in category_name_or_url:
		return category_name_or_url.replace('_', ' ')
	else:
		return category_name_or_url.replace(' ', '_')