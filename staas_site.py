from datetime import datetime
from email.policy import default
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, exc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from forms import RegistrationForm, LoginForm, CreateFlowForm, DeleteFlowForm, UpdateAccountForm, CreateOfferedFlowForm, \
    ModifyFlowForm, SelectFlowForm, ModifyOfferedFlowForm, RestartFlowForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
import os, subprocess
import site_info

# Flask preliminaries
app = Flask(__name__)
app.config['SECRET_KEY'] = '9057920c6e99bb09161efe982f7ba326' # Site specific configuration - Admin to set secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staas.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# map flask form command line arguments into subprocess.run args
def split_opts(my_cmd):
    new = my_cmd[0].split()
    my_cmd.remove(my_cmd[0])
    my_cmd = new + my_cmd 
    return(my_cmd)

# experimenter flow to inherit parameters from offered flow
def inherit_offered_flow_params(flow):
    offered = flow.source_flow
    print("offered flow is (should match selected flow) ", offered)
    try:
        flow.source_command = Flow.query.filter_by(is_offered=True, name=offered).first().source_command
        flow.source_address = Flow.query.filter_by(is_offered=True, name=offered).first().source_address
        flow.source_intfc = Flow.query.filter_by(is_offered=True, name=offered).first().source_intfc
        flow.nat_address = Flow.query.filter_by(is_offered=True, name=offered).first().nat_address
        flow.nat_port = Flow.query.filter_by(is_offered=True, name=offered).first().nat_port
        flow.port_type = Flow.query.filter_by(is_offered=True, name=offered).first().port_type
        print("source_command=" + flow.source_command, "source_address=" + flow.source_address,", source_intfc=" + flow.source_intfc,","
              "nat_address =" + flow.nat_address,", nat_port =" + flow.nat_port,", port_type = " + flow.port_type)

    except Exception:
        print("Couldn't inherit selected offered flow parameters")


