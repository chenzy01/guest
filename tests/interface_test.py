import requests
import unittest


class GetEventListTest(unittest.TestCase):
    # 查询发布会接口测试
    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        #发布会 id 为空
        r = requests.get(url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        r = requests.get(url, params={'eid': '901'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_event_success(self):
        r = requests.get(url, params={'eid': '1'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '小米5发布会')
        self.assertEqual(result['data']['address'], '北京国家议会中心')
        self.assertEqual(result['data']['start_time'], '2016-12-08T14:29:21')


if __name__ == '__main__':
    unittest.main()












