from django.test import TestCase , Client
import datetime
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Task
# Create your tests here.

class TaskModelTests(TestCase):
    def test_is_created_with_duplicate_task(self):
        user = create_test_user ( "test_user1" )
        task1 = test_create_task( title="title1" , user=user.id )
        task2 = Task (title="title1" , user_id=user.id )
        self.assertIs( task2.title_is_duplicated(task2.title,task2.user) ,True )

    def test_is_created_with_no_duplicate_task(self):
        user = create_test_user ( "test_user1" )
        task1 = test_create_task( title="title1" , user=user.id )
        task2 = Task (title="title2" , user_id=user.id )
        self.assertIs( task2.title_is_duplicated(task2.title,task2.user) ,False )

    def test_is_created_with_duplicate_task_dif_users(self):
        user1 = create_test_user ( "test_user1" )
        user2 = create_test_user ( "test_user2" )
        task1 = test_create_task( title="title1" , user=user1.id )
        task2 = Task (title="title1" , user_id=user2.id )
        self.assertIs( task2.title_is_duplicated(task2.title,task2.user) ,False )

class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_no_tasks (self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks are available.")
        self.assertQuerySetEqual(response.context["tasks"], [])

    def test_pending_tasks (self):
        self.task = Task.objects.create(title='Test Task', description='Description', user=self.user)
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertQuerySetEqual(response.context["tasks"], [self.task])

    def test_completed_tasks (self):
        self.task = Task.objects.create(title='Test Task2', description='Description', user=self.user, datacompleted = timezone.now())
        response = self.client.get(reverse("tasks_completed"))
        print(response.headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task2")
        self.assertQuerySetEqual(response.context["tasks"], [self.task])

    def test_create_task_view(self):
        response = self.client.post(reverse('create_task'), {'title': 'New Task', 'description': 'Description'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

def test_create_task (title: str,description : str = "",important : bool = False ,user : int = 3,days : int=None):

    if days == None or days<=0 :
        datacompleted = None if days == None else timezone.now() + datetime.timedelta(days=days)
        return Task.objects.create(title=title,description=description,important=important,user_id=user,                datacompleted= datacompleted)
    else:
        print("Favor ingresar un valor correcto en el campo 'days'")

def create_test_user (user : str ):
    try:
        test_user= User.objects.create(username=user , password= 'testpassword')
        return test_user
    except:
        print("Username already exists!")
    




