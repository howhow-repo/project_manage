from django.db import models


class TicketStatusChoices(models.TextChoices):
    NEW = 'NEW', '新增'
    FILL = 'FILL', '客戶編輯'
    MODIFY = 'MODIFY', '編輯中'
    DONE = 'DONE', '完成'
