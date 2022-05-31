"""Initial migration.

Revision ID: 38164ae2b1ae
Revises: 
Create Date: 2022-05-31 09:52:43.177268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38164ae2b1ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    op.drop_table('reviews')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('movie', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['movie'], ['movies.id'], name='reviews_movie_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='reviews_pkey')
    )
    op.create_table('movies',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('year', sa.VARCHAR(length=4), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('language', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('director', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('actors', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('poster_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('writer', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='movies_pkey'),
    sa.UniqueConstraint('title', name='movies_title_key')
    )
    # ### end Alembic commands ###
