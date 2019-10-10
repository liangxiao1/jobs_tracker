from . import main
from .. import login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from forms import LoginForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2
import logging

from .db_class import TaskCategory

log=logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def init_category_droplist():
    '''
    Return a list for category drop list set
    '''
    drop_list = []
    categories=TaskCategory.query.all()
    if len(categories) == 0 or categories == None:
        log.error('No category found')
    for category in categories:
        drop_list.append(category.task_category_name)
    log.debug('Get categories: %s' % drop_list)
    return drop_list