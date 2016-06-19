from django.contrib.auth.models import User
from django.test import TestCase

from .models import Memory, Prompt


class MemoryMethodTests(TestCase):
    USER = User.objects.first()

    def test_str_with_title(self):
        memory = Memory(title='Test title', text='Sample', creator=self.USER)
        self.assertNotEqual(str(memory).find(memory.title), -1)
        self.assertNotEqual(str(memory).find(self.USER.username), -1)

    def test_str_with_prompt(self):
        prompt = Prompt(text='Test prompt')
        memory = Memory(prompt=prompt, text='Sample', creator=self.USER)
        self.assertNotEqual(str(memory).find(prompt.text), -1)
        self.assertNotEqual(str(memory).find(self.USER.username), -1)
