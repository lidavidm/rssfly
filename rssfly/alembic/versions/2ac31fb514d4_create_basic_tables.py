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

"""create basic tables

Revision ID: 2ac31fb514d4
Revises:
Create Date: 2021-01-10 13:37:54.642395

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2ac31fb514d4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "comic",
        sa.Column("publisher", sa.String(), primary_key=True),
        sa.Column("comic_id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
    )
    op.create_table(
        "chapter",
        sa.Column(
            "publisher", sa.String(), sa.ForeignKey("comic.publisher"), primary_key=True
        ),
        sa.Column(
            "comic_id", sa.String(), sa.ForeignKey("comic.comic_id"), primary_key=True
        ),
        sa.Column("chapter_id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("published", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("comic")
    op.drop_table("chapter")
