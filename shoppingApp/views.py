from time import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
import urllib.request
import json
from .forms import SearchForm

def home(request):
    return render(request, 'index.html')

def boards(request):
    # 블로그 글들을 모조리 띄우는 코드
    #posts = Post.objects.all()
    posts = Post.objects.filter().order_by('-date')
    paginator = Paginator(posts, 4)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'board.html', {'posts':posts})

def products(request):
    return render(request, 'product.html')

def create(request):
    if request.method == 'POST' or request.method == 'FILES':
        # 입력 내용을 DB에 저장
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.author = request.user  
            unfinished.save()
            return redirect('boards')
    else:
        # 입력을 받을 수 있는 html을 갖다 주기
        form = PostForm()
    return render(request, 'form_create.html', {'form':form})

def detail(request, post_id):
    # post_id번째 블로그 글을 DB에서 갖고 와서 detail.html로 띄워주는 코드
    post_detail = get_object_or_404(Post, pk=post_id)

    comment_form = CommentForm()

    return render(request, 'detail.html', {'post_detail':post_detail, 'comment_form':comment_form})

def new_comment(request, post_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Post, pk=post_id)
        finished_form.author = request.user  
        finished_form.save()

    return redirect('detail', post_id)

def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('boards')

def edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST' or request.method == 'FILES':
        # 입력 내용을 DB에 저장
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.date = timezone.now()
            post.photo = form.cleaned_data['photo']
            post.save()
            return redirect('detail', post_id)
    else:
        form = PostForm(instance=post)
        context = {
            'form':form,
        }
        return render(request, 'form_edit.html', context)

def delete_comment(request, post_id, com_id):
    com = get_object_or_404(Comment, pk=com_id)
    com.delete()
    return redirect('detail', post_id)

def edit_comment(request, post_id, com_id):
    com = get_object_or_404(Comment, pk=com_id)
    comment_form = CommentForm(instance=com)
    if request.method == "POST":
        update_form = CommentForm(request.POST, instance=com)
        if update_form.is_valid():
            com.date = timezone.now()
            update_form.save()
            return redirect('detail', post_id)
    return render(request, 'comment_edit.html', {'comment_form':comment_form})

def search(request):
    if request.method == 'POST':
        client_id = "iqVIh8Zdgvd3llrxaee3"
        client_secret = "3E7GG3oYPo"
        form = SearchForm(request.POST)
        searchword = request.POST.get('search')
        encText = urllib.parse.quote("{}".format(searchword))
        if form.is_valid():
            url = 'https://openapi.naver.com/v1/search/shop.json?query=' + encText
            assembled_request = urllib.request.Request(url)          
            assembled_request.add_header("X-Naver-Client-Id",client_id)
            assembled_request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(assembled_request)
            rescode = response.getcode()
            if(rescode==200):
                resdata = response.read()
                obj = json.loads(resdata.decode('UTF-8'))
                obj = obj['items']
                return render(request, 'search.html', {'form':form, 'obj':obj})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form':form})