# experimenter's and administrator's registration info
class User(db.Model,  UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    flows = db.relationship('Flow', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
 

class Flow(db.Model):
    # experimenter's flow parameters that supplement those from offered flows
    name = db.Column(db.String(100), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    is_offered = db.Column(db.Boolean, nullable=False, default=False) #indicates flow offered by admin
    status = db.Column(db.Boolean, nullable = False, default=True) # flow transmission state active or paused
    destination_address = db.Column(db.Text, nullable=False, default='99.121.32.104')
    destination_port = db.Column(db.Text, nullable=False, default='18000')
    source_flow = db.Column(db.Text, nullable=False, default='Flow78') # offered flow selected by user
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user that created flow
    selected_traffic = db.Column(db.Text, nullable=False, default='TCP')
    payload_obfuscation =  db.Column(db.Text, nullable=False, default='SLICE')

    # offered flow metadata parameters specified by admin
    source_command = db.Column(db.Text, nullable=False, default='ps -a')
    source_address= db.Column(db.Text, nullable=False, default='172.17.0.200')
    source_intfc = db.Column(db.Text, nullable=False, default='eno2')
    nat_address = db.Column(db.Text, nullable=False, default='10.43.200.10')
    nat_port =  db.Column(db.Text, nullable=False, default='16010')
    port_type = db.Column(db.Text, nullable=False, default='TCP')  # NAT port is TCP or UDP (pick one)
    speed = db.Column(db.Integer, nullable=False, default=25) # actual or max source speed (Gbs)
    replication = db.Column(db.Text, nullable=False, default='Tapped') # source data mirrored or app generated
    filters = db.Column(db.Text, nullable=False, default='None') # additional source restrictions set by ddmin

    def __repr__(self):
        return f"Flow('{self.id}', '{self.name}', '{self.start_time}')"


@app.before_first_request
def recreate_tables():
    #db.drop_all()   uncomment only to delete existing database upon re-starting staas_site.py - not recommended
    db.create_all()
    print("The root_path of this flask app is", app.root_path)
    subprocess.call([app.root_path + "/console-announcements.py"]) # Site specific configuration (optional) - modify local console messages

@app.route("/")
@app.route("/home")
def home():
    flows = Flow.query.filter_by(is_offered=True).all()
    return render_template('home.html', flows=flows, title='Offered Flows')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/monitor")
@login_required
def monitor():
    # my_cmd = ['ps', '-a'] prepares command for subprocess.run()
    my_cmd = [app.root_path + '/app/bin/display-nat-connections']  # show active nat connections
    try:
        with open(site_info.tmpfile, "w") as outfile:
            cp1 = subprocess.run(my_cmd, text=True, stdout=outfile, stderr=subprocess.PIPE)
        lines = open(site_info.tmpfile, "r").readlines()
        lines = [line for line in lines]
    except FileNotFoundError as e:
        print(e)

    my_cmd = [app.root_path + '/app/bin/display-nft']   #show mangler nat tables, chains, rules
    try:
        with open(site_info.tmpfile, "w") as outfile:
            cp1 = subprocess.run(my_cmd, text=True, stdout=outfile, stderr=subprocess.PIPE)
        nftlines = open(site_info.tmpfile, "r").readlines()
        nftlineslines = [nftline for nftline in nftlines]
    except FileNotFoundError as e:
        print(e)

    return render_template('monitor.html', lines=lines, nftlines=nftlines, title='Monitor')


@app.route("/user/flows")
def user_flows():
    flows = Flow.query.filter_by(user_id=current_user.id).all()
    return render_template('user_flows.html', title='User Flows', flows=flows)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(id=hashString(form.user_name.data), name=form.user_name.data, email=form.email.data, password=hashed_password)
        if '@princeton.edu' in form.email.data:
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.user_name.data = current_user.name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/flow/<int:flow_id>")
def flow(flow_id):
    flow = Flow.query.get_or_404(flow_id)
    return render_template('flow.html', title=flow.name, flow=flow)


@app.route("/flow/new", methods=['GET', 'POST'])
@login_required
def new_flow():
    if current_user.is_admin:    # Create a new Offered flow
        form = CreateOfferedFlowForm()
        print("A1: Create Offered Flow Form presented")
        if form.validate_on_submit():
            print("A2: Create Offered Flow Form submitted")
            flow = Flow(name = form.name.data,
                        id = hashString(form.name.data),
                        description = form.description.data,
                        source_command = form.source_command.data,
                        source_address = form.source_address.data,
                        source_intfc = form.source_intfc.data,
                        nat_address = form.nat_address.data,
                        nat_port = form.nat_port.data,
                        port_type = ','.join(form.port_type.data),
                        speed = form.speed.data,
                        replication = form.replication.data,
                        filters = form.filters.data,
                        is_offered= True,
                        user = current_user)
            # admin creating offered flow merely creates offered flow template in database - not an active flow
            try:
                db.session.add(flow)
                db.session.commit()
                flash('Your flow has been created', 'success')
            except IntegrityError as e:   # or except SQLAlchemyError:
                db.session.rollback()
                print(repr(e))
                print("Database integrity error when committing requested flow")
                msg = "Your flow was not created:" + repr(e)
                flash(msg, 'fail')

            return redirect(url_for('user_flows'))

    else:	    		# Create experimenter running flow instance
        form = CreateFlowForm()
        form.source_flow.choices = [f.name for f in Flow.query.filter_by(is_offered=True).all()] # Show Princeton-Offered Flows ONLY
        print("U1: Create Flow Form presented with available offered flows")
        if form.validate_on_submit():
            print("U2: Create Flow Form submitted")
            flow = Flow(name = form.name.data,
                        id = hashString(form.name.data),
                        description = form.description.data,
                        destination_address = form.destination_address.data,
                        destination_port = form.destination_port.data,
                        source_flow = form.source_flow.data,
                        selected_traffic =  ','.join(form.selected_traffic.data),
                        payload_obfuscation =   ','.join(form.payload_obfuscation.data),
                        user = current_user)

            # get details for user flow from selected offered flow
            # flows = Flow.query.filter_by(source_flow = offered).all
            inherit_offered_flow_params(flow)
            print("U3: all flow parameters imported")
            my_cmd = [app.root_path + '/app/bin/create-flow', flow.source_command, flow.nat_address, flow.nat_port, flow.source_address, flow.source_intfc,
            flow.port_type, flow.destination_address, flow.destination_port]
            my_cmd = split_opts(my_cmd)  # split source_command with multiple args for subprocess.run execution
            print("Running this command ...")
            print(my_cmd)
            with open(site_info.logfile, "w+") as outfile:
                print("U4: Can't open logfile")
                try:
                    cp1 = subprocess.Popen(my_cmd, text=True, stdout=outfile, stderr=subprocess.PIPE, close_fds=True)
                    print("U5: Subprocess started to initiate flow")
                except Exception as e:
                    print("U6: Subprocess.Popen failed to run flow command")
                    print(e)

            try:
                db.session.add(flow)
                db.session.commit()
                flash('Your flow has been created', 'success')
            except IntegrityError as e:   # or except SQLAlchemyError:
                db.session.rollback()
                print(repr(e))
                print("Database integrity error when committing requested flow")
                msg = "Your flow was not created:" + repr(e)
                flash(msg, 'fail')

            return redirect(url_for('user_flows'))
    return render_template('create_flow.html', title='New Flow', form=form, legend='New Flow')

@app.route("/flow/restart", methods=['GET', 'POST'])
@login_required
def restart_flow():
    first_form = RestartFlowForm()
    first_form.flow_selection.choices = [(f.id, f.name) for f in Flow.query.filter_by(user_id=current_user.id).all()] # Show User's Created Flows ONLY

    if first_form.validate_on_submit():
        flow = Flow.query.get_or_404(first_form.flow_selection.data)
        if flow.user_id != current_user.id:
            abort(403)
        print("source_command=" + flow.source_command, "source_address=" + flow.source_address,
              ", source_intfc=" + flow.source_intfc, ","
                                                     "nat_address =" + flow.nat_address, ", nat_port =" + flow.nat_port,
              ", port_type = " + flow.port_type)
        my_cmd = [app.root_path + '/app/bin/restart-flow', flow.source_command, flow.nat_address,
                  flow.nat_port, flow.source_address, flow.source_intfc,
                  flow.port_type, flow.destination_address, flow.destination_port]
        my_cmd = split_opts(my_cmd)  # split source_command with multiple args for subprocess.run execution
        print("Running this command ...")
        print(my_cmd)
        with open(site_info.logfile, "w+") as outfile:
            print("U4: Can't open logfile")
            try:
                cp1 = subprocess.Popen(my_cmd, text=True, stdout=outfile, stderr=subprocess.PIPE, close_fds=True)
                print("U5: Subprocess started to initiate flow")
            except Exception as e:
                print("U6: Subprocess.Popen failed to run flow command")
                print(e)
        #end command invocation
        return redirect(url_for('user_flows'))
    return render_template('restart_flow.html', title='Restart Flow',
                            form=first_form, legend='Restart Flow')

@app.route("/flow/modify", methods=['GET', 'POST'])
@login_required
def modify_flow():
    first_form = SelectFlowForm()
    first_form.flow_selection.choices = [(f.id, f.name) for f in Flow.query.filter_by(user_id=current_user.id).all()] # show experimenter's created flows only

    if first_form.validate_on_submit():
        flow = Flow.query.get_or_404(first_form.flow_selection.data)
        if flow.user_id != current_user.id:
            abort(403)
        return redirect(url_for('modify_flow_form', flow_id=flow.id))
    return render_template('modify_flow.html', title='Modify Flow', 
                            form=first_form, legend='Modify Flow')


@app.route("/flow/modify/<int:flow_id>", methods=['GET', 'POST'])
@login_required
def modify_flow_form(flow_id):
    flow = Flow.query.get_or_404(flow_id)
    if current_user.is_admin:
        form = ModifyOfferedFlowForm()
        if form.validate_on_submit():
            flow.description = form.description.data
            flow.source_address = form.source_address.data
            flow.speed = form.speed.data
            flow.replication = form.replication.data
            flow.filters = form.filters.data
            db.session.commit()
            flash('Your flow information has been updated', 'success')
            return redirect(url_for('user_flows'))
        elif request.method == 'GET':
            form.description.data = flow.description
            form.source_address.data = flow.source_address
            form.speed.data = flow.speed
            form.replication.data = flow.replication
            form.filters.data = flow.filters
    else:
        form = ModifyFlowForm()
        if form.validate_on_submit():
            flow.description = form.description.data
            flow.destination_address = form.destination_address.data
            flow.destination_port = form.destination_port.data
            flow.selected_traffic =  ','.join(form.selected_traffic.data)
            flow.payload_obfuscation =   ','.join(form.payload_obfuscation.data)
            if form.status.data == 'Active':
                prev_status = flow.status
                flow.status = True
                if not prev_status:
                    flow.start_time = datetime.utcnow
            else:
                flow.status = False
            db.session.commit()
            flash('Your flow information has been updated', 'success')
            return redirect(url_for('user_flows'))
        elif request.method == 'GET':
            form.description.data = flow.description
            form.destination_address.data = flow.destination_address
            form.destination_port.data = flow.destination_port

            form.selected_traffic.data = flow.selected_traffic.split(',')
            form.payload_obfuscation.data = flow.payload_obfuscation.split(',')
            if flow.status:
                form.status.data = 'Active'
            else:
                form.status.data = 'Paused'
    return render_template('mod_flow_form.html', title='Modify Flow',
                           form=form, legend= f'Modify Flow: { flow.name }')


@app.route("/flows/delete", methods=['GET', 'POST'])
@login_required
def delete_flow():
    form = DeleteFlowForm()
    form.flows.choices = [f.id for f in Flow.query.filter_by(user_id=current_user.id).all()] # Show User's Created Flows ONLY

    if form.validate_on_submit():
        flow = Flow.query.get_or_404(form.flows.data)
        if flow.user_id != current_user.id:
            abort(403)
        # teardown active flow and cleanup
        my_cmd = [app.root_path + '/app/bin/destroy-flow', flow.source_command, flow.nat_address,
                  flow.nat_port, flow.source_address, flow.source_intfc,
                  flow.port_type, flow.destination_address, flow.destination_port]
        print(my_cmd)
        my_cmd = split_opts(my_cmd)  # split source_command with multiple args for subprocess.run execution
        print(my_cmd)
        print("error3")
        with open(site_info.logfile, "w+") as outfile:
            cp1 = subprocess.run(my_cmd, text=True, stdout=outfile, stderr=subprocess.PIPE)
            print("error4")
        # remove terminated flow from database
        try:
            db.session.delete(flow)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash('Failed to delete specified Flow. Try again.', 'fail')
        flash('Your Flow has been Deleted', 'success')
        return redirect(url_for('home'))
    return render_template('delete_flow.html', title='Delete Flow',
                           form=form, legend='Delete Flow')


# used to create unique ids
def hashString(string):
    hash=0
    for i in range(len(string)):
        hash += ord(string[i]) * i
        hash = hash & hash
    return hash


if __name__ == '__main__':
#   app.run(debug=True)                                 to run with local browser only: http://127.0.0.1:5000/
    app.run(debug=True, port=7700, host="0.0.0.0" )    # to run on specified port on any interface
