import json
import pytest
import logging
from unittest import TestCase
from django.test import Client
from django.urls import reverse
from myblog.models import Posts


@pytest.mark.django_db
class BasicPostsApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.post_url = reverse("myblog-list")

    def tearDown(self) -> None:
        pass


class TestGetPosts(BasicPostsApiTestCase):
    def test_zero_posts_should_return_empty_list(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_posts_should_success(self):
        test_post = Posts.objects.create(
            description="test11", image_path="/home/picture/11", user_id=11
        )
        response = self.client.get(self.post_url)
        # print(response.content)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("description"), test_post.description)
        self.assertEqual(response_content.get("image_path"), test_post.image_path)
        self.assertEqual(response_content.get("user_id"), test_post.user_id)


class TestPostPosts(BasicPostsApiTestCase):
    def test_create_posts_without_arguments_should_fail(self):
        response = self.client.post(path=self.post_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": ["This field is required."],
                "image_path": ["This field is required."],
                "user_id": ["This field is required."],
            },
        )

    def test_create_existing_description_should_fail(self):
        Posts.objects.create(
            description="test", image_path="/home/picture/1", user_id=2
        )
        response = self.client.post(
            path=self.post_url, data={"image_path": "/home/picture/1"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {
                "description": ["This field is required."],
                "image_path": ["posts with this image path already exists."],
                "user_id": ["This field is required."],
            },
        )

    # @pytest.mark.xfail
    # def test_should_be_ok_if_fails(self):
    #     self.assertEqual(1, 2)
    #
    # @pytest.mark.skip
    # def test_skip(self):
    #     self.assertEqual(1, 2)


def raise_posts_exception():
    raise ValueError("Posts Exception")


def test_raise_posts_exception_should_pass():
    with pytest.raises(ValueError) as e:
        raise_posts_exception()
    assert "Posts Exception" == str(e.value)


logger = logging.getLogger("POSTS_LOGS")


def function_that_logs_something():
    try:
        raise ValueError("Posts Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog):
    function_that_logs_something()
    assert "I am logging Posts Exception" in caplog.text


def test_logged_info_level(caplog):
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text
