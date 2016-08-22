import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.template.defaultfilters import slugify

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'rangosay': "Tam is very handsome"}

    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        #Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            name = form.cleaned_data['name']
            slug = slugify(name)
            if Category.objects.filter(slug=slug).exists():
                form.add_error('name', "This name is not acceptable, duplicate with {0}"\
                                            .format(Category.objects.get(slug=slug).name))
                return render(request, 'rango/add_category.html', {'form': form})

            form.save(commit=True)

            # Now call the index() view
            # The user will be shown the hompage
            return index(request)
        else:
            # The supplied from contained errors- just print
            print form.errors
    else:
        # If the request was not a POST, display the form to enter detail
        form = CategoryForm()

    # Bad form (or form details), no form supplied.
    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probaly better to use a redirect here
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}
    render_page = 'rango/add_page.html' .format(category_name_slug)
    return render(request, render_page, context_dict)

