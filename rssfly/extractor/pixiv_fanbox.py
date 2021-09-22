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


_DEFAULT_HEADERS = {
    "user-agent": "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "accept": "application/json",
}


class FanboxExtractor(Extractor):
    @property
    def name(self):
        return "pixiv_fanbox"

    @property
    def publisher(self):
        return "Fanbox"

    def extract(self, context: Context, comic_id: str) -> Comic:
        url = f"https://api.fanbox.cc/post.listCreator?creatorId={comic_id}&limit=10"
        logger.info("Fetching from Fanbox API", url=url)
        headers = _DEFAULT_HEADERS.copy()
        headers["referer"] = f"https://{comic_id}.fanbox.cc"
        headers["origin"] = headers["referer"]
        raw_bytes = context.get_bytes(url, headers=headers)

        response = json.loads(raw_bytes)

        chapters = {}
        for chapter in response["body"]["items"]:
            chapter_id = "{:012}".format(int(chapter["id"]))
            chapter_title = chapter["title"]
            chapter_url = f"https://{comic_id}.fanbox.cc/posts/{chapter['id']}"
            # Deduplicate by URL
            chapters[chapter_url] = Chapter(
                chapter_id=chapter_id,
                name=chapter_title,
                url=chapter_url,
            )
        chapter_list = list(
            sorted(chapters.values(), key=lambda chapter: chapter.chapter_id)
        )
        return Comic(
            publisher=self.publisher,
            comic_id=comic_id,
            name=response["body"]["items"][0]["user"]["name"] + "’s Fanbox",
            url=f"https://{comic_id}.fanbox.cc",
            chapters=chapter_list,
        )
