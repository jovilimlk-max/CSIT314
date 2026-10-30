import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from werkzeug.security import generate_password_hash

from app import RenovoApp
from Entities.userAccount import UserAccount
from Entities.userProfile import UserProfile


class InteriorDesignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        def account_init(account):
            account.db_path = root / 'accounts.db'
        def profile_init(profile):
            profile.db_path = root / 'profiles.db'
        with patch.object(UserAccount, '__init__', account_init), patch.object(UserProfile, '__init__', profile_init):
            self.system = RenovoApp()
        self.app = self.system.app
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
        for name in ('one','two'):
            self.system.user_account.create_user_account(name, name + '@example.com', generate_password_hash('secret'), 'designer')
        self.login()

    def tearDown(self):
        self.temp.cleanup()

    def login(self, email='one@example.com'):
        response = self.client.post('/login', json=dict(email=email, password='secret', role='designer'))
        self.assertEqual(response.status_code, 200)
        self.client.get('/interior-designer/company')

    def post(self, path, data):
        with self.client.session_transaction() as session:
            token = session['csrf_token']
        return self.client.post('/interior-designer' + path, data={**data, 'csrf_token':token}, follow_redirects=True)

    def company(self):
        return self.post('/company/create', dict(name='Studio One',address='Singapore',hours='9 to 6',email='studio@example.com',phone='61234567',established='2015-03-15',description='Interior design studio'))

    def project(self, **changes):
        data = dict(name='Kitchen makeover',description='A new kitchen',progress='Ongoing',start_date='2026-10-20')
        return self.post('/projects/create', {**data, **changes})

    def test_company_create_update_filter_and_status(self):
        self.assertIn(b'no company information yet', self.client.get('/interior-designer/company').data)
        self.assertIn(b'This field is required', self.post('/company/create', {}).data)
        self.assertIn(b'Studio One', self.company().data)
        self.assertIn(b'No designers match', self.client.get('/interior-designer/company?q=missing').data)
        self.assertIn(b'reactivated successfully', self.post('/company/status',dict(status='active')).data)
        self.assertIn(b'suspended successfully', self.post('/company/status',dict(status='suspended')).data)
        self.assertIn(b'value="Studio One"', self.client.get('/interior-designer/company/edit').data)
        self.assertIn(b'Company information updated', self.post('/company/edit', dict(
            name='Updated Studio',address='Singapore',hours='10 to 7',email='studio@example.com',
            phone='61234567',established='2015-03-15',description='Updated description')).data)

    def test_projects_validation_search_edit_and_status(self):
        self.company()
        self.assertIn(b'End date', self.project(progress='Completed').data)
        self.assertEqual(len(self.system.interior_design.projects(1)), 0)
        self.assertIn(b'on or after', self.project(progress='Completed',end_date='2026-10-01').data)
        self.project()
        self.project(name='Completed condo',progress='Completed',end_date='2026-10-25')
        response = self.client.get('/interior-designer/projects?q=condo')
        self.assertIn(b'Completed condo', response.data)
        self.assertNotIn(b'Kitchen makeover', response.data)
        self.assertIn(b'End date', self.client.get('/interior-designer/projects/2').data)
        self.assertIn(b'Project updated', self.post('/projects/1/edit',dict(name='Kitchen revised',description='Changed',progress='Completed',start_date='2026-10-20',end_date='2026-10-29')).data)
        self.assertIn(b'suspended successfully', self.post('/projects/1/status',dict(status='suspended')).data)
        self.assertIn(b'Kitchen revised', self.client.get('/interior-designer/projects?status=suspended').data)
        self.assertIn(b'value="Kitchen revised"', self.client.get('/interior-designer/projects/1/edit').data)

    def test_ownership_csrf_and_logout(self):
        self.company()
        self.project()
        self.assertEqual(self.client.post('/interior-designer/company/status',data={'status':'suspended'}).status_code, 400)
        self.login('two@example.com')
        self.company()
        self.assertEqual(self.client.get('/interior-designer/projects/1').status_code, 404)
        self.assertEqual(self.post('/projects/1/status',dict(status='suspended')).status_code, 404)
        self.assertIn(b'logged out successfully', self.post('/logout',{}).data)
        self.assertIn('login_required', self.client.get('/interior-designer/company').location)

    def test_role_checks_and_suspended_account(self):
        response = self.client.post('/login', json=dict(email='one@example.com',password='secret',role='customer'))
        self.assertEqual(response.status_code, 401)
        self.assertIn('login_required', self.client.get('/interior-designer/projects').location)
        self.login()
        with self.system.interior_design.connect() as db:
            db.execute("UPDATE user_accounts SET status='suspended' WHERE id=1")
        self.assertIn('login_required', self.client.get('/interior-designer/company').location)

    def test_pagination_and_sort(self):
        self.company()
        for i in range(7):
            self.project(name=f'Project {i}')
        response = self.client.get('/interior-designer/projects?sort=asc&page=2')
        self.assertIn(b'Page 2 of 2', response.data)
        self.assertIn(b'Project 5', response.data)
        self.assertNotIn(b'Project 0', response.data)


if __name__ == '__main__':
    unittest.main()
