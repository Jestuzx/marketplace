from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from ..forms import CustomUserCreationForm

User = get_user_model()


class AuthView(View):
    template_name = "users/auth.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # ===================== LOGIN =====================
        if "login" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                user = None

            if user is not None:
                # нужно из-за нескольких backend
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect("profile")
            else:
                return render(
                    request,
                    self.template_name,
                    {"login_error": "Invalid email or password"},
                )

        # ===================== SIGNUP =====================
        elif "signup" in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect("profile")
            else:
                return render(
                    request, self.template_name, {"signup_errors": form.errors}
                )

        # ===================== FALLBACK =====================
        return render(request, self.template_name)
