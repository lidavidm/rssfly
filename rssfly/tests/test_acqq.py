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
from rssfly.extractor.mangaplus import MangaplusExtractor
from rssfly.extractor.pixiv import PixivExtractor
from rssfly.extractor.sunday_webry import SundayWebryExtractor
from rssfly.extractor.tappytoon import TappytoonExtractor
from rssfly.tests.common import FakeContext, get_test_data


def test_acqq():
    comic_id = "646277"
    url = f"https://ac.qq.com/Comic/comicInfo/id/{comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"acqq.{comic_id}.html").decode(),
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


def test_mangaplus():
    comic_id = "100145"
    url = f"https://jumpg-webapi.tokyo-cdn.com/api/title_detail?title_id={comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"mangaplus.{comic_id}.bin"),
        }
    )
    comic = MangaplusExtractor().extract(context, comic_id)
    assert comic.name == "WITCH WATCH"
    assert comic.publisher == "Shueisha MangaPlus"
    assert comic.publisher == MangaplusExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 1
    assert comic.chapters[-1].chapter_id == "000000001"
    assert comic.chapters[-1].name == "1 Witch's Return"


def test_mangaplus_timelimit():
    comic_id = "100056"
    url = f"https://jumpg-webapi.tokyo-cdn.com/api/title_detail?title_id={comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"mangaplus.{comic_id}.bin"),
        }
    )
    comic = MangaplusExtractor().extract(context, comic_id)
    assert comic.name == "SPY x FAMILY"
    assert comic.publisher == "Shueisha MangaPlus"
    assert comic.publisher == MangaplusExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 6
    assert comic.chapters[0].chapter_id == "000000001"
    assert comic.chapters[0].name == "MISSION:1"
    assert comic.chapters[-2].chapter_id == "000000045"
    assert comic.chapters[-2].name == "MISSION: 45"


def test_pixiv():
    comic_id = "60488"
    url = f"https://www.pixiv.net/ajax/series/{comic_id}?p=1&lang=en"
    context = FakeContext(
        {
            url: get_test_data(f"pixiv.{comic_id}.json").decode(),
        }
    )
    comic = PixivExtractor().extract(context, comic_id)
    assert comic.name == "現実もたまには嘘をつく"
    assert comic.publisher == "Pixiv"
    assert comic.publisher == PixivExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 12
    assert comic.chapters[-1].chapter_id == "000091330005"
    assert comic.chapters[-1].name == "現実もたまには嘘をつく92「ならなくていいのよ」"
    assert comic.chapters[-1].url == "https://www.pixiv.net/en/artworks/91330005"


def test_sunday_webry():
    comic_id = "5743"
    url = f"https://www.sunday-webry.com/detail.php?title_id={comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"sunday_webry.{comic_id}.html").decode(),
        }
    )
    comic = SundayWebryExtractor().extract(context, comic_id)
    assert comic.name == "ちょっとだけ抜けちゃう柊さん"
    assert comic.publisher == "Shogakukan"
    assert comic.publisher == SundayWebryExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 4
    assert comic.chapters[-1].chapter_id == "000000005"
    assert comic.chapters[-1].name == "第5話"


def test_tappytoon():
    comic_id = "villainess-turns-hourglass"
    url = f"https://www.tappytoon.com/en/comics/{comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"tappytoon.{comic_id}.html").decode(),
        }
    )
    comic = TappytoonExtractor().extract(context, comic_id)
    assert comic.name == "The Villainess Turns the Hourglass"
    assert comic.publisher == "Tappytoon"
    assert comic.publisher == TappytoonExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 42
    assert comic.chapters[-1].chapter_id == "000000041"
    assert comic.chapters[-1].name == "Episode 42"
