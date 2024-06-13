import boto3
from moto import mock_aws
from challenge.challenge_python import get_s3_objects, fn_caller


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


def test_Helper():
    pass
