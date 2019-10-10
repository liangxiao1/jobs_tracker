from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):
    username = TextField('UserName', render_kw={"placeholder": "Username"}, validators=[Required()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[Required()])
    submit = SubmitField("Login")

class NewUserForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    email = TextField('Email')
    role = SelectField('Role', choices=[('admin', 'admin'),('user', 'user'),('super', 'super')])
    group = SelectField('Group', choices=[('group1', 'group1'),('group2', 'group2'),('group3', 'group3')])
    submit = SubmitField("Create")

class EditUserForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    email = TextField('Email')
    role = SelectField('Role', choices=[('admin', 'admin'),('user', 'user')])
    submit = SubmitField("Update")
    cancel = SubmitField("Cancel")

class SearchForm_v2(FlaskForm):
    search_input = TextField(
        '', render_kw={"placeholder": "Filter by what?"}, validators=[Required()])
    select_item = SelectField()
    def set_choices(self,l):
        self.select_item.choices = l
    submit = SubmitField("Go")
    reset = SubmitField("Reset")

class SearchForm_Record(FlaskForm):
    search_input = TextField(
        '', render_kw={"placeholder": "Filter by what?"}, validators=[Required()])
    select_item = SelectField('', choices=[('username', 'username'),('create_date','create_date'),('task_end_date','task_end_date'),
                            ('task_category_name', 'task_category_name'), ('task_description','task_description'),('task_start_date','task_start_date'),
                             ('task_status', 'task_status'),('task_took_hours', 'task_took_hours'),
                            ('task_result', 'task_result'), ('task_result_comments', 'task_result_comments')])
    submit = SubmitField("Go")
    reset = SubmitField("Reset")

class SearchForm_Categary(FlaskForm):
    search_input = TextField(
        '', render_kw={"placeholder": "Filter by what?"}, validators=[Required()])
    select_item = SelectField('', choices=[('task_categary_id', 'task_categary_id'),
                            ('task_category_name', 'task_category_name'),
                            ('task_category_description', 'task_category_description'),
                            ('task_category_comments', 'task_category_comments')])
    submit = SubmitField("Go")
    reset = SubmitField("Reset")

class NewTaskCategoryForm(FlaskForm):
    task_id = TextField('task_id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    task_category_name = TextField('task_category_name')
    task_category_description = TextAreaField('task_category_description')
    task_category_comments = TextAreaField('task_category_comments')

    submit = SubmitField("Add")

class UpdateTaskCategoryForm(FlaskForm):
    task_id = TextField('task_id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    task_category_name = TextField('task_category_name',render_kw={
                    })
    task_category_description = TextAreaField('task_category_description')
    task_category_comments = TextAreaField('task_category_comments')

    submit = SubmitField("Update")

class NewTaskRecordForm(FlaskForm):
    id = TextField('id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    username = TextField('username',render_kw={
                    'readonly': True})
    create_date = TextField('create_date')
    task_category = SelectField('task_category')
    def set_choices(self,l):
        self.task_category.choices = l
    task_description =  TextAreaField('task_description')
    task_status = SelectField('task_status', choices=[('cancel', 'cancel'),('completed', 'completed'),
                            ('in progress', 'in progress'),('not start', 'not start')])
    task_conclusion = TextField('task_conclusion')
    task_conclusion_comments =  TextAreaField('task_conclusion_comments')
    task_took_hours = SelectField('task_took_hours', choices=[('0', '0'),('0.1', '0.1'),('0.25', '0.25'),
                            ('0.5', '0.5'),('0.75', '0.75'),('1', '1'),('1.25', '1.25'),
                            ('1.5', '1.5'),('1.75', '1.75'),('2', '2'),('2.25', '2.25'),
                            ('2.5', '2.5'),('2.75', '2.75'),('3', '3'),('3.5', '3.5'),
                            ('4', '4'),('4.5', '4.5'),('5', '5'),('6', '6'),
                            ('7', '7'),('8', '8'),('9', '9'),('10', '10')])
    task_start_date = TextField('task_start_date')
    task_end_date = TextField('task_end_date',render_kw={'class':'btn btn-primary btn-lg'})

    submit = SubmitField("Add")

class UpdateTaskRecordForm(FlaskForm):
    id = TextField('id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    username = TextField('username',render_kw={
                    'readonly': True})
    create_date = TextField('create_date',render_kw={
                    'readonly': True})
    task_category = SelectField('task_category')
    def set_choices(self,l):
        self.task_category.choices = l
    task_description =  TextAreaField('task_description')
    task_status = SelectField('task_status', choices=[('cancel', 'cancel'),('completed', 'completed'),
                            ('in progress', 'in progress'),('not start', 'not start')])
    task_conclusion = TextField('task_conclusion')
    task_conclusion_comments =  TextAreaField('task_conclusion_comments')
    task_took_hours = SelectField('task_took_hours', choices=[('0', '0'),('0.1', '0.1'),('0.25', '0.25'),
                            ('0.5', '0.5'),('0.75', '0.75'),('1', '1'),('1.25', '1.25'),
                            ('1.5', '1.5'),('1.75', '1.75'),('2', '2'),('2.25', '2.25'),
                            ('2.5', '2.5'),('2.75', '2.75'),('3', '3'),('3.5', '3.5'),
                            ('4', '4'),('4.5', '4.5'),('5', '5'),('6', '6'),
                            ('7', '7'),('8', '8'),('9', '9'),('10', '10')])
    task_start_date = TextField('task_start_date')
    task_end_date = TextField('task_end_date')

    submit = SubmitField("Update")
    delete = SubmitField("Delete")