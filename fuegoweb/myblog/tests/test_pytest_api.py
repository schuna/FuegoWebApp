import pytest
import json
import logging
from django.urls import reverse
from myblog.models import Posts

post_url = reverse("myblog-list")
pytestmark = pytest.mark.django_db


def test_zero_posts_should_return_empty_list(client):
    response = client.get(post_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_posts_should_success(client):
    test_post = Posts.objects.create(
        description="test11", image_path="/home/picture/11", user_id=11
    )
    response = client.get(post_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("description") == test_post.description
    assert response_content.get("image_path") == test_post.image_path
    assert response_content.get("user_id") == test_post.user_id


def test_create_posts_without_arguments_should_fail(client):
    response = client.post(path=post_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "description": ["This field is required."],
        "image_path": ["This field is required."],
        "user_id": ["This field is required."],
    }


def test_create_existing_description_should_fail(client):
    Posts.objects.create(description="test", image_path="/home/picture/1", user_id=2)
    response = client.post(path=post_url, data={"image_path": "/home/picture/1"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "description": ["This field is required."],
        "image_path": ["posts with this image path already exists."],
        "user_id": ["This field is required."],
    }


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
