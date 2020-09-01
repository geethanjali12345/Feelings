from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib.auth import authenticate, login,logout
from .mixins import FormUserNeededMixin
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView,DeleteView
from .forms import UserRegistrationForm,NotesForm,UserProfileForm
from .models import Notes

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

def signup(request):
    # form = UserCreationForm()
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'signup.html',{'form': form})

@login_required
def NotesView(request):
    current_user=request.user
    notes= Notes.objects.filter(user=current_user)
    query=request.GET.get("q",None)
    paginator = Paginator(notes, 3)  # 3 posts in each page
    page = request.GET.get('page',1)
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        notes = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        notes = paginator.page(paginator.num_pages)
    if query is not None:
        notes=Notes.objects.all()
        notes=notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        )
    return render(request,'notes.html',{'user':current_user,'notes':notes})

class AddNotesView(LoginRequiredMixin,CreateView):
    template_name = 'addnotes.html'
    form_class = NotesForm
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title)
        self.object.user = self.request.user
        # self.object.favorite = self.request.user
        self.object.save()
        return redirect(reverse('notes'))

def NoteDetail(request, pk):
    template_name = 'note-detail.html'
    try:
    	post = get_object_or_404(Notes, id=pk)
    except:
    	raise Http404("Blog does not exist.")

    post.save()
    is_liked= False
    if post.favorite.filter(id=request.user.id).exists():
    	is_liked=True
    params = {
		'blog':post,
		'is_liked':is_liked,
		}

    return render(request, template_name, params)

class UpdateNote(LoginRequiredMixin,FormUserNeededMixin,UpdateView):
    model=Notes
    form_class=NotesForm
    # fields=['title','content']
    template_name='updatenote.html'
    success_url="/notes"

    # @method_decorator(login_required(login_url="/accounts/login"))
    # def dispatch(self, *args, **kwargs):
    #     return super(UpdateBlog, self).dispatch(*args, **kwargs)

class DeleteNote(LoginRequiredMixin,DeleteView):
    model=Notes
    template_name='deletenote.html'
    success_url='/notes'

    # @method_decorator(login_required(login_url="/accounts/login"))
    # def dispatch(self, *args, **kwargs):
    #     return super(DeleteBlog, self).dispatch(*args, **kwargs)

def like_post(request):
	post=get_object_or_404(Notes,id=request.POST.get('post_id'))
	is_liked= False
	if post.favorite.filter(id=request.user.id).exists():
		post.favorite.remove(request.user)
		is_liked= False
	else:
		post.favorite.add(request.user)
		is_liked= True
	return redirect(post.get_absolute_url())

# def favNotesList(request):
# 	user=request.user
# 	fav_notes=user.favorite.all()
# 	return render(request,'favourite_notes.html',{'fav_notes':fav_notes})

@login_required
def favNotesList(request):
    user=request.user
    fav_notes=user.favorite.all()
    query=request.GET.get("q",None)
    paginator = Paginator(fav_notes, 3)  # 3 posts in each page
    page = request.GET.get('page',1)
    try:
        fav_notes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        fav_notes = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        fav_notes = paginator.page(paginator.num_pages)
    if query is not None:
        fav_notes=Notes.objects.all()
        fav_notes=fav_notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        )
    return render(request,'favourite_notes.html',{'user':user,'fav_notes':fav_notes})


@login_required
def user_profile(request):
    """Display user profile information."""
    user = request.user
    return render(request, 'profile.html', {'user': user})

class AddProfile(LoginRequiredMixin,FormUserNeededMixin,CreateView):
	# model= Posts
	form_class=UserProfileForm
	template_name='addprofile.html'
	success_url='/profile'

@login_required
def edit_user_profile(request):
    user = request.user
    form2 =UserProfileForm(instance=user.userprofile)
    if request.method == 'POST':
        form2 = UserProfileForm(
            instance=user.userprofile,
            data=request.POST,
            files=request.FILES
        )
        if form2.is_valid():
            form2.save()
            return redirect(reverse('profile'))
    return render(request, 'edit_profile.html',
        {'form': form2})

def signout(request):
    logout(request)
    return redirect('index')