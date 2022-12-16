from django.db import models


def get_model_or_none(model, query_dict):
    try:
        return model.objects.get(**query_dict)
    except models.ObjectDoesNotExist:
        return None
