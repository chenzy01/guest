from django.test import TestCase
from .models import Event, Guest
from datetime import datetime
from django.contrib.auth.models import User


# Create your tests here.
# 继承 django.test.TestCase 类
class ModelTest(TestCase):
    # 模型测试
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address='shenzhen', start_time='2016-08-31 02:18:33')

        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101',
                             email='alen@mail.com', sign=False)

        def test_event_models(self):
            # 测试发布会表
            result = Event.objects.get(name='oneplus 3 event')
            self.assertEqual(result.address, "beijing")
            self.assertTrue(result.status)

        def test_guest_models(self):
            # 测试嘉宾表
            result = Guest.objects.get(phone='13711001101')
            self.assertEqual(result.realname, "alen")
            self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    # 测试index登录首页

    def test_index_page_renders_index_template(self):
        # 断言是否用给定的index.html模版响应
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    # 测试登录动作

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        # 测试添加用户
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        # 用户名密码为空
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        # 用户名密码错误
        test_data = {'username': 'abc', 'password': '12345'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        # 用户名密码为空
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    # 发布会管理

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2017-08-10 12:11:33')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        # 测试发布会：xiaomi5
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/event_manage/')
        self.assertEqual( self.response.status_code, 200)
        self.assertIn(b"xiaomi5", self.response.content)
        self.assertIn(b"beijing", self.response.content)

    def test_event_manage_search_success(self):
        # 测试发布会搜索
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/search_name/', {'name': 'xiaomi5'})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"xiaomi5", self.response.content)
        self.assertIn(b"beijing", self.response.content)


class GuestManageTest(TestCase):
    # 嘉宾管理

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2017-08-10 12:11:33')
        Guest.objects.create(realname='alen', phone='18611001100', email='alen@mail.com',
                             sign=0, event_id=1)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_manage_success(self):
        # 测试嘉宾信息：alen
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/guest_manage/')
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"alen", self.response.content)
        self.assertIn(b"18611001100", self.response.content)

    def test_guest_manage_search_success(self):
        # 测试嘉宾搜索

        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/search_phone/', {"phone": "18611001100"})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"alen", self.response.content)
        self.assertIn(b"18611001100", self.response.content)


class SignIndexActionTest(TestCase):
    # 发布会签到
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing',
                             status=1, start_time='2017-08-10 12:11:33')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen',
                             status=1, start_time='2017-06-10 13:11:33')
        Guest.objects.create(realname='alen', phone='18611001100', email='alen@mail.com',
                             sign=0, event_id=1)
        Guest.objects.create(realname='una', phone='18611001101', email='una@mail.com',
                             sign=1, event_id=2)
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_sign_index_action_phone_null(self):
        # 手机号为空
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"phone error", self.response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        # 手机号或发布会 id 错误
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/sign_index_action/2/', {"phone": "18611001100"})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"event id or phone error", self.response.content)

    def test_sign_index_action_user_sign_has(self):
        # 用户已签到
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/sign_index_action/2/', {"phone": "18611001101"})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"user has sign in", self.response.content)

    def test_sign_index_action_user_sign_success(self):
        # 签到成功
        self.response = self.client.post('/login_action/', data=self.login_user)
        self.response = self.client.post('/sign_index_action/1/', {"phone": "18611001100"})
        self.assertEqual(self.response.status_code, 200)
        self.assertIn(b"sign in success!", self.response.content)
