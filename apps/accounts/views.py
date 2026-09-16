from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import View


class StaffCreateView(View):

    def get(self, request, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        return render(
            request,
            "accounts/staff_create.html"
        )

    def post(self, request, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password or not role:
            messages.error(
                request,
                "Username, password, and staff role are required."
            )
            return redirect("accounts:staff_create")

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "A user with this username already exists."
            )
            return redirect("accounts:staff_create")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("accounts:staff_create")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_staff = True
        user.is_active = True
        user.save()
        group = Group.objects.filter(name=role).first()

        if group:
            user.groups.add(group)

        messages.success(
            request,
            f"Staff account for {username} was created successfully."
        )

        return redirect("dashboard:home")

    
class StaffListView(View):

    def get(self, request, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        staff_members = (
            User.objects
            .filter(is_staff=True)
            .order_by("first_name", "last_name", "username")
        )

        return render(
            request,
            "accounts/staff_list.html",
            {
                "staff_members": staff_members,
            },
        )

class StaffEditView(View):

    def get(self, request, pk, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        try:
            staff_member = User.objects.get(
                pk=pk,
                is_staff=True,
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Staff member not found."
            )

            return redirect("accounts:staff_list")

        # Normal staff members cannot edit superuser accounts.
        if (
            staff_member.is_superuser
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "You are not permitted to edit an administrator account."
            )

            return redirect("accounts:staff_list")

        return render(
            request,
            "accounts/staff_edit.html",
            {
                "staff_member": staff_member,
            },
        )


    def post(self, request, pk, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        try:
            staff_member = User.objects.get(
                pk=pk,
                is_staff=True,
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Staff member not found."
            )

            return redirect("accounts:staff_list")


        # Normal staff members cannot modify superuser accounts.
        if (
            staff_member.is_superuser
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "You are not permitted to modify an administrator account."
            )

            return redirect("accounts:staff_list")


        username = request.POST.get(
            "username",
            ""
        ).strip()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        is_active = request.POST.get(
            "is_active"
        ) == "on"

        role = request.POST.get("role", "").strip()

        staff_member.save()

        staff_member.groups.clear()

        if role:
            group = Group.objects.filter(name=role).first()

            if group:
                staff_member.groups.add(group)


        # Username is required.
        if not username:

            messages.error(
                request,
                "Username is required."
            )

            return redirect(
                "accounts:staff_edit",
                pk=pk
            )


        # Prevent duplicate usernames.
        if User.objects.filter(
            username=username
        ).exclude(pk=pk).exists():

            messages.error(
                request,
                "Another user already has this username."
            )

            return redirect(
                "accounts:staff_edit",
                pk=pk
            )


        # Update basic information.
        staff_member.username = username
        staff_member.first_name = first_name
        staff_member.last_name = last_name
        staff_member.email = email


        # Prevent anyone from deactivating their own account.
        if staff_member.pk == request.user.pk:

            staff_member.is_active = True

        else:

            staff_member.is_active = is_active


        staff_member.save()


        messages.success(
            request,
            f"Staff account for {staff_member.username} was updated successfully."
        )

        return redirect("accounts:staff_list")

class StaffToggleStatusView(View):

    def post(self, request, pk, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        try:
            staff_member = User.objects.get(
                pk=pk,
                is_staff=True,
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Staff member not found."
            )

            return redirect("accounts:staff_list")


        # Normal staff members cannot modify superuser accounts.
        if (
            staff_member.is_superuser
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "You are not permitted to modify an administrator account."
            )

            return redirect("accounts:staff_list")


        # Prevent users from deactivating themselves.
        if staff_member.pk == request.user.pk:

            messages.error(
                request,
                "You cannot deactivate your own account."
            )

            return redirect("accounts:staff_list")


        # Toggle account status.
        staff_member.is_active = not staff_member.is_active
        staff_member.save(update_fields=["is_active"])


        if staff_member.is_active:

            messages.success(
                request,
                f"{staff_member.username} has been activated successfully."
            )

        else:

            messages.success(
                request,
                f"{staff_member.username} has been deactivated successfully."
            )


        return redirect("accounts:staff_list")

class StaffPasswordResetView(View):

    def get(self, request, pk, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        try:
            staff_member = User.objects.get(
                pk=pk,
                is_staff=True,
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Staff member not found."
            )

            return redirect("accounts:staff_list")


        # Normal staff cannot manage superuser passwords.
        if (
            staff_member.is_superuser
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "You are not permitted to reset an administrator's password."
            )

            return redirect("accounts:staff_list")


        # Prevent changing your own password through staff management.
        if staff_member.pk == request.user.pk:
            messages.error(
                request,
                "Use your account security settings to change your own password."
            )

            return redirect("accounts:staff_list")


        return render(
            request,
            "accounts/staff_password_reset.html",
            {
                "staff_member": staff_member,
            },
        )


    def post(self, request, pk, *args, **kwargs):

        if (
            not request.user.is_authenticated
            or not request.user.is_superuser
            or not request.user.is_active
        ):
            return redirect("accounts:login")

        try:
            staff_member = User.objects.get(
                pk=pk,
                is_staff=True,
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Staff member not found."
            )

            return redirect("accounts:staff_list")


        # Normal staff cannot manage superuser passwords.
        if (
            staff_member.is_superuser
            and not request.user.is_superuser
        ):
            messages.error(
                request,
                "You are not permitted to reset an administrator's password."
            )

            return redirect("accounts:staff_list")


        # Prevent changing your own password here.
        if staff_member.pk == request.user.pk:

            messages.error(
                request,
                "Use your account security settings to change your own password."
            )

            return redirect("accounts:staff_list")


        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        if not password:

            messages.error(
                request,
                "Password is required."
            )

            return redirect(
                "accounts:staff_password_reset",
                pk=pk
            )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect(
                "accounts:staff_password_reset",
                pk=pk
            )


        if len(password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return redirect(
                "accounts:staff_password_reset",
                pk=pk
            )


        staff_member.set_password(password)
        staff_member.save(update_fields=["password"])


        messages.success(
            request,
            f"Password for {staff_member.username} was reset successfully."
        )

        return redirect("accounts:staff_list")

class StaffLoginView(LoginView):

    template_name = "accounts/login.html"

    redirect_authenticated_user = True

    def get_success_url(self):

        return "/dashboard/"

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Invalid username or password."
        )

        return super().form_invalid(form)


class StaffLogoutView(View):

    def post(self, request, *args, **kwargs):

        logout(request)

        messages.success(
            request,
            "You have been signed out successfully."
        )

        return redirect("accounts:login")

