# Copyright 2021 David Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
from typing import List, NamedTuple

import requests


class Context:
    def __init__(self, session: requests.Session):
        self._session = session

    def get_text(self, *args, **kwargs):
        response = self._session.get(*args, **kwargs)
        response.raise_for_status()
        return response.text

    def get_bytes(self, *args, **kwargs):
        response = self._session.get(*args, **kwargs)
        response.raise_for_status()
        return response.content


class Chapter(NamedTuple):
    chapter_id: str
    name: str
    url: str
    # TODO: optional date?


class Comic(NamedTuple):
    publisher: str
    comic_id: str
    name: str
    url: str
    chapters: List[Chapter]


class Extractor:
    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def publisher(self):
        raise NotImplementedError

    @abc.abstractmethod
    def extract(self, context: Context, comic_id: str) -> Comic:
        raise NotImplementedError
