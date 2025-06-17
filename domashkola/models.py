from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from domashkola import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))


class Users(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    grant_status: so.Mapped[int] = so.mapped_column(sa.SmallInteger, nullable=True)    # статус пользователя
  
    def __repr__(self):
        return '<User {} id: {}; email: {}; grant_status: {}>'.format(self.username, self.id, self.email, self.grant_status)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Categories(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    category_name: so.Mapped[str] = so.mapped_column(sa.String(60), index=True, unique=True)
    posts: so.WriteOnlyMapped['Posts'] = so.relationship(back_populates='category')
  
    def __repr__(self):
        return '<Category {}. {}>\n'.format(self.id, self.category_name)
  

class Posts(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    link: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    url: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    header: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    attached_files: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now())
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Categories.id), index=True)
    category_name: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    keywords: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    restrict_status: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)    # статус ограничения на просмотр поста
    priority_status: so.Mapped[int] = so.mapped_column(sa.SmallInteger, nullable=True)    # приоритет сообщения


    category: so.Mapped[Categories] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}. {} от {}. Приложенные файлы: {}. Категория: {}. Статус ограничения: {}. Приоритет: {}>\n'.format(self.id, 
                                                                                                                           self.body[:30]+'...', 
                                                                                                                           self.timestamp, 
                                                                                                                           self.attached_files, 
                                                                                                                           self.category_id, 
                                                                                                                           self.restrict_status, 
                                                                                                                           self.priority_status)
