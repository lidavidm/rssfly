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

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

from rssfly.app import app
from rssfly.extractor.common import Comic
from rssfly.reconcile import PublishedChapter

db = SQLAlchemy(app)

comic = sa.Table(
    "comic",
    db.metadata,
    sa.Column("publisher", sa.String(), primary_key=True),
    sa.Column("comic_id", sa.String(), primary_key=True),
    sa.Column("name", sa.String(), nullable=False),
    sa.Column("url", sa.String(), nullable=False),
)
chapter = sa.Table(
    "chapter",
    db.metadata,
    sa.Column("publisher", sa.String(), primary_key=True),
    sa.Column("comic_id", sa.String(), primary_key=True),
    sa.Column("chapter_id", sa.String(), nullable=False),
    sa.Column("name", sa.String(), nullable=False),
    sa.Column("url", sa.String(), nullable=False),
    sa.Column("published", sa.DateTime(), nullable=False),
)


def load_comic(publisher, comic_id):
    query = (
        sa.select([comic])
        .where(comic.c.publisher == publisher)
        .where(comic.c.comic_id == comic_id)
    )
    info = db.session.execute(query).fetchone()
    if not info:
        return None
    query = (
        sa.select([chapter])
        .where(chapter.c.publisher == publisher)
        .where(chapter.c.comic_id == comic_id)
    )
    chapters = [
        PublishedChapter(
            chapter_id=row["chapter_id"],
            name=row["name"],
            url=row["url"],
            published=row["published"],
        )
        for row in db.session.execute(query).fetchall()
    ]
    chapters.sort(key=lambda chapter: (chapter.published, chapter.chapter_id))
    return Comic(
        publisher=info["publisher"],
        comic_id=info["comic_id"],
        name=info["name"],
        url=info["url"],
        chapters=chapters,
    )


_save_comic_query = """
INSERT INTO comic(publisher, comic_id, name, url)
VALUES (:publisher, :comic_id, :name, :url)
ON CONFLICT (publisher, comic_id) DO UPDATE SET name = :name, url = :url
"""
_save_chapter_query = """
INSERT INTO chapter(publisher, comic_id, chapter_id, name, url, published)
VALUES (:publisher, :comic_id, :chapter_id, :name, :url, :published)
ON CONFLICT (publisher, comic_id, chapter_id) DO UPDATE SET name = :name, url = :url, published = :published
"""


def save_comic(comic_info):
    query = sa.sql.text(_save_comic_query).bindparams(
        publisher=comic_info.publisher,
        comic_id=comic_info.comic_id,
        name=comic_info.name,
        url=comic_info.url,
    )
    db.session.execute(query)
    query = sa.sql.text(_save_chapter_query)
    db.session.execute(
        query,
        [
            dict(
                publisher=comic_info.publisher,
                comic_id=comic_info.comic_id,
                chapter_id=chapter.chapter_id,
                name=chapter.name,
                url=chapter.url,
                published=chapter.published,
            )
            for chapter in comic_info.chapters
        ],
    )
    db.session.commit()
