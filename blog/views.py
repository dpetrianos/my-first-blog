from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment   # connecting to database
from .forms import PostForm, CommentForm, UserForm
import ctypes  # An included library with Python install.
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
# from django.contrib.auth import authenticate, login, logout

WS_EX_TOPMOST = 0x40000
MB_DEFAULT_DESKTOP_ONLY = 0x00020000
MB_YESNO = 0x00000004
MB_ICONWARNING = 0x00000030
STYLE = MB_YESNO | MB_ICONWARNING | MB_DEFAULT_DESKTOP_ONLY | WS_EX_TOPMOST

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style) 
    # ctypes.windll.user32.MessageBoxW()

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ep = Mbox('Warning! ', 'Are you sure for deleting this blog ?', STYLE)       #48+4
    
    if (ep==6):
        Mbox('The answer is YES  6 ', str(ep), STYLE)
        post.delete()
    return redirect('post_list')

##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | Cancel 
##  6 : Cancel | Try Again | Continue    

# Create your views here.

def post_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print("------- starting -------")
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    if not posts :
        # messages.info(request, 'No Posts yet !!!')
        return render(request, 'blog/post_list.html', {'username':User.username})
    else:
        n_comments = []
        # for post in posts:
        #     comments = Comment.objects.filter(post=post).count()
        #     post.ncomments = comments
        #     post.save()
        #     n_comments.append(comments)

        return render(request, 'blog/post_list.html', {'posts' : posts})
        # return render(request, 'blog/post_list.html', {'posts' : posts, 'comments' : n_comments})


def post_draft_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.filter(published_date__isnull=True).filter(author=request.user).order_by('created_date')
    if not posts :
        return render(request, 'blog/post_list.html', {'username':User.username})
    else:
        return render(request, 'blog/post_draft_list.html', {'posts' : posts})

def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=pk)
    paginator = Paginator(comments, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_detail.html', {'page_obj' : page_obj , 'post' : post})    
    return render(request, 'blog/post_detail.html', {'comments' : comments , 'post' : post})    



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def addcomment(request, pk):
    if request.method == 'POST':
        comment = request.POST['newcomment']
        post = get_object_or_404(Post, pk=pk)
        result = Comment.objects.create(author=request.user, post_id=pk, text=comment)      
        # print(result)
        comments = Comment.objects.filter(post=post).count()
        post.ncomments = comments
        post.save()
    return redirect('post_detail', pk=post.pk)
    # return render(request, 'blog/post_detail.html', {'comments' : comments , 'post' : post})    
    # return render(request, 'blog/post_detail.html')


def login(request):
    if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         user1 = form.save(commit=False)
    #         print("--")
    #         print(user1.username)
    #         print(user1.password)
    #         print("--")
    #         if User.objects.filter(username = user1.username).exists():
    #             if User.objects.filter(password = user1.password).exists():
    #                 print("+++")
    #                 return redirect('/')
    #         return redirect('login')
    # else:
    #     form = UserForm()
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials are Invalid')   #Λάθος στα στοιχεία εισόδου
            return redirect('login')


        # if User.objects.filter(username=username).exists() == False:
        #     messages.info(request, 'Username does not exists !!')
        #     return redirect('login')
        # elif User.objects.filter(password=password).exists() == False:
        #     messages.info(request, 'Username does not exists !!')
        #     return redirect('login')
        # else:
        #     print('----')
        #     print(username)
        #     print('----')
        #     return redirect('/')

    # return render(request, 'blog/login.html', {'form': form})
    return render(request, 'blog/login.html', {})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
        return redirect('login')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used !!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used !!')
                return redirect('register')
            else :
                # user = form.save(commit=False)
                user = User.objects.create_user(username=username, email=email, password=password)
                # user = User.objects.create(username=username, email=email, password=password)                
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords are not the same')
            return redirect('register')
    else:
        return render(request, 'blog/register.html')

