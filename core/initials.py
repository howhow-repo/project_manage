import django.utils.timezone as timezone
from django.contrib.auth.models import Group
from customer.models import CustomerType, Customer
from project.models import ProjectStatus, Project
from material.models import Material, MaterialType
from employee.models import Department, User


def add_default_data():
    try:
        Group.objects.get_or_create(name='manager')
        Group.objects.get_or_create(name='normal')
        CustomerType.objects.get_or_create(name='normal')
        ProjectStatus.objects.get_or_create(name='來電詢問')
        ProjectStatus.objects.get_or_create(name='待報價')
        ProjectStatus.objects.get_or_create(name='報價完成')
        ProjectStatus.objects.get_or_create(name='待出工')
        ProjectStatus.objects.get_or_create(name='待收款')
        ProjectStatus.objects.get_or_create(name='收款結束')
        Department.objects.get_or_create(name='一般')
        Department.objects.get_or_create(name='管理')
        man_power = MaterialType.objects.get_or_create(name='人力')
        Material.objects.get_or_create(
            name='人工', type=man_power[0],
            unit='日', unit_price=1, note=None, creator=None, update_time=timezone.now()
        )
    except Exception:
        pass


def add_test_data():
    # test customer data
    try:
        customer_type = CustomerType.objects.get(name='normal')
        creater = User.objects.get(username='howardhsu')
        cusA = Customer.objects.get_or_create(
            name='測試客戶A', type=customer_type, creator=creater,
            address='台北市凱達格蘭大道1號', tel='012345678', cel='0912345678')
        Project.objects.get_or_create(
            title="裝網路", customer=cusA[0], status=ProjectStatus.objects.get(name='待出工'),
            creator=creater
        )
        Project.objects.get_or_create(
            title="維修", customer=cusA[0], status=ProjectStatus.objects.get(name='報價完成'),
            creator=creater
        )

        cusB = Customer.objects.get_or_create(
            name='測試客戶B', type=customer_type, creator=creater,
            address='台中市凱達格蘭大道1號', tel='022345678', cel='0987654321')
        Project.objects.get_or_create(
            title="拉線", customer=cusB[0], status=ProjectStatus.objects.get(name='來電詢問'),
            creator=creater
        )

        cusC = Customer.objects.get_or_create(
            name='測試客戶C', type=customer_type, creator=creater,
            address='台南市凱達格蘭大道1號', tel='032345678', cel='0965748391')
        Project.objects.get_or_create(
            title="裝F", customer=cusC[0], status=ProjectStatus.objects.get(name='收款結束'),
            creator=creater
        )
    except Exception:
        pass


def initial_function():
    add_default_data()
    add_test_data()
