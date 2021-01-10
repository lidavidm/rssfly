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

import urllib.parse

import structlog
from bs4 import BeautifulSoup

from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class AcqqExtractor(Extractor):
    @property
    def name(self):
        return "acqq"

    @property
    def publisher(self):
        return "腾讯动漫"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://ac.qq.com/Comic/comicInfo/id/{comic_id}"
        logger.info("Fetching from ac.qq.com", url=url)
        raw_text = context.get_text(url)
        root = BeautifulSoup(raw_text, features="html.parser")
        chapter_els = root.find_all(class_="works-chapter-item")
        chapters = {}
        for chapter_el in chapter_els:
            link = chapter_el.find("a")
            chapter_title = link.attrs["title"]
            chapter_url = urllib.parse.urljoin(url, link.attrs["href"])
            chapter_id = "{:09}".format(int(link.attrs["href"].split("/")[-1]))
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: int(chapter.chapter_id))
        )
        comic_name = root.find(class_="works-intro-title").text
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=comic_name,
            url=url,
            chapters=chapter_list,
        )
