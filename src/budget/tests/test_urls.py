from django.test import SimpleTestCase, tag
from django.urls import reverse, resolve
from budget.views import project_list, project_detail, ProjectCreateView


@tag('Urls')
class TestUrls(SimpleTestCase):

    def test_list_urls(self):
        url = reverse('list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, project_list)

    # @unittest.skip("Skipping")
    def test_add_urls_t(self):
        url = reverse('add')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView)

    def test_detail_urls(self):
        url = reverse('detail', args=['some-slug'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, project_detail)
