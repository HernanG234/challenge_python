import boto3
import requests
import requests_mock
import pytest
from moto import mock_aws
from challenge.challenge_python import get_s3_objects, fn_caller, Helper


@mock_aws
def test_get_s3_objects():
    # Setup the mock S3 environment
    s3 = boto3.client("s3")
    bucket_name = "my-test-bucket"
    s3.create_bucket(Bucket=bucket_name)

    # Add some objects to the bucket
    objects = [
        {"Key": "my-prefix/object1", "Body": "data1"},
        {"Key": "my-prefix/object2", "Body": "data2"},
        {"Key": "other-prefix/object3", "Body": "data3"},
    ]
    for obj in objects:
        s3.put_object(Bucket=bucket_name, Key=obj["Key"], Body=obj["Body"])

    # Collect all objects that match the prefix
    result = list(get_s3_objects(bucket_name, "my-prefix"))

    # Assert the results
    assert len(result) == 2
    assert result[0]["Key"] == "my-prefix/object1"
    assert result[1]["Key"] == "my-prefix/object2"

    # Test without prefix (should return all objects)
    result = list(get_s3_objects(bucket_name, ""))

    # Assert the results
    assert len(result) == 3
    assert result[0]["Key"] == "my-prefix/object1"
    assert result[1]["Key"] == "my-prefix/object2"
    assert result[2]["Key"] == "other-prefix/object3"


def test_fn():
    """
    No new code written in this function, do not test it.
    """
    pass


def test_fn_caller():
    ret = fn_caller("add", 1, 2)
    assert ret == 3

    ret = fn_caller("concat", 1, 2)
    assert ret == "1,2"

    ret = fn_caller("divide", 10, 2)
    assert ret == 5

    ret = fn_caller("multiply", 2, 3)
    assert ret == 6


def test_fn_transcoder():
    """
    No new code written in this function, do not test it.
    """
    pass


@pytest.fixture
def helper():
    helper = Helper()
    helper.AUTHORIZATION_TOKEN = {
        "access_token": "fake_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "fake_refresh_token",
    }
    return helper


def test_Helper_search_images(helper, requests_mock):
    requests_mock.get(
        f"{helper.DOMAIN}/{helper.SEARCH_IMAGES_ENDPOINT}",
        json={"results": ["image1", "image2"]},
        status_code=200,
    )
    ret = helper.search_images()
    assert ret.status_code == 200
    assert ret.json() == {"results": ["image1", "image2"]}


def test_Helper_get_image(helper, requests_mock):
    requests_mock.get(
        f"{helper.DOMAIN}/{helper.GET_IMAGE_ENDPOINT}/1",
        json={"url": "https://s3.download/fakeid"},
        status_code=200,
    )
    ret = helper.get_image(1)

    assert ret.status_code == 200
    assert ret.json() == {"url": "https://s3.download/fakeid"}

    requests_mock.get(
        f"{helper.DOMAIN}/{helper.GET_IMAGE_ENDPOINT}/2",
        json={"url": "Not Found"},
        status_code=404,
    )
    ret = helper.get_image(2)

    assert ret.status_code == 404
    assert ret.json() == {"url": "Not Found"}


def test_Helper_download_image(helper, requests_mock):
    requests_mock.post(
        f"{helper.DOMAIN}/{helper.DOWNLOAD_IMAGE_ENDPOINT}/1",
        json={"url": "https://s3.download/fakeid"},
        status_code=200,
    )
    ret = helper.download_image(1)

    assert ret.status_code == 200
    assert ret.json() == {"url": "https://s3.download/fakeid"}

    requests_mock.post(
        f"{helper.DOMAIN}/{helper.DOWNLOAD_IMAGE_ENDPOINT}/2",
        json={"url": "Not Found"},
        status_code=404,
    )
    ret = helper.download_image(2)

    assert ret.status_code == 404
    assert ret.json() == {"url": "Not Found"}
