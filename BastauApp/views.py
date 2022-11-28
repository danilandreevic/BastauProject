from .permissions import *
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView, DeleteView

from django.contrib.auth import logout, login
from .filters import CaseFilter
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
menu = [
    {'title': 'Партнеры', 'url_name': 'partners'},
    {'title': 'Кейсы', 'url_name': 'showcases'},
    {'title': 'Победители', 'url_name': 'ListWinners'},
]
def register(request):
    context = {}
    # add the dictionary during initialization
    context["menu"] = menu

    return render(request, "register.html", context)

class Categories(ListView):
    def get_cat(self):
        return Category.objects.all()


def logout_user(request):
    logout(request)
    return redirect('login')


def personal(request):
    context = {}
    # add the dictionary during initialization
    context["menu"] = menu

    return render(request, "personal.html", context)

class ListWinners(ListView):
    # now = datetime.datetime.now()
    model = Answer
    template_name = 'ListWinners.html'
    paginate_by = 6
    extra_context = {"name": 'Победители', 'menu': menu}

    def get_queryset(self):
        queryset = Answer.objects.filter(status='Победа')
        return queryset

def index(request):
    context = {'menu': menu}
    context['data'] = Case.objects.order_by("-id")[0:6]
    context['partners'] = Partner.objects.order_by("-Fio")[0:3]
    case_count = Case.objects.count()
    string_case_count = str(case_count)
    context['string_case_count'] = string_case_count

    return render(request, 'index.html', context)


def about(request):
    context = {'menu': menu}
    return render(request, 'about.html',context)

class createcase( CreateView):
    model = Case
    form_class = AddCaseForm
    template_name = 'createcase.html'
    success_url = "/showcases"
    # context_object_name = "partners"
    extra_context = {
        'menu': menu,
    }

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user_id = Partner.objects.get(user=self.request.user)
        self.object.save()
        return super().form_valid(form)

class ShowCases(ListView):
    # now = datetime.datetime.now()
    model = Case
    template_name = 'ShowCase.html'
    paginate_by = 6
    context_object_name = 'orders'
    extra_context = {"name": 'Кейсы', 'menu': menu}

    def get_queryset(self):
        now = datetime.datetime.now()
        qs = Case.objects.all().filter(is_published=True, date_of_close__gte=now)
        case = CaseFilter(self.request.GET, queryset=qs)
        return case.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CaseFilter(self.request.GET, queryset=self.get_queryset())
        return context

class ShowCasesPartner(ListView):
    model = Case
    context_object_name = 'cases'
    template_name = 'casepartners.html'
    extra_context = {'menu': menu}
    paginate_by = 6

    def get_queryset(self):
        now = datetime.datetime.now()
        queryset = Case.objects.filter(user_id=self.request.user.partner,is_published=True, date_of_close__gte=now)
        return queryset

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        queryset = Case.objects.filter(user_id=self.request.user.partner, is_published=False)
        qs = Case.objects.filter(user_id=self.request.user.partner, date_of_close__lte=now)
        superqs = queryset | qs
        context = super().get_context_data(**kwargs)
        context['total_active_records'] = Case.objects.filter(user_id=self.request.user.partner,is_published=True, date_of_close__gte=now).count()
        context['all_cases'] = Case.objects.filter(user_id=self.request.user.partner).count()
        context['case_isnt_published'] = superqs.count()
        return context

class ShowArchive(ListView):
    model = Case
    context_object_name = 'cases'
    template_name = 'casepartnersnotpub.html'
    extra_context = {'menu': menu}
    paginate_by = 6

    def get_queryset(self):
        now = datetime.datetime.now()
        queryset = Case.objects.filter(user_id=self.request.user.partner,is_published=False)
        qs = Case.objects.filter(user_id=self.request.user.partner, date_of_close__lte=now)

        return queryset | qs

    def get_context_data(self, **kwargs):
        now = datetime.datetime.now()
        queryset = Case.objects.filter(user_id=self.request.user.partner, is_published=False)
        qs = Case.objects.filter(user_id=self.request.user.partner, date_of_close__lte=now)
        superqs = queryset | qs

        context = super().get_context_data(**kwargs)
        context['total_active_records'] = Case.objects.filter(user_id=self.request.user.partner,is_published=True, date_of_close__gte=now).count()
        context['all_cases'] = Case.objects.filter(user_id=self.request.user.partner).count()
        context['case_isnt_published'] = superqs.count()
        return context

