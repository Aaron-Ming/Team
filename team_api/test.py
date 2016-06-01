import unittest, re, json
import pub
from api import app


class TeamApiTest(unittest.TestCase):

    def setUp(self):
        self.mysql  = pub.mysql
        self.logger = pub.logger
        self.app    = app.test_client()
        self.base_url = 'http://api.team.saintic.com'
        self.username = "test_case10"
        self.password = "123456"
        self.email    = None

    def tearDown(self):
        self.logger.debug("test case")

    def test_mysql(self):
        self.assertTrue(self.mysql.get('show tables;'))

    def test_pub(self):
        token,requestId = pub.gen_token(), pub.gen_requestId()
        self.assertEqual(len(token), 32)
        self.assertEqual(len(requestId), 36)
        self.assertTrue(re.match(r'([0-9a-z]{8})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{8})', requestId))

    def test_web_index(self):
        Index = self.app.get('%s/'%self.base_url)
        data = json.loads(Index.data)
        assert 'Team.Api' in data

    def test_web_user(self):
        User = self.app.get('%s/user'%self.base_url)
        data = json.loads(User.data)
        self.assertEqual(data.get('code'), 0)

    def login(self, username, password):
        url = self.base_url + '/user?action=log'
        return self.app.post('/user?action=log',
            data=dict(username=username, password=password),
            follow_redirects=True,
        )
    def test_login(self, username=None, password=None):
        Login = self.login(self.username, self.password)
        data  = json.loads(Login.data)
        print data
        self.assertEqual(data.get('code'), 0)
        assert 'authentication success' in data.get('msg')
        self.assertEqual(data.get('data').get('username'), self.username)

    def registry(self, username, password, email=None):
        url = self.base_url + '/user?action=reg'
        return self.app.post('/user?action=reg',
            data=dict(username=username, password=password, email=email),
            follow_redirects=True,
        )
    def test_registry(self):
        print '\n'
        Registry = self.registry(self.username, self.password, self.email)
        data = json.loads(Registry.data)
        print data
        if data.get('code') == 0:
            self.test_login(username=self.username, password=self.password)
        else:
            print 'registry fail, enter assert'
            assert 'already exists' in data.get('msg')
            self.assertEqual(data.get('data').get('username'), self.username)
            self.assertEqual(data.get('data').get('email'), self.email)

    def token(self, username, password):
        url = self.base_url + '/token'
        return self.app.post(url,
            data=dict(username=username, password=password),
            follow_redirects=True,
            #headers=[('Content-Type', 'application/json')],
        )
    def test_token(self):
        Token = self.token(username=self.username, password=self.password)
        data = json.loads(Token.data)
        print data
        if data.get('code') ==  0:
            assert 'authentication success' in data.get('msg')
            assert 'created' in data.get('msg')
        else:
            assert 'Token already exists' in data.get('msg')
            self.assertEqual(len(data.get('token')), 32)

if __name__ == '__main__':
    unittest.main()
