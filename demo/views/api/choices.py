from django.contrib.auth.decorators import login_required

from acmin.models import ContentType, Filter, Field
from acmin.router import route
from acmin.utils import param, json_response, int_param


# http://127.0.0.1:8000/api/demo/choices/?attribute=city.province&type=City&parent=2
@route("api/demo/choices/")
@login_required
def get(request):
    attribute = param(request, "attribute")
    contenttype: ContentType = ContentType.get("demo", param(request, "type"))
    if contenttype and attribute:
        parent = int_param(request, "parent")
        model = contenttype.get_model()

        queryset = Filter.filter(model.objects, request, model)
        if parent > 0 and "." in attribute:
            parent_attribute = attribute.split(".")[-1]
            if Field.get_default_field(model, parent_attribute):
                queryset = queryset.filter(**{f"{parent_attribute}_id": parent})
        return json_response(dict(
            status=0,
            choices=[dict(value=obj.id, title=str(obj)) for obj in queryset.all()]
        ))

    return json_response(dict(status=1))
