from django.test import TestCase
from catalog.models import Author

# Create your tests here.

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(first_name='Big',last_name='Bob')
    
    def test_first_name_max_length(self):
        author =Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name} {author.first_name}'
        self.assertEqual(str(author), expected_object_name)
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/authors/1')
    def test_verbose_names(self):
        fieldsVerbose =[
            ('last_name','last name'),
            ('first_name','first name'),
            ('date_of_birth','Birth'),
            ('date_of_death','Died'),
        ]
        author = Author.objects.get(id=1)
        for field_name,verbose_name in fieldsVerbose:
            field_label = author._meta.get_field(field_name).verbose_name
            self.assertEqual(field_label,verbose_name)

