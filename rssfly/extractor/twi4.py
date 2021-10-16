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
from pathlib import Path

import structlog
from bs4 import BeautifulSoup

from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class Twi4Extractor(Extractor):
    @property
    def name(self):
        return "twi4"

    @property
    def publisher(self):
        return "Saizensen"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://sai-zen-sen.jp/comics/twi4/{comic_id}/"
        logger.info("Fetching from sai-zen-sen.jp", url=url)
        raw_text = context.get_text(url)
        root = BeautifulSoup(raw_text, features="html.parser")
        chapters = {}
        for chapter_el in root.find(id="backnumbers").find_all("li"):
            link_el = chapter_el.find("a")
            chapter_title = link_el.text.strip()
            chapter_url = link_el.attrs["href"]
            chapter_id = Path(urllib.parse.urlparse(chapter_url).path).stem
            chapter_id = "{:012}".format(int(chapter_id))
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: chapter.chapter_id)
        )
        comic_name = root.find("title").text.strip()
        end = comic_name.find("』")
        comic_name = comic_name[1:end]
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=comic_name,
            url=url,
            chapters=chapter_list,
        )
