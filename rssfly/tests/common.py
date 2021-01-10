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

import os
from pathlib import Path
from typing import Dict


class FakeContext:
    def __init__(self, urls: Dict[str, str]):
        self._urls = urls

    def get_text(self, url, **kwargs):
        # TODO: raise proper error
        return self._urls[url]


def get_test_data(path: str) -> str:
    root = Path(os.environ.get("RSSFLY_TEST_DATA_ROOT", ".")) / path
    with root.open() as f:
        return f.read()
