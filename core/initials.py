from datetime import datetime
from django.contrib.auth.models import Group
from customer.models import CustomerType, CaseStatus, Customer
from materials.models import Material, MaterialType
from employee.models import Department, User


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
        man_power = MaterialType.objects.get_or_create(name='人力')
        Material.objects.get_or_create(
            name='人工', type=man_power[0],
            unit='日', unit_price=1, note=None, creator=None, update_time=datetime.now()
        )
    except Exception:
        pass


def add_test_data():
    # test customer data
    customer_type = CustomerType.objects.get(name='normal')
    creater = User.objects.get(username='howardhsu')
    Customer.objects.get_or_create(name='測試客戶A', type=customer_type, creator=creater,
                                   address='台北市凱達格蘭大道1號', tel='012345678', cel='0912345678')
    Customer.objects.get_or_create(name='測試客戶B', type=customer_type, creator=creater,
                                   address='台中市凱達格蘭大道1號', tel='022345678', cel='0987654321')
    Customer.objects.get_or_create(name='測試客戶C', type=customer_type, creator=creater,
                                   address='台南市凱達格蘭大道1號', tel='032345678', cel='0965748391')


def initial_function():
    add_default_data()
    add_test_data()

