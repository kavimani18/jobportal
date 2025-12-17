from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from employers.models import JobPost

from .forms import CandidateRegisterForm, ApplicationForm
from .models import JobApplication


# ⭐ Candidate Register
def register(request):
    if request.method == "POST":
        form = CandidateRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('candidates:login')  # Redirect to login page after successful registration
    else:
        form = CandidateRegisterForm()

    return render(request, 'candidates/register.html', {'form': form})


# ⭐ PUBLIC — Show all jobs (no login required)
def all_jobs(request):
    jobs = JobPost.objects.all().order_by('-created_at')
    return render(request, 'candidates/all_jobs.html', {'jobs': jobs})


# ⭐ APPLY — Login Required
@login_required(login_url='candidates:login')
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user   # link logged-in user
            application.save()
            return redirect('candidates:application_success')
    else:
        form = ApplicationForm()

    return render(request, 'candidates/apply_job.html', {
        'form': form,
        'job': job
    })



# ⭐ Application Success Page
@login_required(login_url='candidates:login')
def application_success(request):
    return render(request, 'candidates/app_success.html')


# ⭐ Logout View
def user_logout(request):
    logout(request)
    return redirect('candidates:all_jobs')