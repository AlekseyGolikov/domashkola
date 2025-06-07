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
  posts: so.WriteOnlyMapped['Posts'] = so.relationship(back_populates='category')
  
  def __repr__(self):
    return '<Category {}. {}>\n'.format(self.id, self.category_name)
  

class Posts(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    link: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    attached_files: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now())
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Categories.id), index=True)

    category: so.Mapped[Categories] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}. {} от {}>\n'.format(self.id, self.body, self.timestamp)
