from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, IPAddress
from flask_login import current_user


class RegistrationForm(FlaskForm):
    user_name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    user_name = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CreateFlowForm(FlaskForm):
    name = StringField('Flow Name',
                        validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('Flow Description', validators=[DataRequired()])
    source_flow = SelectField('Select Source Flow', validate_choice=False)  # could be accessed through ID or Name
    destination_address = StringField('Flow Destination Address (IPv4 Address)',
                        validators=[DataRequired(), Length(min=7, max=15), IPAddress()], render_kw={"placeholder":"10.10.10.10"})
    destination_port = StringField('Flow Destination Port',
                        validators=[DataRequired(), Length(min=1, max=5)], render_kw={"placeholder":"1-65535"})
    selected_traffic = SelectMultipleField('Select Traffic(s) to Forward', choices=['tcp', 'udp', 'icmp' ,'Any'])
    payload_obfuscation =  SelectMultipleField('Select Payload Obfuscation(s)', choices=['Mask', 'Slice', 'None'])
    submit = SubmitField('Create Flow')

class CreateOfferedFlowForm(FlaskForm):
    name = StringField('Flow Name', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder":"Enter unique flow name"})
    description = TextAreaField('Flow Description', validators=[DataRequired()])
    source_command = StringField('Source executable',
                        validators=[DataRequired(), Length(min=7, max=85)], render_kw={"placeholder":"/bin/ps -a"})
    source_address = StringField('Flow Source Address (IPv4 Address)',
                        validators=[DataRequired(), Length(min=7, max=15), IPAddress()], render_kw={"placeholder":"10.10.10.10"})
    source_intfc = StringField('Flow Source Interface', validators=[DataRequired(), Length(min=3, max=12)], render_kw={"placeholder": "eth3"})

    nat_address = StringField('NAT Address (IPv4 Address)',
                                 validators=[DataRequired(), Length(min=7, max=15), IPAddress()],
                                 render_kw={"placeholder": "10.43.200.10"})
    nat_port = StringField('NAT Port', validators=[DataRequired(), Length(min=1, max=5)], render_kw={"placeholder":"1-65535"})
    port_type = SelectMultipleField('Select Port Type(s)', choices=['tcp', 'udp'])
    filters = StringField('Specify Filters',
                        validators=[DataRequired(), Length(min=2, max=60)])
    speed = IntegerField('Flow Speed (Gbps)', validators=[DataRequired()])
    replication= SelectField('Select Replication Method', choices=['Tapped', 'Application']) # could be accessed through ID or Name
    submit = SubmitField('Create Flow Offering')

class SelectFlowForm(FlaskForm):
    flow_selection = SelectField('Select Flow to Modify', validate_choice=False) # could be accessed through ID or Name
    submit = SubmitField('Select Flow')

class RestartFlowForm(FlaskForm):
        flow_selection = SelectField('Select Flow to Restart',
                                     validate_choice=False)  # could be accessed through ID or Name
        submit = SubmitField('Restart Flow Application')

class ModifyFlowForm(FlaskForm):
    status = SelectField('Modify Flow Status', choices=['Active', 'Paused'])
    description = TextAreaField('Flow Description', validators=[DataRequired()])
    destination_address = StringField('Flow Destination Address (IPv4 Address)',
                        validators=[DataRequired(), Length(min=7, max=15)], render_kw={"placeholder":"8.10.18.10"})
    destination_port = StringField('Flow Destination Port',
                        validators=[DataRequired(), Length(min=1, max=5)], render_kw={"placeholder":"1-65535"})
    selected_traffic = SelectMultipleField('Select Traffic(s) to Forward', choices=['tcp', 'udp', 'icmp' ,'Any'])
    payload_obfuscation =  SelectMultipleField('Select Payload Obfuscation(s)', choices=['Mask', 'Slice', 'None'])
    submit = SubmitField('Submit Flow Modifications', default=False)

class ModifyOfferedFlowForm(FlaskForm):
    description = TextAreaField('Flow Description', validators=[DataRequired()])
    source_command = StringField('Source executable',
                        validators=[DataRequired(), Length(min=7, max=85)], render_kw={"placeholder":"/bin/ps -a"})
    source_address = StringField('Flow Source Address (IPv4 Address)',
                        validators=[DataRequired(), Length(min=7, max=15)], render_kw={"placeholder":"10.10.10.10"})
    nat_address = StringField('NAT Address (IPv4 Address)',
                                 validators=[DataRequired(), Length(min=7, max=15), IPAddress()],
                                 render_kw={"placeholder": "10.43.200.10"})
    nat_port = StringField('NAT Port', validators=[DataRequired(), Length(min=1, max=5)], render_kw={"placeholder": "1-65535"})
    port_type = SelectMultipleField('Select Port Type(s)', choices=['tcp', 'udp'])
    speed = IntegerField('Flow Speed (Gbps)', validators=[DataRequired()])
    filters = StringField('Specify Filters',
                        validators=[DataRequired(), Length(min=2, max=60)])
    replication= SelectField('Select Replication Method', choices=['Tapped', 'Application']) # could be accessed through ID or Name
    submit = SubmitField('Submit Flow Modifications', default=False)

class DeleteFlowForm(FlaskForm):
    flows = SelectField('Select ID of Flow to Delete') # could be accessed through ID or Name
    submit = SubmitField('Delete Flow')
