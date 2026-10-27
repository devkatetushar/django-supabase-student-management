from django.test import TestCase
from django.urls import reverse
from .models import Student


class StudentCrudTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Test Student",
            roll_number="TEST001",
            email="test@example.com",
            age=20,
            course="Chemical Engineering",
            address="Test address",
        )

    def test_list_page_shows_student(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Student")

    def test_create_student(self):
        response = self.client.post(reverse("student_create"), {
            "name": "New Student",
            "roll_number": "TEST002",
            "email": "new@example.com",
            "age": "21",
            "course": "Chemical Engineering",
            "address": "",
        })
        self.assertRedirects(response, reverse("student_list"))
        self.assertTrue(Student.objects.filter(roll_number="TEST002").exists())

    def test_delete_requires_post(self):
        response = self.client.post(reverse("student_delete", args=[self.student.pk]))
        self.assertRedirects(response, reverse("student_list"))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
