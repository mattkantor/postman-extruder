from main import deconstruct, generate_tests_from_js
import pytest

def no_test_sample():
    sample = "./sample.json"
    deconstruct(sample)


def test_rewrite_code():
    sample_test_js = ["pm.test(\"Status code is 200\", function () {","    pm.response.to.have.status(200);","});"]
    tests = generate_tests_from_js(sample_test_js)
    assert tests=="200"


