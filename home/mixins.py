from django.contrib import messages
from django.shortcuts import redirect




class LoginFirstMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'you should login first', 'danger')
        return redirect('accounts:login')
