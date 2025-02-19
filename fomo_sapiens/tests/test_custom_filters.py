from django.test import TestCase
from django.template import Template, Context


class StartsWithFilterTest(TestCase):

    def test_startswith_filter(self):
        template_string = "{{ 'Hello, World!'|startswith:'Hello' }}"

        context = Context()
        rendered = Template(template_string).render(context)

        self.assertEqual(rendered.strip(), "True")

    def test_startswith_filter_false(self):
        template_string = "{{ 'Hello, World!'|startswith:'World' }}"

        context = Context()
        rendered = Template(template_string).render(context)

        self.assertEqual(rendered.strip(), "False")

    def test_startswith_empty_value(self):
        template_string = "{{ ''|startswith:'Hello' }}"

        context = Context()
        rendered = Template(template_string).render(context)

        self.assertEqual(rendered.strip(), "False")

    def test_startswith_empty_prefix(self):
        template_string = "{{ 'Hello, World!'|startswith:'' }}"

        context = Context()
        rendered = Template(template_string).render(context)

        self.assertEqual(rendered.strip(), "True")
