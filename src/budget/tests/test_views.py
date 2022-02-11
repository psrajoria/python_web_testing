import json
from urllib import response
from django.test import TestCase, Client, tag
from django.urls import reverse
from budget.models import Project, Category, Expense


# @tag('Views')
class TestViews(TestCase):
    @tag('fast')
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.test_project = Project.objects.create(
            name='project1',
            budget=100000,
        )

    # @tag('slow')
    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')

    # @tag('fast')
    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    # @tag('fast')
    def test_project_detail_POST_category(self):
        Category.objects.create(
            project=self.test_project,
            name='design'
        )

        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'design'
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.test_project.expenses.first().title, 'expense1')

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.test_project.expenses.count(), 0)

    def test_project_detail_DELETE_expense(self):
        test_category = Category.objects.create(
            project=self.test_project,
            name='design'
        )
        Expense.objects.create(
            project=self.test_project,
            title='expense1',
            amount=1000,
            category=test_category
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1
        }))
        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.test_project.expenses.count(), 0)

    def test_project_detail_DELETE_no_ID(self):
        test_category = Category.objects.create(
            project=self.test_project,
            name='design'
        )
        Expense.objects.create(
            project=self.test_project,
            title='expense1',
            amount=1000,
            category=test_category
        )

        response = self.client.delete(self.detail_url)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.test_project.expenses.count(), 1)

    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'project2',
            'budget': 1000,
            'categoriesString': 'design,development'
        })

        test_project2 = Project.objects.get(id=2)
        self.assertEquals(test_project2.name, 'project2')
        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, test_project2)
        self.assertEquals(first_category.name, 'design')
        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, test_project2)
        self.assertEquals(second_category.name, 'development')
