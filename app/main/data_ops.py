from . import main
from .. import data_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_, and_

from forms import LoginForm, SearchForm_Record, NewTaskRecordForm, UpdateTaskRecordForm, NewTaskCategoryForm, UpdateTaskCategoryForm, SearchForm_Categary

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from .db_class import TaskRecord, TaskCategory, TaskCategory, AppUser
from datetime import datetime

#from . import libs

@main.route('/initdb', methods=['GET','POST'])
def initdb():
    #init database and set the admin password to 'redhat'
    try:
        #ProjectTab.__table__.create(report_db.get_engine())
        #ProjectMap.__table__.create(report_db.get_engine())
        #AppUser.__table__.drop(report_db.get_engine())
        #AppUser.__table__.create(report_db.get_engine())
        data_db.create_all()
        #create super user when init database,
        super_user = AppUser()
        super_user.username = 'admin'
        password = 'redhat'
        super_user.password = generate_password_hash(password)
        super_user.email = 'xiliang@redhat.com'
        super_user.role = 'super'
        super_user.group = 'group1'
        data_db.session.add(super_user)
        data_db.session.commit()
        flash('Init db done','info')
    except Exception as err:
        flash(err,'error')
    return redirect(url_for('main.record_all'))

@main.route('/record_new', methods=['GET', 'POST'])
@login_required
def record_new():
    #add daily record data
    username = current_user.username
    per_page_default = 50
    search_form = SearchForm_Record(csrf_enabled=False)
    msg = ''
    record_data_form = NewTaskRecordForm(csrf_enabled=False,prefix="record_data_form")
    
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
            return redirect(url_for('main.record_all'))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data
            return redirect(url_for('main.record_all', select_item=select_item,search_input=search_input))
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    record = TaskRecord()
    task_categarys = TaskCategory.query.with_entities(TaskCategory.task_categary_id,TaskCategory.task_category_name)
    task_category_name_list = []
    task_categary_id_list = []
    for i in task_categarys:
        task_category_name_list.append((i.task_category_name,i.task_category_name))
        task_categary_id_list.append(i.task_categary_id)
    print(task_category_name_list)
    record_data_form.set_choices(task_category_name_list)
    

    record_data_form.username.data = username
    if record_data_form.validate_on_submit():
        record.username = username
        record.create_date = record_data_form.create_date.data
        
        task_categary = TaskCategory.query.filter_by(task_category_name=record_data_form.task_category.data).first()
        record.task_category = task_categary.task_categary_id
        print("id %s" % record.task_category)
        record.task_description = record_data_form.task_description.data
        record.task_status = record_data_form.task_status.data
        record.task_conclusion = record_data_form.task_conclusion.data
        record.task_conclusion_comments = record_data_form.task_conclusion_comments.data
        record.task_took_hours = record_data_form.task_took_hours.data
        record.task_start_date = record_data_form.task_start_date.data
        record.task_end_date = record_data_form.task_end_date.data
        data_db.session.add(record)
        data_db.session.commit()
        flash("Added successfully!",'info')
        return redirect(url_for('main.record_all'))
    record_data_form.username.data = username
    create_date = datetime.today().date()
    record_data_form.create_date.data = create_date
    record_data_form.task_description.data = ''
    record_data_form.task_status.data = ''
    record_data_form.task_conclusion.data = ''
    record_data_form.task_conclusion_comments.data = ''
    record_data_form.task_took_hours.data = ''
    record_data_form.task_start_date.data = ''
    record_data_form.task_end_date.data = ''

    return render_template('record_new.html',record_data_form=record_data_form,search_form=search_form)

