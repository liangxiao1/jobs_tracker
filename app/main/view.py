from . import main
from .. import login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_,and_
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from forms import LoginForm,SearchForm_Record

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2

from .db_class import TaskRecord,TaskCategory
from . import libs
import copy

@main.route('/record_all', methods=['GET', 'POST'])
@login_required
def record_all():

    table_titles = ['id','username','create_date','task_category','task_description','task_status',\
        'task_conclusion','task_conclusion_comments','task_took_hours','task_start_date','task_end_date']
    records = TaskRecord.query.all()
    #username = request.args.get('username')
    username = current_user.username
    per_page_default = 50
    search_form =SearchForm_Record(csrf_enabled=True)
    per_page = request.args.get('per_page')
    if per_page is None and not session.has_key('per_page'):
        per_page = per_page_default
        session['per_page'] = per_page
    elif per_page is None and session.has_key('per_page'):
        per_page = session['per_page']
    elif per_page is not None:
        session['per_page'] = per_page

    msg = ''
    #pagination = libs.search_db(search_form=search_form,project_name=project_name,submit=search_form.validate_on_submit(),reset=search_form.reset.data)
    find_count = 0
    page = request.args.get('page', 1, type=int)
    query_obj = None
    if search_form.validate_on_submit():
        print('item select %s, search input %s'% (search_form.select_item.data,search_form.search_input.data))
        if search_form.reset.data:
            msg += "Clear all filters!"
            flash(msg,'info')
            # session.clear()
            session.pop('search_input', None)
            session.pop('select_item', None)
            query_obj = None
            search_form.select_item.data = None
            return redirect(url_for('main.record_all',username=username))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data 
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    
    if select_item is None and session.has_key("select_item"):
        select_item = session['select_item']
        search_input = session['search_input']
        search_form.search_input.data = search_input
        search_form.select_item.data = select_item
    elif select_item is not None:
        session['select_item'] = select_item
        session['search_input'] = search_input
        search_form.search_input.data = search_input
        search_form.select_item.data = select_item
    if select_item is not None and 'id' in select_item:
        query_obj=TaskRecord.id
    if select_item is not None and 'username' in select_item:
        query_obj=TaskRecord.username
    if select_item is not None and 'create_date' in select_item:
        query_obj=TaskRecord.create_date
    if select_item is not None and 'task_end_date' in select_item:
        query_obj=TaskRecord.task_end_date
    if select_item is not None and 'task_category_name' in select_item:
        query_obj=TaskRecord.task_category_name
    if select_item is not None and 'task_description' in select_item:
        query_obj=TaskRecord.task_description
    if select_item is not None and 'task_start_date' in select_item:
        query_obj=TaskRecord.task_start_date
    if select_item is not None and 'task_status' in select_item:
        query_obj=TaskRecord.task_status
    if select_item is not None and 'task_took_hours' in select_item:
        query_obj=TaskRecord.task_took_hours
    if select_item is not None and 'task_result' in select_item:
        query_obj=TaskRecord.task_result
    if select_item is not None and 'task_result_comments' in select_item:
        query_obj=TaskRecord.task_result_comments


    if query_obj is not None:
        filter_item = query_obj.like("%"+search_input+"%")
        pagination = TaskRecord.query.filter(and_(filter_item,TaskRecord.username==username)).order_by(
            TaskRecord.id.desc()).paginate(page, per_page=int(per_page), error_out=False)
    else:
        pagination = TaskRecord.query.order_by(
            TaskRecord.id.desc()).paginate(page, per_page=int(per_page), error_out=False)
        print(pagination.items)

    find_count = pagination.total

    page = request.args.get('page', 1, type=int)
    msg += 'Found %s items in %s pages!' % (find_count,pagination.pages)
    flash(msg, category='info')
    records = pagination.items
    records_put = copy.deepcopy(records)
    for record in records_put:
        task_categary = TaskCategory.query.filter_by(task_categary_id=record.task_category).first()
        if task_categary is not None:
            record.task_category = task_categary.task_category_name

    if search_form.validate_on_submit():    
        return redirect(url_for('main.record_all', select_item=select_item, search_input=search_input, username=username,per_page=per_page))
    return render_template('record_all.html', per_page=session['per_page'], search_form=search_form, records=records_put,table_titles=table_titles, pagination=pagination, select_item=select_item, search_input=search_input,username=username)