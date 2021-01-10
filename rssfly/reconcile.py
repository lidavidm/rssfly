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

"""Given known chapters and fresh chapters, reconcile the two.

We store known chapters in a database so that we can have a canonical
"publication" time. Else feed readers will constantly see "new"
chapters.

"""

import datetime
from typing import List, NamedTuple

from rssfly.extractor.common import Chapter


class PublishedChapter(NamedTuple):
    chapter_id: str
    name: str
    url: str
    published: datetime.datetime


def reconcile(
    existing: List[PublishedChapter], current: List[Chapter], *, now: datetime.datetime
) -> List[PublishedChapter]:
    existing_ids = set(ch.chapter_id for ch in existing)
    new_chapters = existing[:]
    for chapter in current:
        if chapter.chapter_id in existing_ids:
            # TODO: maybe update details
            continue
        # TODO: optional date from source?
        new_chapters.append(PublishedChapter(published=now, **chapter._asdict()))
    return new_chapters
