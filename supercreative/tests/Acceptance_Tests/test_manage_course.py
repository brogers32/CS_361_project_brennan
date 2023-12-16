from django.test import TestCase, Client
from supercreative.course import course
from supercreative.models import Course, UserCourseAssignment, Section
from supercreative.authentication import authentication
from supercreative.user import user
from supercreative.create_sections import section


class ManageCoursesAcceptanceTests(TestCase):
    client = None
    existing_course = None
    existing_section = None
    existing_user = None

    def setUp(self):
        self.client = Client()

        # Set up data for the whole TestCase
        course.create_course(1, 'Test course', 'Test Description', 'TC101')
        self.existing_course = Course.objects.get(course_id=1)
        self.existing_user = user.create_user(1, 'test@uwm.edu', 'P@ssword123', 'ADMINISTRATOR', 'Jayson',
                                              'Rock', '1234567890', '123 Sesame St')
        authentication.create_session(self.client.session, 'test@uwm.edu')

        # Set up an existing section for testing edit_section
        section.create_section(1, self.existing_course, 'Lecture', self.existing_user)
        self.existing_section = Section.objects.get(section_id=1)

    def test_get_manage_courses(self):
        response = self.client.get('/manage-courses/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-courses.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)

    def test_post_assign_user(self):
        response = self.client.post('/manage-courses/', {'action': 'assign_user', 'user_id': '1', 'course_id': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-courses.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)

    def test_post_request_new_section(self):
        response = self.client.post('/manage-courses/', {'action': 'request_new', 'course_id': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])
        self.assertTrue(response.context['new'])

    def test_post_new_section(self):
        response = self.client.post('/manage-courses/', {'action': 'new_section', 'section_id': '2', 'course_id': '1',
                                                         'section_type': 'Lecture', 'user': self.existing_user})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])
        self.assertTrue(response.context['new'])

    def test_post_delete_section(self):
        response = self.client.post('/manage-courses/',
                                    {'action': 'delete_section', 'section_id': '1', 'course_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])
        self.assertFalse(response.context['new'])

    def test_post_invalid_action(self):
        response = self.client.post('/manage-courses/', {'action': 'invalid_action'})

        self.assertEqual(response.status_code, 200)  # Should return a response even for an invalid action

    def test_post_add_user(self):
        response = self.client.post('/manage-courses/', {'action': 'add_user', 'course_id': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('course', response.context)
        self.assertIn('eligible_users', response.context)
        self.assertTrue(response.context['popup'])
        self.assertFalse(response.context['edit'])

    def test_post_view_section(self):
        response = self.client.post('/manage-courses/', {'action': 'view_section', 'course_id': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)
        self.assertTrue(response.context['popup'])
        self.assertFalse(response.context['edit'])
