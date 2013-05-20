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


class BaseResource(object):
    _resource_name = 'base'

    @property
    def dict(self):
        return self.to_dict()

    @property
    def wrapped_dict(self):
        return {self._resource_name: self.dict}

    def to_dict(self):
        dictionary = self.__dict__.copy()
        return dict([(k, v) for k, v in dictionary.iteritems()
                     if k != '_sa_instance_state'])

    def as_resource(self):
        return Resource(self._resource_name, self.to_dict())


class Resource(BaseResource):
    def __init__(self, _name, _info):
        self._name = _name
        self._info = _info

    def __getattr__(self, k):
        if k not in self.__dict__:
            return self._info.get(k)
        return self.__dict__[k]

    def __repr__(self):
        return '<%s %s>' % (self._name, self._info)

    def __eq__(self, other):
        return self._name == other._name and self._info == other._info

    def to_dict(self):
        return self._info.copy()
