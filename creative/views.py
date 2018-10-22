from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from creative.forms import SignUpForm
from creative.forms import UserForm
from creative.forms import ProfileForm
from creative.forms import StoryUpdate
from creative.forms import CommentForm
from creative.tokens import account_activation_token
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from django.http import HttpResponse , HttpResponseRedirect ,Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView ,UpdateView
from .models import Story
from .models import Chapter
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth import logout








# login view
def LoginView(request,method='POST'):
	next = request.GET.get('next', 'http://127.0.0.1:8000/creative/story/list/')
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)
	user = authenticate(username=username, password=password)
	if request.method == 'POST':
		if user is not None and user.is_active:
			login(request, user)
			return HttpResponseRedirect(next)
		else:
			return HttpResponse("Invalid login. Please try again.")	
	return render(request, 'login.html ')

def LogoutView(request):
    logout(request)
    




# registration view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
    'domain': current_site.domain,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
    'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registartion.html', {'form': form})


#account activation view
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('update')
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

# update user profile
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None , request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('update')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,'instance':request.user.profile
    })

# create story
class StoryCreate(CreateView):
    model = Story
    fields = ['title','resume','genres','langues','image']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StoryCreate, self).form_valid(form)
  
    

# create chapter
class ChapterCreate(CreateView):
    model = Chapter
    fields = ['title_chap','content']
    success_url = reverse_lazy('story-user-list')

    def form_valid(self, form):
        form.instance.story_id = self.kwargs.get('pk')
        return super(ChapterCreate, self).form_valid(form)

#Show list of stories created by the user
class StoryUser(ListView):

    model = Story
    paginate_by = 10
    queryset = Story.objects.all()


    
    def get_queryset(self):
        queryset = super(StoryUser, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset    


#update story

def story_update(request, pk):
    
    instance = get_object_or_404(Story, pk=pk)
    form = StoryUpdate(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "story": instance,
        "form":form,
    }
    return render(request, "creative/story_update_form.html", context) 

# update chapter

class ChapterUpdate(UpdateView):
    model = Chapter
    fields = ['title_chap','content']
    success_url = reverse_lazy('creative/story_update_form')      

#show list of all stories
class StoryList(ListView):

    model = Story
    template_name_suffix = '_all_form'
    paginate_by = 10
    queryset = Story.objects.all()

# add a comment to a story
def add_comment_to_post(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user
            comment.save()
            return redirect('story-detail', pk=story.pk)
    else:
        form = CommentForm()
    return render(request, 'creative/add_comment.html', {'form': form})

# see details of a story
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'creative/read_story.html', {'story': story})

#read the desired chapter
def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'creative/chapter_detail.html', {'chapter': chapter}) 

