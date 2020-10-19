from django.shortcuts import render

# Create your views here.


def temlates_view(request):

    return render(request, 'documents/templates.html')


def single_template_view(request, id):

    return render(request, 'documents/single_tempalate.html')


def test_view(request):

    return render(request, 'documents/test.html')