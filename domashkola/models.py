from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from domashkola import db
from datetime import datetime


class Users(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
  password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
  
  def __repr__(self):
    return '<User {}>'.format(self.username)


class Categories(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  category_name: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
  posts: so.WriteOnlyMapped['Posts'] = so.relationship(back_populates='author')
  
  def __repr__(self):
    return '<Category {}>'.format(self.category_name)
  

class Posts(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    link: so.Mapped[str] = so.mapped_column(sa.String(60))
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    attached_files: so.Mapped[str] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Users.id), index=True)

    author: so.Mapped[Users] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
