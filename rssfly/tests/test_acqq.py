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

from rssfly.extractor.acqq import AcqqExtractor
from rssfly.extractor.tappytoon import TappytoonExtractor
from rssfly.tests.common import FakeContext, get_test_data


def test_acqq():
    comic_id = "646277"
    url = f"https://ac.qq.com/Comic/comicInfo/id/{comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"acqq.{comic_id}.html"),
        }
    )
    comic = AcqqExtractor().extract(context, comic_id)
    assert comic.name == "暗恋"
    assert comic.publisher == "腾讯动漫"
    assert comic.publisher == AcqqExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 25
    assert comic.chapters[-1].chapter_id == "000000025"
    assert comic.chapters[-1].name == "暗恋：暗恋20"


def test_tappytoon():
    comic_id = "villainess-turns-hourglass"
    url = f"https://www.tappytoon.com/en/comics/{comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"tappytoon.{comic_id}.html"),
        }
    )
    comic = TappytoonExtractor().extract(context, comic_id)
    assert comic.name == "The Villainess Turns the Hourglass"
    assert comic.publisher == "Tappytoon"
    assert comic.publisher == TappytoonExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 43
    print(comic.chapters)
    assert comic.chapters[-1].chapter_id == "000000042"
    assert comic.chapters[-1].name == "Episode 43"