def detail_view(request, case_id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    # add the dictionary during initialization

    context["data"] = Case.objects.get(pk=case_id)
    context["menu"] = menu

    return render(request, "DetailCase.html", context)

def detail_view_for_Partner(request, case_id):
    context = {}
    # add the dictionary during initialization
    context["data"] = Case.objects.get(pk=case_id)
    context["menu"] = menu

    return render(request, "DetailCaseOfPartner.html", context)

class ShowPartners(ListView):
    model = Partner
    template_name = 'partners.html'
    paginate_by = 6
    extra_context = {'name': 'Партнеры', 'menu': menu}

class LoginUser(LoginView):
    form = LoginUserForm
    template_name = "login.html"
    extra_context = {'menu': menu}

    def get_success_url(self):
        return reverse_lazy('index')

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_register.html'
    extra_context = {'menu':menu}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class partner_register(CreateView):
    model = User
    form_class = PartnerSignUpForm
    template_name = 'partner_register.html'
    extra_context = {'menu': menu}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class student_update(PartnerPermissionMixin, UpdateView):
    model = Student
    fields = ['Fio', 'Educational_institution', 'age', 'region', 'Direction_of_study', 'Education']
    template_name = 'personal.html'
    context_object_name = 'student'
    success_url = "/"
    extra_context = {'menu': menu}


class partner_update(PartnerPermissionMixin,UpdateView):
    model = Partner
    fields = ['Fio', 'name_of_partner', 'site', 'avatar', 'about_company']
    success_url = "/"
    context_object_name = 'partner'
    template_name = 'personal_partner.html'
    extra_context = {'menu': menu}

class case_update(CaseCreateUpdateDeletePermissionMixin, UpdateView):
    model = Case
    fields = ['title', 'description', 'category', 'file', 'region', 'is_published', 'tags']
    success_url = "/mycases"
    template_name = 'updatecase.html'
    extra_context = {'menu': menu}

class answer_update(AnswerCreateUpdateDeletePermissionMixin, UpdateView):
    model = Answer
    fields = ['Url', 'File']
    success_url = "/answers"
    template_name = 'updateAnswer.html'
    extra_context = {'menu': menu}

class delete_case(CaseCreateUpdateDeletePermissionMixin, DeleteView):
    model = Case
    template_name = 'delete_case.html'
    success_url = "/mycases"
    extra_context = {'menu': menu}

class AnswerToCase(FormMixin, DetailView):
    model = Case
    template_name = 'addanswer.html'
    form_class = AddAnswer
    success_url = '/'
    context_object_name = 'get_case'
    extra_context = {'menu': menu}
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.id_case = self.get_object()
        self.object.id_student = Student.objects.get(user=self.request.user)
        self.object.is_won = False
        self.object.status = 'Ожидание'
        self.object.save()
        return super().form_valid(form)




class delete_answer(AnswerCreateUpdateDeletePermissionMixin, DeleteView):
    model = Answer
    template_name = 'delete_answer.html'
    success_url = "/answers"
    extra_context = {'menu': menu}

class ShowAnswer(CaseCreateUpdateDeletePermissionMixin, DetailView):
    model = Case
    template_name = 'showanswer.html'

    def get_context_data(self, **kwargs):
            context = super(ShowAnswer, self).get_context_data(**kwargs)
            context['data'] =Case.objects.get(id=self.kwargs.get('pk'))

            context["menu"] = menu
            context['answer_victory'] = Answer.objects.filter(id_case=self.kwargs.get('pk'), status='Победа').count()
            context['answer_waiting'] = Answer.objects.filter(id_case=self.kwargs.get('pk'), status='Ожидание').count()
            context['all_answer'] = Answer.objects.filter(id_case=self.kwargs.get('pk')).count()
            context['answer_defeat'] = Answer.objects.filter(id_case=self.kwargs.get('pk'), status='Отказ').count()
            return context
# def ShowAnswer(request, case_id):
#     context = {}
#     # add the dictionary during initialization
#     context["data"] = Case.objects.get(pk=case_id)
#     context["menu"] = menu
#     context['answer_victory'] = Answer.objects.filter(id_case=case_id, status='Победа').count()
#     context['answer_waiting'] = Answer.objects.filter(id_case=case_id, status='Ожидание').count()
#     context['all_answer'] = Answer.objects.filter(id_case=case_id).count()
#     context['answer_defeat'] = Answer.objects.filter(id_case=case_id, status='Отказ').count()
#     return render(request,'showanswer.html', context)

class ShowAnswerStudent(ListView):
    model = Answer
    template_name = 'showanswer_student.html'
    now = datetime.datetime.now()
    extra_context = {'name': 'Ответы', 'menu': menu, 'now': now}

    def get_queryset(self):
        queryset = Answer.objects.filter(id_student=self.request.user.student)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_victory'] = Answer.objects.filter(id_student=self.request.user.student,status='Победа').count()
        context['answer_waiting'] = Answer.objects.filter(id_student=self.request.user.student, status='Ожидание').count()
        context['all_answer'] = Answer.objects.filter(id_student=self.request.user.student).count()
        context['answer_defeat'] = Answer.objects.filter(id_student=self.request.user.student,status='Отказ').count()
        return context

class ShowAnswerStudentStatusVictory(ListView):
    model = Answer
    template_name = 'answers_status/status_victory.html'
    now = datetime.datetime.now()
    extra_context = {'name': 'Ответы', 'menu': menu, 'now': now}

    def get_queryset(self):
        queryset = Answer.objects.filter(id_student=self.request.user.student, status='Победа')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_victory'] = Answer.objects.filter(id_student=self.request.user.student,status='Победа').count()
        context['answer_waiting'] = Answer.objects.filter(id_student=self.request.user.student, status='Ожидание').count()
        context['all_answer'] = Answer.objects.filter(id_student=self.request.user.student).count()
        context['answer_defeat'] = Answer.objects.filter(id_student=self.request.user.student,status='Отказ').count()
        return context

class ShowAnswerStudentStatusDefeat(ListView):
    model = Answer
    template_name = 'answers_status/status_defeat.html'
    now = datetime.datetime.now()
    extra_context = {'name': 'Ответы', 'menu': menu, 'now': now}

    def get_queryset(self):
        queryset = Answer.objects.filter(id_student=self.request.user.student, status='Отказ')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_victory'] = Answer.objects.filter(id_student=self.request.user.student,status='Победа').count()
        context['answer_waiting'] = Answer.objects.filter(id_student=self.request.user.student, status='Ожидание').count()
        context['all_answer'] = Answer.objects.filter(id_student=self.request.user.student).count()
        context['answer_defeat'] = Answer.objects.filter(id_student=self.request.user.student,status='Отказ').count()
        return context

class ShowAnswerStudentStatusWaiting(ListView):
    model = Answer
    template_name = 'answers_status/status_waiting.html'
    now = datetime.datetime.now()
    extra_context = {'name': 'Ответы', 'menu': menu, 'now': now}

    def get_queryset(self):
        queryset = Answer.objects.filter(id_student=self.request.user.student, status='Ожидание')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_victory'] = Answer.objects.filter(id_student=self.request.user.student,status='Победа').count()
        context['answer_waiting'] = Answer.objects.filter(id_student=self.request.user.student, status='Ожидание').count()
        context['all_answer'] = Answer.objects.filter(id_student=self.request.user.student).count()
        context['answer_defeat'] = Answer.objects.filter(id_student=self.request.user.student,status='Отказ').count()
        return context

def detail_student(request, user_id):
    a = User.objects.get(pk=user_id)
    context = {}
    context["student_info"] = Student.objects.get(user=a)
    context["menu"] = menu
    return render(request, "Bio_student.html", context)

def detail_partner(request, user_id):
    a = User.objects.get(pk=user_id)
    context = {}
    context["partner_info"] = Partner.objects.get(user=a)
    context["menu"] = menu
    return render(request, "Bio_partner.html", context)


class TagIndexView(ListView):
    template_name = 'ShowCase.html'
    model = Case
    extra_context = {'name': 'Партнеры', 'menu': menu}
    def get_queryset(self):
        queryset = Case.objects.filter(tags__slug= self.kwargs.get('tag_slug'))
        return queryset

class PasswordResetViewBastau(PasswordResetView):
    template_name = "reset_password/password_reset.html"
    extra_context = {'menu': menu}

class PasswordResetDoneViewBastau(PasswordResetDoneView):
    template_name="reset_password/password_reset_sent.html"
    extra_context = {'menu': menu}

class PasswordResetConfirmViewBastau(PasswordResetConfirmView):
    template_name="reset_password/password_reset_form.html"
    extra_context = {'menu': menu}

class PasswordResetCompleteViewBastau(PasswordResetCompleteView):
    template_name = "reset_password/password_reset_done.html"
    extra_context = {'menu': menu}


class Winner(WinnerUpdateMixin, UpdateView):
    model = Answer
    fields = ['status',]
    success_url = "/"
    context_object_name = 'partner'
    template_name = 'updatewinner.html'
    extra_context = {'menu': menu}
