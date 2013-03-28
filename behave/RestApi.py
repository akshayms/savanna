import requests
from re import match, search, sub
from os.path import dirname, join

echo = True


class RestApi():
    def __init__(self):
        self.baseurl = ""
        self.token = ""
        for line in open(join(dirname(__file__), "config.txt"), "r"):
            m = match('^baseurl\s*=\s*\"(?P<url>http://.*)/*\"$', line)
            if m:
                self.baseurl = m.group("url")

            m = match('^token\s*=\s*\"(?P<token>.*)/*\"$', line)
            if m:
                self.token = m.group("token")
                break

    def execute_post(self, url, body=""):
        URL = self.baseurl + url
        resp = requests.post(URL, data=body, headers={
            "x-auth-token": self.token, "Content-Type": "application/json"})
        if echo:
            print("URL = %s\ndata = %s\nresponse = %s\n"
                  % (URL, body, resp.status_code))
        return resp

    def execute_put(self, url, body=""):
        URL = self.baseurl + url
        resp = requests.put(URL, data=body, headers={
            "x-auth-token": self.token, "Content-Type": "application/json"})
        if echo:
            print("URL = %s\ndata = %s\nresponse = %s\n"
                  % (URL, body, resp.status_code))
        return resp

    def execute_get(self, url):
        URL = self.baseurl + url
        resp = requests.get(URL, headers={"x-auth-token": self.token})
        if echo:
            print("URL = %s\nresponse = %s\n" % (URL, resp.status_code))
        return resp

    def execute_delete(self, url):
        URL = self.baseurl + url
        resp = requests.delete(URL, headers={"x-auth-token": self.token})
        if echo:
            print("URL = %s\nresponse = %s\n" % (URL, resp.status_code))
        return resp

    def get_clusters(self):
        url = "/clusters"
        res = self.execute_get(url)
        return res

    def get_cluster(self, cluster_id):
        url = "/clusters/" + str(cluster_id)
        res = self.execute_get(url)
        return res

    def create_cluster(self, cluster):
        url = "/clusters"
        body = cluster
        res = self.execute_post(url, body)
        return res

    def delete_cluster(self, cluster_id):
        url = "/clusters/" + str(cluster_id)
        res = self.execute_delete(url)
        return res

    def put_cluster(self, cluster_body, cluster_id):
        url = "/clusters/" + str(cluster_id)
        body = cluster_body
        res = self.execute_put(url, body)
        return res

    def get_templates(self):
        url = "/node-templates"
        res = self.execute_get(url)
        return res

    def get_template(self, template_id):
        url = "/node-templates/" + str(template_id)
        res = self.execute_get(url)
        return res

    def create_template(self, template_body):
        url = "/node-templates"
        body = template_body
        res = self.execute_post(url, body)
        return res

    def delete_template(self, template_id):
        url = "/node-templates/" + str(template_id)
        res = self.execute_delete(url)
        return res

    def put_template(self, template_body, template_id):
        url = "/node-templates/" + str(template_id)
        body = template_body
        res = self.execute_put(url, body)
        return res
