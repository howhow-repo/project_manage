from django.db import models
from django.db.models import Manager


def get_model_or_none(model, query_dict):
    try:
        return model.objects.get(**query_dict)
    except models.ObjectDoesNotExist:
        return None


class MyManager(Manager):
    def get_models_or_none(self, *args, **kwargs):
        try:
            return self.filter(*args, **kwargs).first()
        except models.ObjectDoesNotExist:
            return None
