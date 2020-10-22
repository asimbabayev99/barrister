from django.shortcuts import render, get_object_or_404, HttpResponse, Http404
from documents.models import *
from documents.utils import Parser, documents
from django.template import Template, Context
import json

# Create your views here.


def temlates_view(request):
    templates = Document.objects.all()

    context = {
        'templates': templates,
    }

    return render(request, 'documents/templates.html', context=context)


def single_template_view(request, id):
    template = get_object_or_404(Document.objects.all(), id=id)
    # html, js = Parser().get_content(template.conf)

    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body)
            t = Template(template.content)
            c = Context(data)
            print(data)
            html = t.render(c)
            return HttpResponse(html)
        else:
            return Http404()
    else:
        t = Template(template.content)
        c = Context(request.POST)
        content = t.render(c)

    context = {
        'template': template,
        # 'html_content': html,
        # 'js_content': js,
        'content': content,
    }

    return render(request, 'documents/single_template.html', context=context)


def test_view(request):

    return render(request, 'documents/test.html')