from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRestrictedMixin(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRestrictedMixin, self).dispatch(*args, **kwargs)