from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from apps.forms import CreateUserForm, CustomCreateUserForm
from apps.models.user import User
from apps.tasks import send_to_email


class UserView(LoginRequiredMixin, ListView):
    queryset = User.objects.filter(type=User.Type.STUDENT)
    context_object_name = 'students'
    template_name = 'apps/parts/students-list.html'
    ordering = '-id'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        queryset = super().get(request, *args, **kwargs)
        student_id = self.request.GET.get('pk')
        User.objects.filter(id=student_id).delete()
        return queryset


class DetailStudentView(LoginRequiredMixin, DetailView):
    queryset = User.objects.filter(type=User.Type.STUDENT)
    template_name = 'apps/parts/student-detail.html'
    context_object_name = 'student'


class CreateStudentView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'apps/parts/add-student.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        # form.save(commit=False).type = User.Type.STUDENT
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdateStudentView(LoginRequiredMixin, UpdateView):
    form_class = CreateUserForm
    model = User
    template_name = 'apps/parts/student-edit.html'
    context_object_name = 'student'
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TeachersListView(LoginRequiredMixin, ListView):
    template_name = 'apps/parts/teachers-list.html'
    queryset = User.objects.filter(type=User.Type.TEACHER)
    context_object_name = 'teachers'
    ordering = '-id'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        queryset = super().get(request, *args, **kwargs)
        teacher_id = self.request.GET.get('pk')
        User.objects.filter(pk=teacher_id).delete()
        return queryset


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CreateUserForm
    model = User
    template_name = 'apps/parts/teacher-edit.html'
    context_object_name = 'teacher'
    success_url = reverse_lazy('teachers-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'apps/parts/add-teacher.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('teachers-list')

    def form_valid(self, form):
        form.save(commit=False).type = User.Type.TEACHER
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class TeacherDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.filter(type=User.Type.TEACHER)
    template_name = 'apps/parts/teacher-detail.html'
    context_object_name = 'teacher'


class CustomLoginView(LoginView):
    template_name = 'apps/register/login.html'

    def get_success_url(self):
        user: User = self.request.user
        if user.type == User.Type.STUDENT:
            return resolve_url('students-list')
        return resolve_url('home')


class CustomRegisterView(CreateView):
    model = User
    template_name = 'apps/register/register.html'
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('login-page')

    def form_valid(self, form):
        email = form.data['email']
        send_to_email.delay(email)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-page')
