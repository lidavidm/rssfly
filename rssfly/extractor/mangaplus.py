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

import structlog

from rssfly.extractor import mangaplus_pb2
from rssfly.extractor.common import Chapter, Comic, Context, Extractor

logger = structlog.get_logger(__name__)


class MangaplusExtractor(Extractor):
    @property
    def name(self):
        return "mangaplus"

    @property
    def publisher(self):
        return "Shueisha MangaPlus"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://jumpg-webapi.tokyo-cdn.com/api/title_detail?title_id={comic_id}"
        logger.info("Fetching from MangaPlus API", url=url)
        raw_bytes = context.get_bytes(url)

        response = mangaplus_pb2.SeriesResponse()
        response.ParseFromString(raw_bytes)

        chapters = {}
        for chapter in response.series.series.chapters:
            chapter_id = "{:09}".format(int(chapter.number.lstrip("#")))
            chapter_title = chapter.title
            chapter_url = (
                f"https://mangaplus.shueisha.co.jp/viewer/{chapter.chapter_id}"
            )
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: int(chapter.chapter_id))
        )
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=response.series.series.description.title,
            url=f"https://mangaplus.shueisha.co.jp/titles/{comic_id}",
            chapters=chapter_list,
        )