@main.route('/record_update', methods=['GET', 'POST'])
@login_required
def record_update():
    #update daily record data
    username = current_user.username
    taskid = request.args.get('taskid')
    if taskid is None:
        flash('Please specify taskid to edit','info')
        return redirect(url_for('main.record_all'))
    per_page_default = 50
    search_form = SearchForm_Record(csrf_enabled=False)
    msg = ''
    record_data_form = UpdateTaskRecordForm()
    task_categarys = TaskCategory.query.with_entities(TaskCategory.task_categary_id,TaskCategory.task_category_name)
    task_category_name_list = []
    task_categary_id_list = []
    for i in task_categarys:
        task_category_name_list.append((i.task_category_name,i.task_category_name))
        task_categary_id_list.append(i.task_categary_id)
    record_data_form.set_choices(task_category_name_list)
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
            return redirect(url_for('main.record_all',project_name='test4'))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data
            return redirect(url_for('main.record_all', select_item=select_item,search_input=search_input))
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    record = TaskRecord.query.filter_by(id=taskid).first()
    if record is None:
        flash("No such task found%s"%taskid,'error')
        return redirect(url_for('main.record_all'))
    if record_data_form.validate_on_submit():
        if record_data_form.delete.data:
            data_db.session.delete(record)
            data_db.session.commit()
            flash("Item %s deleted!" % taskid)
            return redirect(url_for('main.record_all'))
            
        record.id = taskid
        record.username = username
        record.create_date = record_data_form.create_date.data
        record.task_category = record_data_form.task_category.data
        task_categary = TaskCategory.query.filter_by(task_category_name=record_data_form.task_category.data).first()
        record.task_category = task_categary.task_categary_id
        record.task_description = record_data_form.task_description.data
        record.task_status = record_data_form.task_status.data
        record.task_conclusion = record_data_form.task_conclusion.data
        record.task_conclusion_comments = record_data_form.task_conclusion_comments.data
        record.task_took_hours = record_data_form.task_took_hours.data
        record.task_start_date = record_data_form.task_start_date.data
        record.task_end_date = record_data_form.task_end_date.data
        data_db.session.add(record)
        data_db.session.commit()
        flash("Update successfully!",'info')
        return redirect(url_for('main.record_all'))

    record_data_form.id.data = record.id
    record_data_form.username.data = record.username
    record_data_form.create_date.data = record.create_date
    task_categary = TaskCategory.query.filter_by(task_categary_id=record.task_category).first()
    if task_categary is not None:
        record_data_form.task_category.data = task_categary.task_category_name
    #record_data_form.task_category.data = record.task_category
    record_data_form.task_description.data = record.task_description
    record_data_form.task_status.data = record.task_status
    record_data_form.task_conclusion.data = record.task_conclusion
    record_data_form.task_conclusion_comments.data = record.task_conclusion_comments
    record_data_form.task_took_hours.data = record.task_took_hours
    record_data_form.task_start_date.data = record.task_start_date
    record_data_form.task_end_date.data = record.task_end_date
    #return redirect(url_for('main.record_update',taskid=taskid))
    return render_template('record_update.html',record_data_form=record_data_form,search_form=search_form,taskid=taskid)


@main.route('/categary_new', methods=['GET', 'POST'])
@login_required
def categary_new():
    #create new task categary
    task_categary_form = NewTaskCategoryForm()
    search_form = SearchForm_Categary(csrf_enabled=True)
    categary = TaskCategory()
    #project.project_name=project_form.project_name.data
    if task_categary_form.validate_on_submit():
        categary.task_category_name = task_categary_form.task_category_name.data
        categary.task_category_description = task_categary_form.task_category_description.data
        categary.task_category_comments = task_categary_form.task_category_comments.data
        try:
            if TaskCategory.query.filter_by(task_category_name=categary.task_category_name).count() > 0:
                flash('Categary name already exists!','error')
                return render_template('categary_new.html',form=search_form,task_categary_form=task_categary_form)
            data_db.session.add(categary)
            data_db.session.commit()
            #ProjectTab.__tablename__='project_%s'%project_name
            #ProjectTab.set_tablename('project_%s'%project_name)
            #project.__table__.create(report_db.get_engine())
            flash("Added successfully!")
            return redirect(url_for('main.categary_all'))
        except Exception as err:
            flash(err,'error')
    return render_template('categary_new.html',search_form=search_form,task_categary_form=task_categary_form)

