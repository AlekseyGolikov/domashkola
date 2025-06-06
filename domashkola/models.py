from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from domashkola import db


class User(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
  password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
  
  def __repr__(self):
    return '<User {}>'.format(self.username)
  