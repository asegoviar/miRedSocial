from django.shortcuts import render

def feed_page(request):
    return render(request, "posts/feed.html")