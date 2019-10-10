from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_
from flask_login import UserMixin

from .. import data_db

class TaskCategory(data_db.Model):
    __tablename__ = 'task_category'
    task_categary_id = Column(Integer, primary_key=True)
    task_category_name = Column(String)
    task_category_description = Column(String)
    task_category_comments = Column(String)
    sqlite_autoincrement = True

class TaskRecord(data_db.Model):
    __tablename__ = 'task_record'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    create_date = Column(String)
    task_category = Column(String)
    task_description = Column(String)
    task_status = Column(String)
    task_conclusion = Column(String)
    task_conclusion_comments = Column(String)
    task_took_hours = Column(String)
    task_start_date = Column(String)
    task_end_date = Column(String)
    sqlite_autoincrement = True

class AppUser(UserMixin, data_db.Model):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    group = Column(String)
    @property
    def is_admin(self):
        if 'admin' in self.role:
            return True
        elif 'super' in self.role:
            return True
        else:
            return False
    @property
    def is_super(self):
        if 'super' in self.role:
            return True
        else:
            return False 
    sqlite_autoincrement = True
