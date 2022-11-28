from django.http import Http404, HttpResponse

class PartnerPermissionMixin:
    def has_permissions(self):
        return self.get_object().user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

class AnswerCreateUpdateDeletePermissionMixin:
    def has_permissions(self):
        return self.get_object().id_student.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

class CaseCreateUpdateDeletePermissionMixin:
    def has_permissions(self):
        return self.get_object().user_id.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

class WinnerUpdateMixin:
    def has_permissions(self):
        return self.get_object().id_case.user_id.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class AnswerAddPermissionMixin:
    def has_permissions(self):
        return self.get_object().user_id.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

