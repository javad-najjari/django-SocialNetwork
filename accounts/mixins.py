from django.shortcuts import get_object_or_404, redirect
from .models import User
from django.contrib import messages




class EditAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if request.user == user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You can not edit other people's profiles", 'warning')
            return redirect('home:home')

