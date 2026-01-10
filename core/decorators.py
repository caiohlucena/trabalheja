from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def apenas_empresa(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not hasattr(request.user, 'profile'):
            messages.error(request, 'Perfil de usuário inválido.')
            return redirect('/dashboard/')

        if request.user.profile.tipo != 'empresa':
            messages.error(request, 'Acesso permitido apenas para empresas.')
            return redirect('/dashboard/')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
