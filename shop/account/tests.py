from django.test import TestCase
from account.forms import LoginForm, SignupForm
from account.models import Account, State, City


class FormTest(TestCase):
    def test_login_form_validation(self):
        login_data = {'username': 'admin', 'password': 'admin'}
        form = LoginForm(data=login_data)
        self.assertTrue(form.is_valid())

        login_data = {'username': '', 'password': 'admin'}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), False)

        login_data = {'username': 'admin', 'password': ''}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), False)

        login_data = {'username': 123, 'password': 123}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), True)

        login_data = {'username': [1,'admin',3], 'password': {'name':'admin'}}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), True)

    def test_signup_form_validation(self):
        state = State.objects.create(name='خراسان رضوی')
        city = City.objects.create(name='مشهد', state=state)

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertTrue(form.is_valid())

        signup_data = {'first_name': 1, 'last_name': 1, 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 1,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertTrue(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '072050049',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '0911234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '012346789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '2', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '2', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@12'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': '123abc', 'password2': '123abc'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())


class ViewTest(TestCase):
    def setUp(self):
        state = State.objects.create(name='خراسان رضوی')
        city = City.objects.create(name='مشهد', state=state)

    def login(self, login_data={'username': 'username', 'password': 'password@123'}):
        response = self.client.get('/account/logout/')

        response = self.client.post('/account/login/', login_data)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'logged in', response.content)

    def create_user_and_login(self, username='username'):
        response = self.client.get('/account/logout/')

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': username,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        login_data = {'username': username, 'password': 'password@123'}
        account_count = Account.objects.count()
        response = self.client.post('/account/signup/', signup_data)
        self.assertTrue(account_count + 1, Account.objects.count())

        self.login(login_data)

        return login_data

    def test_signup_view(self, username='username'):
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

        response = self.client.get('/account/signup')
        self.assertEqual(response.status_code, 301)

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': username,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        account_count = Account.objects.count()
        response = self.client.post('/account/signup/', signup_data)
        self.assertTrue(account_count+1, Account.objects.count())

        account = Account.objects.get(username='username')
        self.client.force_login(account)
        response = self.client.get('/account/signup/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED

        response = self.client.post('/account/signup/', signup_data)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED

        self.client.logout()

    def test_login_view(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 301)

        login_data = self.create_user_and_login()

        response = self.client.get('/account/login/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'User is already logged in', response.content)

        response = self.client.post('/account/login/', login_data)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'User is already logged in', response.content)

    def test_logout_view(self):
        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You have already logged out.', response.content)

        login_data = self.create_user_and_login()

        response = self.client.post('/account/login/', login_data)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'User is already logged in', response.content)
        response = self.client.get('/account/logout/')
        self.assertEqual(b'You have successfully logged out.', response.content)

        response = self.client.get('/account/logout/')
        self.assertEqual(b'You have already logged out.', response.content)

    def test_edit_view(self):
        response = self.client.get('/account/1/edit/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()

        response = self.client.get('/account/1/edit/')
        self.assertTemplateUsed(response, 'edit.html')
        self.assertEqual(response.context['form'].instance.username, 'username')

        response = self.client.get('/account/2/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login('username2')

        response = self.client.get('/account/1/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        response = self.client.get('/account/2/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertTemplateUsed(response, 'edit.html')
        self.assertEqual(response.context['form'].instance.username, 'username2')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/1/edit/')
        self.assertTemplateUsed(response, 'edit.html')

        response = self.client.get('/account/3/edit/')
        self.assertTemplateUsed(response, 'edit.html')

    def test_detail_view(self):
        response = self.client.get('/account/1/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/account/1/')
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual('username', response.context['account'].username)

        self.create_user_and_login('username2')

        response = self.client.get('/account/2/')
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual('username2', response.context['account'].username)

        response = self.client.get('/account/1/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/3/')
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual('admin', response.context['account'].username)

        response = self.client.get('/account/1/')
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual('username', response.context['account'].username)

        response = self.client.get('/account/4/') # TODO: CHECK REDIRECTION WHEN ERROR PAGE CREATED
        self.assertTemplateNotUsed(response, 'detail.html')

    def test_list_view(self):
        response = self.client.get('/account/all/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/account/all/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/all/')
        self.assertTemplateUsed('list.html')
        self.assertEqual(Account.objects.get(pk=1), response.context['accounts'][0])
        self.assertEqual(Account.objects.get(pk=2), response.context['accounts'][1])

    def test_deactivate(self):
        response = self.client.get('/account/1/deactivate/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/account/1/deactivate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login('username2')
        response = self.client.get('/account/1/deactivate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/2/deactivate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'Account deactivated!', response.content)

        response = self.client.get('/account/2/deactivate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'Account is already deactivated!', response.content)

    def test_activate(self):
        response = self.client.get('/account/1/activate/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/account/1/activate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login('username2')
        response = self.client.get('/account/1/activate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/2/activate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'Account is already activated!', response.content)

        self.client.get('/account/2/deactivate/')
        response = self.client.get('/account/2/activate/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'Account activated!', response.content)

