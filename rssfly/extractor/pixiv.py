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

from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class PixivExtractor(Extractor):
    @property
    def name(self):
        return "pixiv"

    @property
    def publisher(self):
        return "Pixiv"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://www.pixiv.net/ajax/series/{comic_id}?p=1&lang=en"
        logger.info("Fetching from MangaPlus API", url=url)
        raw_bytes = context.get_bytes(url)

        response = json.loads(raw_bytes)

        chapters = {}
        # Beyond first 12, seem to be for sidebar
        for chapter in response["body"]["thumbnails"]["illust"][:12]:
            chapter_id = "{:012}".format(int(chapter["id"]))
            chapter_title = chapter["title"]
            chapter_url = f"https://www.pixiv.net/en/artworks/{chapter['id']}"
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: chapter.chapter_id)
        )
        series = [
            series
            for series in response["body"]["illustSeries"]
            if series["id"] == comic_id
        ][0]
        user_id = series["userId"]
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=series["title"],
            url=f"https://www.pixiv.net/user/{user_id}/series/{comic_id}",
            chapters=chapter_list,
        )
