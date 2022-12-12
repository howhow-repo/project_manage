import django.utils.timezone as timezone
from django.contrib.auth.models import Group
from customer.models import CustomerType, Customer, CustomerStatus
from project.models import ProjectStatus, ProjectType, Project
from material.models import Material, MaterialType
from employee.models import Department, User


def add_default_data():
    try:
        Group.objects.get_or_create(name='manager')
        Group.objects.get_or_create(name='normal')

        CustomerType.objects.get_or_create(name='一般住家')
        CustomerType.objects.get_or_create(name='公司行號')
        CustomerType.objects.get_or_create(name='企業合作')

        CustomerStatus.objects.get_or_create(name='待回覆')
        CustomerStatus.objects.get_or_create(name='待追蹤')
        CustomerStatus.objects.get_or_create(name='專案進行中')
        CustomerStatus.objects.get_or_create(name='未收款')
        CustomerStatus.objects.get_or_create(name='已收款')
        CustomerStatus.objects.get_or_create(name='無需求')

        ProjectStatus.objects.get_or_create(name='來電詢問')
        ProjectStatus.objects.get_or_create(name='待報價')
        ProjectStatus.objects.get_or_create(name='報價完成')
        ProjectStatus.objects.get_or_create(name='待出工')
        ProjectStatus.objects.get_or_create(name='待收款')
        ProjectStatus.objects.get_or_create(name='收款結束')

        ProjectType.objects.get_or_create(name='其他')
        ProjectType.objects.get_or_create(name='拉線')
        ProjectType.objects.get_or_create(name='攝影機')
        ProjectType.objects.get_or_create(name='網路')
        ProjectType.objects.get_or_create(name='對講機')
        ProjectType.objects.get_or_create(name='維修')

        Department.objects.get_or_create(name='一般')
        Department.objects.get_or_create(name='管理')
        MaterialType.objects.get_or_create(name='人力')

    except Exception:
        print("ERROR add_default_data")


def add_test_data():
    # test customer data
    try:
        customer_type = CustomerType.objects.get(name='一般住家')
        creater = User.objects.get(username='howardhsu')
        cusA = Customer.objects.get_or_create(
            name='測試客戶A', type=customer_type, creator=creater, editor=creater,
            address='台北市凱達格蘭大道1號', tel='012345678', cel='0912345678')
        Project.objects.get_or_create(
            title="裝網路", customer=cusA[0], status=ProjectStatus.objects.get(name='待出工'),
            creator=creater, editor=creater,
        )
        Project.objects.get_or_create(
            title="維修", customer=cusA[0], status=ProjectStatus.objects.get(name='報價完成'),
            creator=creater, editor=creater,
        )

        cusB = Customer.objects.get_or_create(
            name='測試客戶B', type=customer_type, creator=creater, editor=creater,
            address='台中市凱達格蘭大道1號', tel='022345678', cel='0987654321')
        Project.objects.get_or_create(
            title="拉線", customer=cusB[0], status=ProjectStatus.objects.get(name='來電詢問'),
            creator=creater, editor=creater,
        )

        cusC = Customer.objects.get_or_create(
            name='測試客戶C', type=customer_type, creator=creater, editor=creater,
            address='台南市凱達格蘭大道1號', tel='032345678', cel='0965748391')
        Project.objects.get_or_create(
            title="裝對講機", customer=cusC[0], status=ProjectStatus.objects.get(name='收款結束'),
            creator=creater, editor=creater,
        )
        Material.objects.get_or_create(
            name='人工', type=MaterialType.objects.get(name='人力'),
            unit='日', unit_price=1, note=None, creator=None
        )
    except Exception:
        print("ERROR add_test_data")


def initial_function():
    add_default_data()
    add_test_data()
