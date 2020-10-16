from django.shortcuts import render

# Create your views here.


def index_view(request):

    return render(request, 'documents/index.html')



def test_view(request):

    return render(request, 'documents/test.html')