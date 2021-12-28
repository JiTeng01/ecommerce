from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy


class BaseURL:

    @classmethod
    def _get_url(cls, name, app=None, args=None, kwargs=None, params=None, is_redirect=False):
        if any(w in name for w in ['/', '#', '?']):
            return HttpResponseRedirect(name)

        if app:
            name = '%s:%s' % (app, name)

        if args is not None:
            redirect_url = reverse_lazy(name, args=args)
        elif kwargs is not None:
            redirect_url = reverse_lazy(name, kwargs=kwargs)
        else:
            redirect_url = reverse_lazy(name)

        if params is not None:
            redirect_url += ("?" + "&".join(params) if params is not None else '')

        return redirect_url if not is_redirect else HttpResponseRedirect(redirect_url)

    @classmethod
    def get_redirect_url(cls, name, is_absolute_url=False):
        redirect_url = name
        if not is_absolute_url:
            redirect_url = reverse_lazy(redirect_url)
        return HttpResponseRedirect(redirect_url)

    @classmethod
    def get_reverse_url(cls, name):
        return reverse_lazy(name)