@main.route('/categary_update', methods=['GET', 'POST'])
@login_required
def categary_update():
    #update existing task categary
    categary_id = request.args.get('task_categary_id',None)
    if categary_id == None or categary_id == '':
        flash('No categary_id specified','warning')
        return redirect(url_for('main.categary_all'))
    task_categary_form = UpdateTaskCategoryForm()
    task_categary = TaskCategory.query.filter_by(task_categary_id=categary_id).first()
    if task_categary == None:
        flash('No categary_id found in db','warning')
        return redirect(url_for('main.categary_all'))
    search_form = SearchForm_Categary(csrf_enabled=True)
    categary = TaskCategory()
    #project.project_name=project_form.project_name.data
    if task_categary_form.validate_on_submit():
        task_categary.task_category_name = task_categary_form.task_category_name.data
        task_categary.task_category_description = task_categary_form.task_category_description.data
        task_categary.task_category_comments = task_categary_form.task_category_comments.data
        try:
            if TaskCategory.query.filter_by(task_category_name=categary.task_category_name).count() > 0:
                flash('Categary name already exists!','error')
                return render_template('categary_update.html',search_form=search_form,task_categary_form=task_categary_form)
            data_db.session.add(task_categary)
            data_db.session.commit()
            #ProjectTab.__tablename__='project_%s'%project_name
            #ProjectTab.set_tablename('project_%s'%project_name)
            #project.__table__.create(report_db.get_engine())
            flash("Updated successfully!")
            return redirect(url_for('main.categary_update',task_categary_id=categary_id))
        except Exception as err:
            flash(err,'error')
    task_categary_form.task_id.data = task_categary.task_categary_id
    task_categary_form.task_category_name.data = task_categary.task_category_name
    task_categary_form.task_category_description.data = task_categary.task_category_description
    task_categary_form.task_category_comments.data = task_categary.task_category_comments
    return render_template('categary_update.html',search_form=search_form,task_categary_form=task_categary_form,task_categary_id=categary_id)

@main.route('/categary_all', methods=['GET', 'POST'])
@login_required
def categary_all():
    #show all task categary
    search_form = SearchForm_Categary(csrf_enabled=True)
    task_categarys= TaskCategory.query.all()
    username = current_user.username
    per_page_default = 50

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
            return redirect(url_for('main.categary_all',username=username))
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
    if select_item is not None and 'task_categary_id' in select_item:
        query_obj=TaskCategory.task_categary_id
    if select_item is not None and 'task_category_name' in select_item:
        query_obj=TaskCategory.task_category_name
    if select_item is not None and 'task_category_description' in select_item:
        query_obj=TaskCategory.task_category_description
    if select_item is not None and 'task_category_comments' in select_item:
        query_obj=TaskCategory.task_category_comments

    if query_obj is not None:
        filter_item = query_obj.like("%"+search_input+"%")
        pagination = TaskCategory.query.filter(and_(filter_item)).order_by(
            TaskCategory.task_categary_id.desc()).paginate(page, per_page=int(per_page), error_out=False)
    else:
        pagination = TaskCategory.query.order_by(
            TaskCategory.task_categary_id.desc()).paginate(page, per_page=int(per_page), error_out=False)
        print(pagination.items)

    find_count = pagination.total

    page = request.args.get('page', 1, type=int)
    msg += 'Found %s items in %s pages!' % (find_count,pagination.pages)
    flash(msg, category='info')
    task_categarys = pagination.items
    if search_form.validate_on_submit():    
        return redirect(url_for('main.categary_all', select_item=select_item, search_input=search_input, username=username,per_page=per_page))
    return render_template('categary_all.html',task_categarys=task_categarys,search_form=search_form)