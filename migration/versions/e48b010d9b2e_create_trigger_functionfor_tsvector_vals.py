"""Create trigger functionfor tsvector vals

Revision ID: e48b010d9b2e
Revises: b3f2ecef7d45
Create Date: 2023-12-04 00:19:45.047740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e48b010d9b2e'
down_revision: Union[str, None] = 'b3f2ecef7d45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE FUNCTION tsvector_update() RETURNS trigger AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                NEW.tsvector_column = 
                    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                    setweight(to_tsvector('english', 
                        COALESCE((SELECT array_to_string(array_agg(tags.tag), ' ') 
                                  FROM blog_tags
                                  LEFT JOIN tags ON blog_tags.tag_id = tags.id
                                  WHERE blog_tags.blog_id = NEW.id), '')), 'B') ||
                    setweight(to_tsvector('english', COALESCE(NEW.blog_text, '')), 'D') ||
                    setweight(to_tsvector('english', COALESCE((SELECT users.username 
                                                                FROM users 
                                                                WHERE users.id = NEW.author_id), '')), 'B');
            END IF;

            IF TG_OP = 'UPDATE' THEN
                NEW.tsvector_column = 
                    setweight(to_tsvector('english', COALESCE(NEW.title, OLD.title, '')), 'A') ||
                    setweight(to_tsvector('english', 
                        COALESCE((SELECT array_to_string(array_agg(tags.tag), ' ') 
                                  FROM blog_tags
                                  LEFT JOIN tags ON blog_tags.tag_id = tags.id
                                  WHERE blog_tags.blog_id = NEW.id), '')), 'B') ||
                    setweight(to_tsvector('english', COALESCE(NEW.blog_text, OLD.blog_text, '')), 'D') ||
                    setweight(to_tsvector('english', COALESCE((SELECT users.username 
                                                                FROM users 
                                                                WHERE users.id = NEW.author_id), '')), 'B');
            END IF;

            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
        ON blogs FOR EACH ROW 
        EXECUTE PROCEDURE tsvector_update();
    """)


def downgrade() -> None:
    op.execute('DROP TRIGGER tsvector_update ON blogs')
    op.execute('DROP FUNCTION tsvector_update()')
