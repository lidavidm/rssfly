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
from rssfly.extractor.comic_walker import ComicWalkerExtractor
from rssfly.extractor.mangaplus import MangaplusExtractor
from rssfly.extractor.pixiv import PixivExtractor
from rssfly.extractor.pixiv_fanbox import FanboxExtractor
from rssfly.extractor.tappytoon import TappytoonExtractor
from rssfly.extractor.twi4 import Twi4Extractor
from rssfly.extractor.webnewtype import ComicNewtypeExtractor
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


def test_comic_walker():
    comic_id = "KDCW_KS13202228010000_68"
    url = f"https://comic-walker.com/contents/detail/{comic_id}"
    context = FakeContext(
        {
            url: get_test_data(f"comic_walker.{comic_id}.html").decode(),
        }
    )
    comic = ComicWalkerExtractor().extract(context, comic_id)
    assert comic.name == "クラスの大嫌いな女子と結婚することになった。"
    assert comic.publisher == "Kadokawa"
    assert comic.publisher == ComicWalkerExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 9
    assert comic.chapters[-1].chapter_id == "第5話-2"
    assert comic.chapters[-1].name == "クラスの大嫌いな女子と結婚することになった。 第5話-2"
    assert (
        comic.chapters[-1].url
        == "https://comic-walker.com/viewer/?tw=2&dlcl=ja&cid=KDCW_KS13202228010009_68"
    )


def test_comic_newtype():
    comic_id = "watatsuyo"
    series_url = f"https://comic.webnewtype.com/contents/{comic_id}/"
    url = f"https://comic.webnewtype.com/contents/{comic_id}/more/1/"
    context = FakeContext(
        {
            series_url: get_test_data(f"newtype.{comic_id}.html").decode(),
            url: get_test_data(f"newtype.{comic_id}.json").decode(),
        }
    )
    comic = ComicNewtypeExtractor().extract(context, comic_id)
    assert comic.name == "私より強い男と結婚したいの"
    assert comic.publisher == "Kadokawa"
    assert comic.publisher == ComicNewtypeExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 1
    assert comic.chapters[-1].chapter_id == "000001001"
    assert comic.chapters[-1].name == "第01話"
    assert (
        comic.chapters[-1].url
        == "https://comic.webnewtype.com/contents/watatsuyo/1001/"
    )


def test_comic_newtype_longer():
    comic_id = "fuzoroi"
    series_url = f"https://comic.webnewtype.com/contents/{comic_id}/"
    url = f"https://comic.webnewtype.com/contents/{comic_id}/more/1/"
    context = FakeContext(
        {
            series_url: get_test_data(f"newtype.{comic_id}.html").decode(),
            url: get_test_data(f"newtype.{comic_id}.json").decode(),
        }
    )
    comic = ComicNewtypeExtractor().extract(context, comic_id)
    assert comic.name == "不揃いの連理"
    assert comic.publisher == "Kadokawa"
    assert comic.publisher == ComicNewtypeExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 18
    assert comic.chapters[-1].chapter_id == "000000170"
    assert comic.chapters[-1].name == "第十七話"
    assert (
        comic.chapters[-1].url == "https://comic.webnewtype.com/contents/fuzoroi/170/"
    )


def test_fanbox():
    comic_id = "niichi021"
    url = f"https://api.fanbox.cc/post.listCreator?creatorId={comic_id}&limit=10"
    context = FakeContext(
        {
            url: get_test_data(f"fanbox.{comic_id}.json").decode(),
        }
    )
    comic = FanboxExtractor().extract(context, comic_id)
    assert comic.name == "にいち’s Fanbox"
    assert comic.publisher == "Fanbox"
    assert comic.publisher == FanboxExtractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 10
    assert comic.chapters[-1].chapter_id == "000002751947"
    assert comic.chapters[-1].name == "【ちょっとだけ先読み】現実もたまには嘘をつく98"
    assert comic.chapters[-1].url == "https://niichi021.fanbox.cc/posts/2751947"


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
    assert comic.chapters[-1].chapter_id == "001010076"
    assert comic.chapters[-1].name == "Special Illustration 5"
    assert comic.chapters[-2].chapter_id == "000000053"
    assert comic.chapters[-2].name == "MISSION 53"
    print(comic.chapters)


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


def test_twi4():
    comic_id = "nekonote"
    url = f"https://sai-zen-sen.jp/comics/twi4/{comic_id}/"
    context = FakeContext(
        {
            url: get_test_data(f"twi4.{comic_id}.html"),
        }
    )
    comic = Twi4Extractor().extract(context, comic_id)
    assert comic.name == "猫の手だって役に立つ"
    assert comic.publisher == "Saizensen"
    assert comic.publisher == Twi4Extractor().publisher
    assert comic.comic_id == comic_id
    assert len(comic.chapters) == 11
    assert comic.chapters[-1].chapter_id == "000000000011"
    assert comic.chapters[-1].name == "NOBEL『癖』 #0011"
