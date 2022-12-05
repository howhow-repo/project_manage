from django.contrib.auth.models import Group
from customer.models import CustomerType, CaseStatus
from materials.models import Material, MaterialType
from employee.models import Department


def add_default_data():
    try:
        Group.objects.get_or_create(name='manager')
        Group.objects.get_or_create(name='normal')
        CustomerType.objects.get_or_create(name='normal')
        CaseStatus.objects.get_or_create(name='來電詢問')
        CaseStatus.objects.get_or_create(name='待報價')
        CaseStatus.objects.get_or_create(name='報價完成')
        CaseStatus.objects.get_or_create(name='待出工')
        CaseStatus.objects.get_or_create(name='待收款')
        CaseStatus.objects.get_or_create(name='收款結束')
        Department.objects.get_or_create(name='一般')
        Department.objects.get_or_create(name='管理')

        Material.objects.get_or_create(
            name='人工', type=MaterialType.objects.get_or_create(name='人力'),
            unit='日', unit_price=1, note=None, creator=None
        )
    except Exception:
        pass


def initial_function():
    add_default_data()
