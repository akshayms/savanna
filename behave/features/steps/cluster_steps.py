from behave import *
from random import choice, randint
from string import ascii_lowercase
from sys import path
from time import sleep
import RestApi
import json

path.append(path.append(".."))
rest = RestApi.RestApi()

@When('User see clusters')
def get_clusters(context):
    global status_code
    global error_content
    global res_content_list_clusters
    res_content_list_clusters = []
    res = rest.get_clusters()
    status_code = res.status_code
    if status_code == 200:
        res_content_list_clusters = json.loads(res.content)
    else:
        error_content = json.loads(res.content)


@When('User get cluster with id: "{n}"')
def get_cluster(context, n):
    global status_code
    global res_content_get_cluster
    global error_content
    try:
        num = context.ids[int(n)]
    except Exception, e: num = 0000000000001
    res = rest.get_cluster(num)
    status_code = res.status_code
    if status_code == 200:
        res_content_get_cluster = json.loads(res.content)
    else:
        error_content = json.loads(res.content)


@Given('cluster data')
def create_cluster_body(context):
    global cluster_body
    cluster_body = context.text


@When('User create cluster')
def add_cluster(context):
    global cluster_body
    global status_code
    global res_content
    global error_content
    res = rest.create_cluster(cluster_body)
    status_code = res.status_code
    if status_code == 202:
        #sleep(60)
        res_content = json.loads(res.content)
        context.ids.append(res_content['cluster'].get(u'id'))
    else:
        error_content = json.loads(res.content)


@When('User delete cluster with id: "{n}"')
def del_cluster(context, n):
    global status_code
    global error_content
    try:
        num = context.ids[int(n)]
    except Exception, e: num = 0000000000001
    res = rest.delete_cluster(num)
    status_code = res.status_code
    if status_code != 204:
        error_content = json.loads(res.content)


@When('User put cluster with id: "{n}"')
def put_cluster(context, n):
    global status_code
    global res_content
    global cluster_body
    global error_content
    try:
        num = context.ids[int(n)]
    except Exception, e: num = 0000000000001
    res = rest.create_cluster(cluster_body, num)
    status_code = res.status_code
    if status_code == 202:
        res_content = json.loads(res.content)
    else:
        error_content = json.loads(res.content)
