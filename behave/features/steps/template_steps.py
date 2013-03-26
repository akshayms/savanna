from behave import *
from random import choice, randint
from string import ascii_lowercase
from sys import path
import RestApi
import json

path.append(path.append(".."))
rest = RestApi.RestApi()

@When('User see templates')
def get_templates(context):
    global error_content
    global status_code
    global res_content_list_templates
    res_content_list_templates = []
    res = rest.get_templates()
    status_code = res.status_code
    if status_code == 200:
        res_content_list_templates = json.loads(res.content)
    else:
        error_content = json.loads(res.content)


@When('User get template with id: "{n}"')
def get_template(context, n):
    global error_content
    global status_code
    global res_content_get_template
    try:
        num = context.ids[int(n)]
    except Exception, e: num = "0000000001"
    res = rest.get_template(num)
    status_code = res.status_code
    if status_code == 200:
        res_content_get_template = json.loads(res.content)
    else:
        error_content = json.loads(res.content)


@Given("node_template body")
def node_template_body(context):
    global template_body
    template_body = context.text


@When('User create template')
def add_template(context):
    global error_content
    global template_body
    global status_code
    global res_content
    res = rest.create_template(template_body)
    status_code = res.status_code
    if status_code == 202:
        res_content = json.loads(res.content)
        context.ids.append(res_content['node_template'].get(u'id'))
    else:
        error_content = json.loads(res.content)


@When('User delete template with id: "{n}"')
def del_template(context, n):
    global error_content
    global status_code
    try:
        num = context.ids[int(n)]
    except Exception, e: num = "0000000001"
    res = rest.delete_template(num)
    status_code = res.status_code
    if status_code != 204:
        error_content = json.loads(res.content)


@When('User put template with id: "{n}"')
def put_template(context, n):
    global error_content
    global status_code
    global res_content
    global template_body
    try:
        num = context.ids[int(n)]
    except Exception, e: num = "0000000001"
    res = rest.create_template(template_body, num)
    status_code = res.status_code
    if status_code == 202:
        res_content = json.loads(res.content)
    else:
        error_content = json.loads(res.content)
