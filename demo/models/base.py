from acmin.models import AcminModel


class BaseModel(AcminModel):
    class Meta:
        abstract = True
