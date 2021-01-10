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

from bs4 import BeautifulSoup

from rssfly.extractor.common import Chapter, Comic, Context


def extract(context: Context, url: str) -> Comic:
    root = BeautifulSoup(context.get_text(url), features="html.parser")
    chapter_els = root.find_all(class_="works-chapter-item")
    chapters = {}
    for chapter_el in chapter_els:
        link = chapter_el.find("a")
        chapter_title = link.attrs["title"]
        chapter_url = urllib.parse.urljoin(url, link.attrs["href"])
        chapter_id = link.attrs["href"].split("/")[-1]
        # Deduplicate by URL
        chapters[chapter_url] = Chapter(
            id=chapter_id,
            name=chapter_title,
            url=chapter_url,
        )
    chapter_list = list(sorted(chapters.values(), key=lambda chapter: int(chapter.id)))
    comic_name = root.find(class_="works-intro-title").text
    return Comic(
        id=url.split("/")[-1],
        name=comic_name,
        chapters=chapter_list,
    )
