from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BlogForm
from .models import Blog
from account.models import User
from django.contrib.auth.decorators import login_required

# home view = my blog list


@login_required(login_url='/account/login/')
def homeView(request):
    user = User.objects.get(id=request.user.id)
    myBlogList = user.blog_set.all()
    return render(request, 'blog/home.html', {"myBlogList": myBlogList})


@login_required(login_url='/account/login/')
def blogDetails(request, pk):
    try:
        blog = Blog.objects.get(blogger=request.user, id=pk)
        return render(request, 'blog/details.html', {"blog": blog})
    except:
        messages.error(request, "You cannot access this!")
        return redirect('/')

# create new blog


@login_required(login_url='/account/login/')
def createBlog(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        form.instance.blogger = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "New Blog created!")
            return redirect('/')
    context = {'form': form}
    return render(request, "blog/blog_form.html", context)

# update blog


@login_required(login_url='/account/login/')
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if blog.blogger == request.user:
        form = BlogForm(instance=blog)

        if request.method == "POST":
            form = BlogForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, "blog/blog_form.html", context)
    else:
        messages.error(request, "Your can't update it!")
        return redirect('/')
# delete blog


@login_required(login_url='/account/login/')
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if blog.blogger == request.user:
        if request.method == "POST":
            blog.delete()
            messages.success(request, "Blog Deleted!")
            return redirect('home')

        return render(request, "blog/delete.html", {'obj': blog})
    else:
        messages.error(request, "Your can't update it!")
        return redirect('/')
