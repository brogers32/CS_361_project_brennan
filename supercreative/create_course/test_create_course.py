from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from supercreative.models import (User, Course, Section)
from supercreative.create_course.create_course import create_course


class LoginUnitTest(TestCase):
    course = None
    role = None

    def setUp(self):

        # create a mock course
        '''
        self.course = Course.objects.create(course_id=1, course_name="Intro to Software Engineering",
                                            course_description="stuff", course_code="COMPSCI-361")
        '''

        new_course = Course(
            course_id=1,
            course_name="Intro to Software Engineering",
            course_description="stuff",
            course_code="COMPSCI-361"
        )

        new_course.save()

        self.course = new_course

        # create a mock user
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="administrator", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")

    def test_correct_course(self):
        # correctly create a course
        self.assertTrue(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                      self.course.course_code, self.user.role),
                        "create_course did not return true when it should have.")

        # get created course and check its values
        created_course = Course.objects.get(course_id=self.course.course_id)

        self.assertEqual(created_course.course_id, self.course.course_id, "create_course did not correctly set the "
                                                                          "course_id")

        self.assertEqual(created_course.course_name, self.course.course_name, "create_course did not correctly set the "
                                                                              "course_name")

        self.assertEqual(created_course.course_description, self.course.course_description, "create_course did not "
                                                                                            "correctly set the "
                                                                                            "course_description")

        self.assertEqual(created_course.course_code, self.course.course_code, "create_course did not correctly set the "
                                                                              "course_code")

    def test_invalid_course_id(self):
        # attempt to create a course with various invalid course ids
        self.assertFalse(create_course("wrong", self.course.course_name, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course("1", self.course.course_name, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(None, self.course.course_name, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(-1, self.course.course_name, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=self.course.course_name)

    def test_invalid_course_name(self):
        # attempt to create a course with various invalid course names
        self.assertFalse(create_course(self.course.course_id, 1, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, True, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, None, self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=self.course.course_id)

    def test_invalid_course_description(self):
        # attempt to create a course with various invalid course descriptions
        self.assertFalse(create_course(self.course.course_id, self.course.course_name, 1,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, False,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, None,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=self.course.course_id)

    def test_invalid_course_code(self):
        # attempt to create a course with various invalid course codes
        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       1, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       True, self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       None, self.user.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=self.course.course_id)

    def test_invalid_role(self):
        # attempt to create a course with invalid user role
        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       self.course.course_code, ""),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       self.course.course_code, "student"),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                                       self.course.course_code, None),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=self.course.course_id)

    def test_duplicates(self):
        # create a course
        create_course(self.course.course_id, self.course.course_name, self.course.course_description,
                      self.course.course_code, self.user.role)

        # try to create additional courses with duplicate values
        self.assertFalse(create_course(self.course.course_id, "different course name", self.course.course_description,
                                       "different course code", self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(3, self.course.course_name, self.course.course_description,
                                       "different course code", self.user.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(3, "different course name", self.course.course_description,
                                       self.course.course_code, self.user.role),
                         "create_course did not return false when it should have.")

        # make sure none of the courses with duplicate values were created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_name="different course name")

        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_id=3)

        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            created_course = Course.objects.get(course_code="different course code")
