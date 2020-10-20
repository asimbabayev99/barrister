from django.shortcuts import render, get_object_or_404
from documents.models import *
from documents.utils import Parser, documents
from django.template import Template

# Create your views here.


def temlates_view(request):
    templates = Document.objects.all()

    context = {
        'templates': templates,
    }

    return render(request, 'documents/templates.html', context=context)


def single_template_view(request, id):
    template = get_object_or_404(Document.objects.all(), id=id)
    html, js = Parser().get_content(documents['nikah'])

    if request.method == "POST":
        t = template.Template(content)
        c = template.Context(request.data)
        html = t.render(c)
        return html

    context = {
        'template': template,
        'html_content': html,
        'js_content': js,
    }

    return render(request, 'documents/single_template.html', context=context)


def test_view(request):

    return render(request, 'documents/test.html')