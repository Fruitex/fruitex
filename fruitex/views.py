from django.shortcuts import render_to_response

def home(request):
    return render_to_response("index.html", {})

def error(request):
    return render_to_response("error.html", {})

def browserNotSupport(request):
    return render_to_response("not_support.html", {})
