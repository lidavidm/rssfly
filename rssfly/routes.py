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

import datetime

import requests
from flask import make_response, render_template

import rssfly.model as model
from rssfly.app import app
from rssfly.extractor import acqq, tappytoon
from rssfly.extractor.common import Comic, Context
from rssfly.reconcile import reconcile


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/acqq/<comic_id>")
def extract_acqq(comic_id):
    extractor = acqq.AcqqExtractor()
    existing = []
    existing_comic = model.load_comic(publisher=extractor.publisher, comic_id=comic_id)
    if existing_comic:
        existing = existing_comic.chapters
    with requests.Session() as session:
        context = Context(session)
        comic = extractor.extract(context, comic_id)
        reconciled = reconcile(existing, comic.chapters, now=datetime.datetime.now())
        comic = Comic(
            publisher=comic.publisher,
            comic_id=comic.comic_id,
            name=comic.name,
            url=comic.url,
            chapters=reconciled,
        )
        model.save_comic(comic)
    response = make_response(
        render_template(
            "feed.xml",
            comic=comic,
            latest=max(comic.chapters, key=lambda chapter: chapter.published),
        )
    )
    response.headers["Content-Type"] = "application/atom+xml"
    return response


@app.route("/tappytoon/<comic_id>")
def extract_tappytoon(comic_id):
    extractor = tappytoon.TappytoonExtractor()
    existing = []
    existing_comic = model.load_comic(publisher=extractor.publisher, comic_id=comic_id)
    if existing_comic:
        existing = existing_comic.chapters
    with requests.Session() as session:
        context = Context(session)
        comic = extractor.extract(context, comic_id)
        reconciled = reconcile(existing, comic.chapters, now=datetime.datetime.now())
        comic = Comic(
            publisher=comic.publisher,
            comic_id=comic.comic_id,
            name=comic.name,
            url=comic.url,
            chapters=reconciled,
        )
        model.save_comic(comic)
    response = make_response(
        render_template(
            "feed.xml",
            comic=comic,
            latest=max(comic.chapters, key=lambda chapter: chapter.published),
        )
    )
    response.headers["Content-Type"] = "application/atom+xml"
    return response
