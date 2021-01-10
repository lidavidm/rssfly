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

from rssfly.extractor.acqq import extract
from rssfly.extractor.tests.common import FakeContext, get_test_data


def test_extract():
    url = "https://ac.qq.com/Comic/comicInfo/id/646277"
    context = FakeContext(
        {
            url: get_test_data("acqq.646277.html"),
        }
    )
    comic = extract(context, url)
    assert comic.name == "暗恋"
    assert comic.id == "646277"
    assert len(comic.chapters) == 25
    assert comic.chapters[-1].id == "25"
    assert comic.chapters[-1].name == "暗恋：暗恋20"
