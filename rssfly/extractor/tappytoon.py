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

import structlog
from bs4 import BeautifulSoup

from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class TappytoonExtractor(Extractor):
    @property
    def name(self):
        return "tappytoon"

    @property
    def publisher(self):
        return "Tappytoon"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://www.tappytoon.com/en/comics/{comic_id}"
        logger.info("Fetching from tappytoon.com", url=url)
        raw_text = context.get_text(url)
        root = BeautifulSoup(raw_text, features="html.parser")
        data = json.loads(root.find("script", id="__NEXT_DATA__").string)
        chapters = {}
        chapter_data = data["props"]["initialState"]["entities"]["chapters"]
        for chapter in chapter_data.values():
            if not chapter["isAccessible"]:
                # Exclude "not yet"
                continue
            chapter_id = "{:09}".format(chapter["order"])
            chapter_title = chapter["title"]
            chapter_url = f"https://www.tappytoon.com/en/chapters/{chapter['id']}"
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: int(chapter.chapter_id))
        )
        comic_data = data["props"]["initialState"]["entities"]["comics"]
        comic_data = comic_data[next(iter(comic_data.keys()))]
        comic_name = comic_data["title"]
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=comic_name,
            url=url,
            chapters=chapter_list,
        )
