from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.list import ListView, MultipleObjectMixin
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from.models import UserBase, Profile, Review
from.forms import RegistrationForm, UpdateUserForm, UpdateProfileForm, ReviewForm
from .token import account_activation_token
from question.models import Question



class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review.html'

    def form_valid(self, form):
        # Adding the user to the review form
        form.instance.user = self.request.user

        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your Review Has Been Posted!'
        ) 
        return super().form_valid(form)

class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_results.html'
    paginate_by = 4

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'review/review_update.html'
    form_class = ReviewForm

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your Changes Have Been Saved!'
        ) 
        return super().form_valid(form)

    def test_func(self):
            review = self.get_object()
            return True if self.request.user == review.user else False # one line if statement :)

@login_required
def review_delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        review.delete()
    else:
        return HttpResponseForbidden()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




class UserCreateView(CreateView):
    model = UserBase
    form_class = RegistrationForm
    template_name = 'account/registration/registration.html'
    success_url = reverse_lazy('account:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs) 

    def form_valid(self, form):
        user = form.save(self.request)

        # Email Activation Setup
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('account/registration/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)

        # Success message 
        messages.add_message(
            self.request,
            messages.INFO,
            'Check Your Email For Account Activation Link'
        ) 
        return super().form_valid(form)

def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'account/registration/activation_invalid.html')

class ProfileDetailView(DetailView, MultipleObjectMixin):
    model = Profile
    template_name = 'account/profile/profile.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        profile = self.get_object()
        object_list = Question.objects.filter(author=profile.user)
        
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserBase
    template_name = 'account/profile/userbase_confirm_delete.html'
    success_url = reverse_lazy('account:login')

    def delete(self, request, *args, **kwargs):
        user = UserBase.objects.get(slug=self.kwargs['slug'])   
        user.is_active = False
        user.save()

        # Success message 
        messages.add_message(
            self.request,
            messages.ERROR,
            'Your Account Has Been Deleted!'
        ) 
        return HttpResponseRedirect(self.success_url)

    def test_func(self):
            user = self.get_object()
            return True if self.request.user == user else False # one line if statement :)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserBase
    form_class = UpdateUserForm
    template_name = 'account/profile/update_user.html'

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your Changes Have Been Saved!'
        ) 
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
            user = self.get_object()
            return True if self.request.user == user else False # one line if statement :)

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'account/profile/update_profile.html'

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your Changes Have Been Saved!'
        )
        return super().form_valid(form)

    def test_func(self):
            profile = self.get_object()
            return True if self.request.user == profile.user else False # one line if statement :)




class MyPasswordChangeView(PasswordChangeView):
    template_name='account/registration/password_change_form.html'

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Password Reset Successfully!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse('account:profile', kwargs={'slug':user.slug})

class MyPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'account/passwordreset/password_reset_form.html'
    email_template_name='account/passwordreset/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')

    def test_func(self):
        return self.request.user.is_anonymous

class MyPasswordResetDoneView(UserPassesTestMixin, PasswordResetDoneView):
    template_name = 'account/passwordreset/password_reset_done.html'

    def test_func(self):
        return self.request.user.is_anonymous

class MyPasswordResetCompleteView(UserPassesTestMixin, PasswordResetCompleteView):
    template_name = 'account/passwordreset/password_reset_complete.html'

    def test_func(self):
        return self.request.user.is_anonymous



@login_required
def star(request):

    if request.POST.get('action') == 'post':

        result = ''

        id = int(request.POST.get('uid'))
        profile = get_object_or_404(Profile, id=id)

        e = bool
        if profile.stars.filter(id=request.user.id).exists():
            e = True
            profile.stars.remove(request.user)
            profile.star_count -= 1
            result = profile.star_count
            profile.save()
        else:
            e = False
            profile.stars.add(request.user)
            profile.star_count += 1
            result = profile.star_count
            profile.save()

        return JsonResponse({'result':result, 'user':e})

