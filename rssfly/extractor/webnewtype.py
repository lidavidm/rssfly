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

import json
import urllib.parse

import structlog
from bs4 import BeautifulSoup

from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class ComicNewtypeExtractor(Extractor):
    @property
    def name(self):
        return "Comic Newtype"

    @property
    def publisher(self):
        return "Kadokawa"

    def extract(self, context: Context, comic_id: str) -> Comic:
        series_url = f"https://comic.webnewtype.com/contents/{comic_id}/"
        url = f"https://comic.webnewtype.com/contents/{comic_id}/more/1/"
        logger.info(
            "Fetching from comic.webnewtype.com", series_url=series_url, url=url
        )
        raw_text = context.get_bytes(url)
        payload = json.loads(raw_text)

        chapters = {}
        root = BeautifulSoup(payload["html"], features="html.parser")
        for el in root.find_all("li"):
            chapter_title = el.find(class_="number").text
            chapter_url = urllib.parse.urljoin(url, el.find("a").attrs["href"])
            _, _, raw_id = el.attrs["id"].partition("_")
            chapter_id = "{:09}".format(int(raw_id))
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: int(chapter.chapter_id))
        )

        root = BeautifulSoup(context.get_text(series_url), features="html.parser")
        comic_name, _, _ = root.find("title").text.partition(" - ")
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=comic_name,
            url=url,
            chapters=chapter_list,
        )
