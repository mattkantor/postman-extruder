import json
import sys
import os
import traceback
import re
import argparse
from collections import defaultdict

test_output =  dict()

def _export_data(_group_name,_name, method, header, url, payload, code):
    new_item = dict(name=_name, method=method, header=header, url=url, payload=payload, code=code)
    if _group_name in test_output:
        to_put = test_output[_group_name]
        to_put = to_put.append(new_item)
        test_output[_group_name] = to_put
    else:
        test_output[_group_name] = [new_item]

def debug(text):
    print("------------------------")
    print("\t %s" % text)
    print("------------------------")

def generate_tests_from_js(text):
    for _test in text:
        if "pm.response.to.have.status" in _test:
            statuses = re.findall(r'\d+', _test)
            if len(statuses)>0:
                return statuses[0]
    return 0
def parse_body(content):
    payload = ""
    if content["mode"] == "raw":
        payload = content["raw"]
    return payload

def parse_request(content):
    method = content["method"]
    header = content["header"] #array
    url = content["url"]
    return method, header, url

def convert_url_using_variables(url):
    return url


def parse_test(_group_name, _test):

    _test_name = _test["name"]
    if "event" in _test:
        code = ""
        payload=""
        method="get"
        header=""
        url=""
        for event in _test["event"]:
            if "listen" in event and event["listen"] == "test":
                code = event["script"]["exec"]
                code = generate_tests_from_js(code)
        if "request" in _test:
            method, header, url = parse_request(_test["request"])
        if "body" in _test:
            payload = parse_body(_test["body"])
        _export_data(_group_name, _test_name, method, header, url, payload, code)
    if "item" in _test:
        for _subitem in _test["item"]:
            parse_test(_group_name,_subitem)


def deconstruct(filePath):
    print('\t Deconstructing %s' % filePath)
    with open(filePath) as json_file:
        try:
            data = json.load(json_file)
            _test_info = data["info"]
            _group_name = _test_info["name"]
            debug(_group_name)
            _item = data["item"]
            for _test in _item:
                parse_test(_group_name,_test)

        except Exception as e:
            print(e)
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # traceback.print_tb(exc_traceback)
    return


# Set the directory you want to start from
def run(env_dir,env_file):
    rootDir = env_dir
    for dirName, subdirList, fileList in os.walk(rootDir):
        if ".git" not in dirName:
            print('Found directory: %s' % dirName)
            for fname in fileList:
                if ".json" in fname :
                    deconstruct(dirName +"/"+ fname)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Convert tests')
    parser.add_argument('root_dir', metavar='p',  action="store",
                        help='location of the postman files', default='../guest-integration')

    parser.add_argument('environment_file', metavar='e', action="store",
                        help='location of the environment file to use')

    args = parser.parse_args()



    run(args.root_dir, args.environment_file)
    print(test_output)