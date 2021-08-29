from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, FormView, View
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_unicorn.components import UnicornView
from django.contrib.auth.decorators import login_required

import json

from .forms import QuestionCraetionForm, QuestionSearchForm, CommentCreateForm, QuestionUpdateForm
from .models import Question, Comment
from account.models import UserBase
from programmingLanguage.models import Category


# Question CRUD
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'question/question_create.html'
    form_class = QuestionCraetionForm

    # Adding the author to the question form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionListView(ListView):
    model = Question
    template_name = 'question/question_list.html'
    paginate_by = 6
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = Category.objects.root_nodes()
        count = Question.objects.count()
        question_likes = Question.objects.all().order_by('-like_count') 

        context['category'] = category
        context['count'] = count
        context['question_likes'] = question_likes[:6]
        return context
        
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'question/question_update.html'
    form_class = QuestionUpdateForm

    def form_valid(self, form):
        # Success message 
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your Changes Have Been Saved!'
        ) 
        return super().form_valid(form)

    def test_func(self):
            question = self.get_object()
            return True if self.request.user == question.author else False # one line if statement :)

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'question/question_delete.html'

    def delete(self, request, *args, **kwargs):
        # Success message 
        messages.add_message(
            self.request,
            messages.ERROR,
            'The Question Has Been Deleted!'
        ) 
        return super().delete(request, *args, **kwargs)

    def test_func(self):
            question = self.get_object()
            return True if self.request.user == question.author else False # one line if statement :)

    def get_success_url(self):
        user = self.request.user
        return reverse('question:user_question_list', kwargs={'slug':user.slug})



# Comments + Question Detail view
# class QuestionDetailView(DetailView):
#     model = Question
#     template_name = 'question/question_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         question = self.object
#         comments = question.comments.all
#         context['comments'] = comments
#         context['form'] = CommentCreateForm
#         return context

# class UserCommentForm(LoginRequiredMixin, CreateView):
#     template_name = 'question/question_detail.html'
#     form_class = CommentCreateForm
#     model = Comment

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         # question = Question.objects.get(slug=self.kwargs.get('slug'))
#         # form.instance.question = question

#         result = form.cleaned_data.get('content')
#         user = request.user.username
#         return JsonResponse({'result':result, 'user':user})
#         # return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('question:question_detail', kwargs={'slug': self.object.question.slug})



# class QuestionView(View):
#     def get(self, request, *args, **kwargs):
#         view = question_detail
#         return view(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         view = add_comment
#         return view(request, *args, **kwargs)



def question_detail(request, slug):

    question = get_object_or_404(Question, slug=slug)

    allcomments = question.comments.all()

    comment_form = CommentCreateForm()

    return render(request, 'question/question_detail.html', {'question': question, 'form': comment_form, 'comments': allcomments})


def add_comment(request):

    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            c = Comment.objects.get(id=id)
            # question = c.question
            # count = question.comments.all().count()
            children = c.get_children()
            cc = []
            for child in children:
                cc.append(child.id)
                children2 = child.get_children()
                if children2:
                    for child2 in children2:
                        cc.append(child2.id)
                        children3 = child2.get_children()
                        if children3:
                            for child3 in children3:
                                cc.append(child3.id)

            c.delete()
            length = len(cc)
            return JsonResponse({'remove': id, 'children':cc, 'len':length})

        else:
            form = CommentCreateForm(request.POST)
            if form.is_valid():
                user_comment = form.save(commit=False)
                result = form.cleaned_data.get('content')
                user = request.user
                user_comment.author = user
                user_comment.save()
                return JsonResponse({'result': result, 'username': user.username})
            
    return JsonResponse({"result":''})

# User / Category Questions
class UserQuestionDetailView(DetailView, MultipleObjectMixin):
    model = UserBase
    template_name = 'question/user_question_list.html'
    paginate_by = 6
    
    # To add an object_list so we can paginate the objects
    def get_context_data(self, **kwargs):
        object_list = Question.objects.filter(author=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context

class CategoryQuestionDetailView(DetailView, MultipleObjectMixin):
    model = Category
    template_name = 'question/category_question_list.html'
    paginate_by = 6

    # To add an object_list so we can paginate the objects
    def get_context_data(self, **kwargs):
        object_list = Question.objects.filter(tags=self.object)
        
        # To get the number of all questions in root+children category 
        q_set = set(object_list)

        if not self.object.is_leaf_node():
            children = self.object.get_children()

            for child in children:
                questions = Question.objects.filter(tags=child)
                for question in questions:
                    q_set.add(question)

        object_list = list(q_set)
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['questions'] = object_list            
        return context
    

# Search Function
def question_search(request):
    form = QuestionSearchForm()

    q = ''
    c = ''
    a = ''
    results = []


    if 'query' in request.GET:
        form = QuestionSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['query']
            c = form.cleaned_data['tags']
            a = form.cleaned_data['username']


        
            if c is not None and a :
                m, a = username_check(username=a)
                
                if m == 'no':
                    messages.add_message(request, messages.ERROR,f'Author "{a}" not found.. please type in a correct username') 
                    return render(request, 'question/search.html',{'form':form, 'query': q, 'results': results, 'tag':c, 'author2':a})
            
                else:    
                    results = Question.objects.filter(author=a).filter(tags=c).filter(title__contains=q)

            elif c is None and a :
                m, a = username_check(username=a)
                
                if m == 'no':
                    messages.add_message(request, messages.ERROR,f'Author "{a}" not found.. please type in a correct username') 
                    return render(request, 'question/search.html',{'form':form, 'query': q, 'results': results, 'tag':c, 'author2':a})
            
                else:    
                    results = Question.objects.filter(author=a).filter(title__contains=q)

            elif c is not None and not a  :
                results = Question.objects.filter(tags=c).filter(title__contains=q)

            else :
                results = Question.objects.filter(title__contains=q)

    return render(request, 'question/search.html',{'form':form, 'query': q, 'results': results, 'tag':c, 'author':a})

# Username Validation
def username_check(username):

    authors = UserBase.objects.all()
    usernames = []

    for author in authors:
        usernames.append(author.username)

    if username in usernames:
        author = UserBase.objects.get(username=username)
        m = 'yes'
        return m, author
    else:
        m = 'no'
        return  m, username

@login_required
def like(request):

    if request.POST.get('action') == 'post':

        result = ''

        id = int(request.POST.get('qid'))
        question = get_object_or_404(Question, id=id)

        e = bool
        if question.likes.filter(id=request.user.id).exists():
            e = True
            question.likes.remove(request.user)
            question.like_count -= 1
            result = question.like_count
            question.save()
        else:
            e = False
            question.likes.add(request.user)
            question.like_count += 1
            result = question.like_count
            question.save()

        return JsonResponse({'result':result, 'user':e})