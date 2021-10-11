from django.db.models import Q
from django.apps import apps
from rest_framework.request import Request


# Avoids 401s for unprotected endpoints -- but 403s (permissions classes) unaffected
class MethodAuthenticationMixin(object):
    # method_authentication_classes = {
    #     "OPTIONS": None,
    #     "GET": None,
    #     "POST": None,
    #     "PUT": None,
    #     "PATCH": None,
    #     "HEAD": None,
    #     "DELETE": None,
    #     "TRACE": None,
    #     "CONNECT": None,
    # }

    def initialize_request(self, request, *args, **kwargs):
        parser_context = self.get_parser_context(request)

        method = request.method.upper()
        if hasattr(self, "method_authentication_classes") and isinstance(
            self.method_authentication_classes.get(method), (list, tuple)
        ):
            authenticators = [
                auth() for auth in self.method_authentication_classes[method]
            ]
        else:
            authenticators = self.get_authenticators()

        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=authenticators,
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context,
        )


class OrFilterSetMixin(object):
    def _listify(self, value):
        if not isinstance(value, (list, set, tuple)):
            value = [value]
        return [v for v in value if v != ""]

    def or_lookup(self, queryset, name, value, key=None, lookup_expr="exact"):
        name = self._listify(name)
        q = Q()
        for n in name:
            fieldname = "{}__{}".format(n, lookup_expr)
            for v in set(value):
                if v is not None and v != "":
                    predicate = {fieldname: v}
                    if key is not None:
                        predicate = {fieldname: [{key: v}]}
                    q |= Q(**predicate)

        return queryset.filter(q).distinct()

    def int_lookup(self, queryset, name, value):
        value = [int(v.strip(",. ")) for v in self._listify(value)]
        return self.or_lookup(queryset, name, value)

    def id_lookup(self, queryset, name, value):
        Model = apps.get_model("api", name)
        name = f"{name}__{Model._meta.pk.name}"
        return self.int_lookup(queryset, name, value)

    def char_lookup(self, queryset, name, value):
        value = [str(v).strip() for v in self._listify(value)]
        return self.or_lookup(queryset, name, value, lookup_expr="icontains")
