import unittest
import requests
import hashlib
from time import time


class AddEventTest(unittest.TestCase):
    # 添加发布会（带用户验证）

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        # app_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间
        now_time = time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_request_error(self):
        # 请求方法错误
        r = requests.get(self.base_url)
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], 'request error')

    def test_add_event_sign_null(self):
        # 签名参数为空
        payload = {'id': '', 'name': '', 'limit': '', 'address': '', 'start_time': '', 'create_time': '',
                   'time': '', 'sign': ''}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user sign null')

    def test_add_event_time_out(self):
        # 请求超时
        now_time = str(int(self.client_time) - 61)
        payload = {'id': 1, 'name': '', 'limit': '', 'address': '', 'start_time': '', 'create_time': '',
                   'time': now_time, 'sign': 'abd'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10013)
        self.assertEqual(result['message'], 'user sign timeout')

    def test_add_event_sign_error(self):
        # 签名错误
        payload = {'id': 1, 'name': '', 'limit': '', 'address': '', 'start_time': '', 'create_time': '',
                   'time': self.client_time, 'sign': 'abd'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10014)
        self.assertEqual(result['message'], 'user sign error')

    def test_add_event_eid_exist(self):
        # id 已存在
        payload = {'id': 1, 'name': '一加4发布会', 'limit': '2000', 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'event id already exist')

    def test_add_event_name_exist(self):
        # name 已存在
        payload = {'id': 11, 'name': '一加3发布会', 'limit': '2000', 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10023)
        self.assertEqual(result['message'], 'event name already exist')

    def test_add_event_data_type_error(self):
        # 日期格式错误
        payload = {'id': 11, 'name': '一加5发布会', 'limit': '2000', 'address': '深圳宝体',
                   'start_time': '2017', 'create_time': '2017',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10024)
        self.assertEqual(result['message'], 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.')

    def test_add_event_sign_success(self):
        # 签名成功
        payload = {'id': 21, 'name': '一加5手机发布会', 'limit': '2000', 'address': '深圳宝体',
                   'start_time': '2017-10-02 12:00:00', 'create_time': '2017-10-02 12:00:00',
                   'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')


if __name__ == '__main__':
    unittest.main()











