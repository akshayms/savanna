# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import savanna.tests.integration.base
import savanna.tests.integration.parameters as param
import telnetlib


def empty_object_id(expr):
    return '' if expr else param.IMAGE_ID


def print_data(expr):
    return True if expr else False


# def set_tag():
#     return '/tag'
#
#
# def set_untag():
#     return '/untag'


class TestsCRUDImageRegistry(savanna.tests.integration.base.ITestCase):

    def get_images_list(self):
        data = self.get_object(self.url_images, empty_object_id(True),
                               200, print_data(False))
        return data

    def set_description_username(self, description, username):
        url = self.url_images + '/' + param.IMAGE_ID
        body = dict(
            description='%s' % description,
            username='%s' % username
        )
        data = self.post_object(url, body, 202)
        return data

    def get_image_by_tags(self, tag_name):
        url = self.url_images + '?tags=' + tag_name
        data = self.get_object(
            url, empty_object_id(True), 200, print_data(False))
        return data

    def set_tags_untags_image(self, url_part, tag_name):
        url = self.url_images + '/' + param.IMAGE_ID + url_part
        tag = []
        tag.append('%s' % tag_name)
        body = dict(tags=tag)
        data = self.post_object(url, body, 202)
        return data

    def get_image_description(self):
        url = self.url_images + '/'
        data = self.get_object(
            url, empty_object_id(False), 200, print_data(False))
        return data

    def setUp(self):
        super(TestsCRUDImageRegistry, self).setUp()
        telnetlib.Telnet(self.host, self.port)

    def test_image_registry(self):
        username = 'ubuntu'
        tag1_name = 'animal'
        tag2_name = 'dog'
        description = 'working image'

        self.get_images_list()
        #self.assertEquals(data['images'][0]['id'], param.IMAGE_ID)

        data = self.set_description_username(description, username)
        self.assertEquals(data['image']['description'], description)
        self.assertEquals(data['image']['username'], username)

        try:
            data = self.set_tags_untags_image('/tag', tag1_name)
            self.assertEquals(data['image']['tags'], [tag1_name])
            data = self.set_tags_untags_image('/tag', tag2_name)
            self.assertEquals(data['image']['tags'], [tag1_name, tag2_name])

        except Exception as e:
            self.set_tags_untags_image('/untag', tag1_name)
            self.set_tags_untags_image('/untag', tag2_name)
            self.fail(e.message)

        data = self.get_image_by_tags(tag1_name)
        self.assertEquals(data['images'][0]['id'], param.IMAGE_ID)
        data = self.get_image_by_tags(tag2_name)
        self.assertEquals(data['images'][0]['id'], param.IMAGE_ID)

        data = self.get_image_description()
        del data['image']['updated']
        del data['image']['progress']
        del data['image']['minRam']
        del data['image']['minDisk']
        del data['image']['metadata']
        del data['image']['created']
        del data['image']['name']
        self.assertEquals(data, dict(image=dict(
            status='ACTIVE',
            username='%s' % username,
            tags=['%s' % tag1_name, '%s' % tag2_name],
            description='%s' % description,
            id='%s' % param.IMAGE_ID
        )))

        data = self.set_tags_untags_image('/untag', tag1_name)
        self.assertEquals(data['image']['tags'], [tag2_name])
        data = self.set_tags_untags_image('/untag', tag2_name)
        self.assertEquals(data['image']['tags'], [])

        data = self.get_image_by_tags(tag1_name)
        self.assertEquals(data['images'], [])
        data = self.get_image_by_tags(tag1_name)
        self.assertEquals(data['images'], [])

        self.get_images_list()
        #self.assertEquals(data['images'][0]['id'], param.IMAGE_ID)
