import re
from flask import Flask, abort, request, render_template, redirect, url_for, session,make_response, flash,jsonify,flash
import sqlite3
from flask_mail import Mail
import os
import pytz
from routes import UserViews
from flask_migrate import Migrate
import logging
from models import db
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.csrf import CSRFProtect, generate_csrf
from wtforms.validators import InputRequired, Email
from wtforms.validators import DataRequired
from datetime import datetime,timezone
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

def create_app():
    # project start   student.html
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'JunyiSun_secret_key'  # make safe
    app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
    app.config['SECURITY_PASSWORD_SALT'] = '3243f6a8885a308d313198a2e0370734'
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP   smtp.gmail.com
    app.config['MAIL_PORT'] = 587  # port
    app.config['MAIL_USE_TLS'] = True  
    app.config['MAIL_USERNAME'] = 's395615470@gmail.com'
    app.config['MAIL_PASSWORD'] = 'johgpueksgsakecj'  # Gmail

    app.config['MAIL_DEFAULT_SENDER'] = 's395615470@gmail.com'  # default email

    migrate = Migrate()
    csrf = CSRFProtect()
    login_manager = LoginManager()
    mail = Mail()
    
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)


    app.register_blueprint(UserViews.bp)

    with app.app_context():
        db.create_all()

    from passwordReset import PasswordResetService
    app.password_reset_service = PasswordResetService()

    return app


app = create_app()


def is_valid_email(email):
    # Define a regex pattern for validating email addresses
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Register')

@app.route('/', methods=['GET', 'POST'])
@app.route('/access/', methods=['GET', 'POST'])
def access():
    login_form = LoginForm()
    register_form = RegisterForm()
    
    if 'login' in request.form and login_form.validate_on_submit():
        # Handle login logic
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user)
            # Define the Shanghai timezone using pytz
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            # Get the current UTC time as a timezone-aware datetime object
            current_utc_time = datetime.now(timezone.utc)
            # Convert the UTC time to Shanghai time
            current_shanghai_time = current_utc_time.astimezone(shanghai_tz)
            user.last_seen = current_shanghai_time
            # Commit changes to the database if this is being used in a web app
            db.session.commit()
            session['loggedin'] = True
            session['username'] = user.name
            return redirect(url_for('main'))  # success page
        else:
            return render_template('result.html', login_form=login_form, register_form=register_form, msg='Incorrect username or password!')

    elif 'register' in request.form and register_form.validate_on_submit():
        # Handle registration logic
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        if not is_valid_email(email):
            user_message = "Registration failed due to invalid email format. Please enter a valid email address."
            return render_template('result.html', login_form=login_form, register_form=register_form, msg=user_message)
        try:
            new_user = User(name=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('student'))
        except Exception as e:
            db.session.rollback()
            user_message = "Registration failed due to a database error. Please use a different username and email address."
            return render_template('result.html', login_form=login_form, register_form=register_form, msg=user_message)

    return render_template('student.html', login_form=login_form, register_form=register_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Register function called")  # for testing
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        try:
            username = register_form.username.data
            password = register_form.password.data
            email = register_form.email.data
            new_user = User(name=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('access'))
        except Exception as e:
            db.session.rollback()
            user_message = "Registration failed due to a database error. Please use a different username and email address."
            return render_template("error.html", message=user_message)

    return render_template("student.html", register_form=register_form)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(name=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            session['loggedin'] = True
            session['username'] = user.name
            
            return render_template('main.html', msg='Login successful!')  
            # return redirect(url_for('index'))  # 假设你有一个名为 'index' 的视图函数
        else:
            return render_template('result.html', form=login_form, msg='Incorrect username or password！')
    return render_template('login.html', login_form=login_form)

from werkzeug.security import generate_password_hash

@app.route('/update_profile', methods=['POST'])


@app.route('/logout/', endpoint='logout1')
def logout():
    logout_user()

    return redirect(url_for('student'))

@app.route('/update_name', methods=['POST'])
@login_required
def update_name():
    current_user.name = request.form['name']
    db.session.commit()
    flash('Your name has been updated.')
    return redirect(url_for('dashboard'))

@app.route('/update_email', methods=['POST'])
@login_required
def update_email():
    
    current_user.email = request.form['email']
    db.session.commit()
    flash('Your email has been updated.')
    return redirect(url_for('dashboard'))

@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    if 'password' in request.form and request.form['password']:
        # Update the user's password
        hashed_password = generate_password_hash(request.form['password'])
        current_user.password = hashed_password
        db.session.commit()
        flash('Password update successful. Redirecting to student page in 10 seconds...', 'success')
    else:
        flash('Please enter a new password.', 'error')
    
    # Redirect back to the dashboard page
    return redirect(url_for('dashboard'))
    
import hashlib
import time

def gravatar_url(email, size=100, default='retro', rating='g'):
    """Generate a gravatar URL based on the email provided."""
    hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    url = f"https://www.gravatar.com/avatar/{hash}?s={size}&d={default}&r={rating}"
    return url

from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from flask import render_template

def get_user_rank_and_score(user_id):
    # Reuse the same logic to calculate scores
    post_scores = db.session.query(
        User.id.label('user_id'),
        (5 * func.count(Request.id)).label('score')
    ).join(Request, User.name == Request.username).group_by(User.id).subquery()

    reply_scores = db.session.query(
        User.id.label('user_id'),
        (3 * func.count(Reply.id)).label('score')
    ).join(Reply, User.name == Reply.responderName).group_by(User.id).subquery()

    like_scores = db.session.query(
        User.id.label('user_id'),
        func.count(Like.id).label('score')
    ).join(Like, User.id == Like.user_id).group_by(User.id).subquery()

    received_like_scores = db.session.query(
        User.id.label('user_id'),
        (2 * func.count(Like.id)).label('score')
    ).join(Reply, Reply.responderName == User.name
    ).join(Like, Reply.id == Like.reply_id).group_by(User.id).subquery()

    final_scores = db.session.query(
        User.id,
        User.name,
        (func.coalesce(post_scores.c.score, 0) +
         func.coalesce(reply_scores.c.score, 0) +
         func.coalesce(like_scores.c.score, 0) +
         func.coalesce(received_like_scores.c.score, 0)).label('score')
    ).select_from(User
    ).outerjoin(post_scores, User.id == post_scores.c.user_id
    ).outerjoin(reply_scores, User.id == reply_scores.c.user_id
    ).outerjoin(like_scores, User.id == like_scores.c.user_id
    ).outerjoin(received_like_scores, User.id == received_like_scores.c.user_id
    ).order_by(db.desc('score')).all()

    # Find user rank and score
    rank = 1
    current_score = None
    user_rank = None
    user_score = None
    for index, result in enumerate(final_scores):
        if result.id == user_id:
            if current_score != result.score:
                user_rank = index + 1
                current_score = result.score
            user_score = result.score
            break

    return user_rank, user_score


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user
    # Handle form submission for updating bio
    if request.method == 'POST':
        new_bio = request.form.get('bio', '')
        user.bio = new_bio
        db.session.commit()
        flash('Your bio has been updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    requests = user.get_requests(user.name)
    avatar = gravatar_url(user.email)
    user_time_zone = pytz.timezone('Asia/Shanghai')  # Correctly using a specific timezone
    un_last_seen = current_user.last_seen.astimezone(user_time_zone) if current_user.last_seen else "Never"
    last_seen = un_last_seen.strftime("%Y-%m-%d %I:%M %p")  # Format with AM/PM
    user_rank, user_score = get_user_rank_and_score(user.id)
  # Directly access the requests, assuming the relationship is defined in the User model
    return render_template('dashboard.html', user=user, requests=requests,avatar=avatar,user_rank=user_rank, user_score=user_score,last_seen=last_seen)

from flask_login import login_required, current_user  # Assuming you're using flask_login for user session management

@app.route('/request/<int:request_id>')
@login_required
def specific_request(request_id):
    request_obj = Request.query.get(request_id)  # Using get for direct ID access
    if not request_obj:
        #flash('Request not found.', 'error')  # Flash a message if no request found
        return redirect(url_for('main'))  # Redirect to a safe page

    # Prepare reply form data if needed, for example:
    # If using WTForms, instantiate your form here if it's going to be rendered on the same page

    return render_template('specific_request.html', request=request_obj)

@app.route('/delete_request/<int:request_id>', methods=['POST'])
@login_required
def delete_request(request_id):
    request = Request.query.get(request_id)
    if request.username != current_user.name:
        abort(403)  # Prevent deleting requests not owned by the user
    db.session.delete(request)
    db.session.commit()
    flash('Request deleted successfully!', 'success')
    return redirect(url_for('dashboard'))



@app.route('/errorPage')
def errorPage():
    # show the error
    return "There is an error and please try later"

# this is for a main    http://127.0.0.1:5000   
@app.route('/')
def regi_login():
    return render_template('student.html')

# view page       http://127.0.0.1:5000/main/
@app.route('/main')
def main():
    return render_template('main.html')

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

# create a Request        http://127.0.0.1:5000/createRequest/
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    form = RequestForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        username = session.get('username')

        if not username:
            return redirect(url_for('login'))

        new_request = Request(title=title, description=description, username=username)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('createRequest.html', form=form)


from dateutil.relativedelta import relativedelta

def time_since(dt):
    """Return the time difference from now to a given datetime in a user-specific timezone."""
    if dt is None:
        return "Never"
    now = datetime.now()  # Get current time
   

    if dt > now:
        # dt is in the future
        diff = relativedelta(dt, now)  # Note the swapped arguments
    else:
        # dt is in the past
        diff = relativedelta(now, dt)
  
    if diff.years > 0:
        return f"{diff.years} year{'s' if diff.years > 1 else ''} ago"
    if diff.months > 0:
        return f"{diff.months} month{'s' if diff.months > 1 else ''} ago"
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    if diff.hours > 0:
        return f"{diff.hours} hour{'s' if diff.hours > 1 else ''} ago"
    if diff.minutes > 0:
        return f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} ago"
    if diff.seconds > 0:
        return f"{diff.seconds} second{'s' if diff.seconds > 1 else ''} ago"
    return "just now"


from sqlalchemy.exc import SQLAlchemyError

def model_to_dict(model, with_avatar=False, include_user_details=False):
    data = {column.name: getattr(model, column.name) for column in model.__table__.columns}

    if with_avatar or include_user_details:
        user_field = getattr(model, 'username', None) or getattr(model, 'responderName', None)

        if user_field:
            try:
                user = User.query.filter_by(name=user_field).first()
                if user:
                    if with_avatar:
                        data['email'] = user.email
                        data['avatar_url'] = user.gravatar_url()
                    if include_user_details:
                        data['user_bio'] = getattr(user, 'bio', 'No bio available')
                        data['user_last_seen'] = time_since(user.last_seen)
            except SQLAlchemyError as e:
                print(f"An error occurred while fetching user data: {str(e)}")

    return data


class ReplyForm(FlaskForm):
    reply = TextAreaField('Reply', validators=[DataRequired()])

#  this is for findRequest       http://127.0.0.1:5000/main/          @app.route('/findRequest')
from flask import render_template, request

@app.route('/findRequest')
def findRequest():
    search_queryFR = request.args.get('searchQueryFR', '').strip()
    rows = []
    message = 'No matching requests found.' if search_queryFR else 'Recent requests:'

    if search_queryFR:
        try:
            # Filter requests based on the title containing the search query
            requests = Request.query.filter(Request.title.ilike(f'%{search_queryFR}%')).all()
        except Exception as e:
            message = 'An issue occurred during the search process.'
            print(f"Search request failed, error: {e}")
            return render_template('findRequest.html', rows=[], message=message, search_queryFR=search_queryFR)
    else:
        # Fetch recent requests if no search query is provided
        requests = Request.query.order_by(Request.title).limit(5).all()

    # Prepare data for all fetched requests
    for req in requests:
        row = model_to_dict(req, with_avatar=True, include_user_details=True)
        replies = Reply.query.filter_by(request_id=req.id).all()
        row['replies'] = [model_to_dict(reply, with_avatar=True) for reply in replies]  # Ensure avatars for replies
        
        # Aggregate likes for each reply and add other necessary data
        for reply in row['replies']:
            reply['like_count'] = Like.query.filter_by(reply_id=reply['id']).count()

        row['form'] = ReplyForm()  # Instantiate a reply form for each request
        rows.append(row)

    # Render the template with the data
    return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)



# this is to reply        people could click submit button     and then reply
@app.route('/replyRequest', methods=['GET', 'POST'])
def replyRequest():
    if request.method == 'POST':
        reply_content = request.form['reply']
        responderName = session.get('username')
        request_title = request.form.get('search_queryFR')
        request_id = request.form.get('request_id')

        if not responderName:
            return redirect(url_for('student'))
        # if reply_content and request_title and request_id:
        if reply_content and request_id:
            matching_request = Request.query.filter(
                        Request.title.like('%' + request_title + '%'),
                        Request.id == request_id  # ID is match
                    ).first()
        #  # use  SQLAlchemy 

            
            if matching_request:
                new_reply = Reply(request_id=matching_request.id, reply_content=reply_content, responderName=responderName)
                db.session.add(new_reply)
                db.session.commit()

                return redirect(url_for('findRequest'))
            else:
                return render_template('findRequest.html', error="Cannot find the request")

        else:
            return render_template('findRequest.html', error="Reply content cannot be empty")

    else:
        request_title = request.args.get('search_queryFR')
        return render_template('findRequest.html', request_title=request_title)





@app.route('/student')
def student():
    register_form = RegisterForm()
    login_form = LoginForm()  
    return render_template('student.html', register_form=register_form, login_form=login_form)



class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

# user and email  should match    click Forget my password to skip the page
@app.route('/forgot_password')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    return render_template('forgotPassword.html', form=form)



# button  send to my email
@app.route('/send_link', methods=['POST'])
def sendLink():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            from passwordReset import PasswordResetService
            PasswordResetService.sendUpdatePassword(email)
            flash("Send the email, please check personal email", 'success')
            return redirect(url_for('student'))
        else:
            flash("This email is not in Database", 'danger')
            return render_template('forgotPassword.html', form=form)
    return render_template('forgotPassword.html', form=form) 



class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


# use  qq email for this project
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    register_form = RegisterForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        from passwordReset import PasswordResetService  
        email = PasswordResetService.verify_reset_token(token)
        if email is None:
            flash('The reset token is invalid or has expired.', 'error')
            return redirect(url_for('reset_request'))
        PasswordResetService.update_password(email, new_password)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('student'))
    return render_template('reset_password.html', form=form, register_form=register_form, login_form=login_form, token=token)


@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')





#  similar to reset_password    qq email
@app.route('/change_password', methods=['POST'])
def change_password():
    token = request.args.get('token')  # get token
    new_password = request.form['new_password']
    if not new_password:
        flash('No new password provided.', 'error')  # no password
        return redirect(url_for('reset_request'))  
    from passwordReset import PasswordResetService
    email = PasswordResetService.verify_reset_token(token)
    if email is None:
        flash('The reset token is invalid or has expired.', 'error')
        return redirect(url_for('reset_request'))  

    if not email:  
        flash('The email is invalid.', 'error')
        return redirect(url_for('reset_request'))  
    PasswordResetService.update_password(email, new_password)
    flash('Your password has been updated!', 'success')
    return redirect(url_for('login'))



from flask_login import current_user, login_required
from flask import session, jsonify, request
from models import Like, User

@app.route('/like', methods=['POST'])
@login_required
def like():
    reply_id = request.json.get('reply_id')

    existing_like = Like.query.filter_by(user_id=current_user.id, reply_id=reply_id).first()
    if existing_like:
        return jsonify({'replay_id':reply_id, 'message': 'Already liked'}), 400

    new_like = Like(user_id=current_user.id, reply_id=reply_id)
    db.session.add(new_like)
    try:
        db.session.commit()
        like_count = Like.query.filter_by(reply_id=reply_id).count()
        return jsonify({'message': 'Like successful', 'like_count': like_count}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500




#get count-likes
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments

from models import User, Request, Reply, Like
from sqlalchemy import func



@app.route('/Ranking')
def ranking():
    """Generate ranking and line chart page"""
    rankings = ranking_logic()

    # Prepare line chart data
    user_names = [r[2] for r in rankings]  # User names
    scores = [r[3] for r in rankings]  # Corresponding scores

    plt.style.use('grayscale')  # Use grayscale background style
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(user_names, scores, marker='o', linestyle='-', color='black')  # Black line and points
    ax.set_facecolor((0.5, 0.5, 0.5, 0.5))  # RGBA where 0.5 is the transparency level
    fig.patch.set_facecolor('none')  # Transparent outer background of the chart
    fig.patch.set_alpha(0.01)

    # Set border color
    for spine in ax.spines.values():
        spine.set_color('black')  # Set to black
        spine.set_linewidth(1)  # Set border width

    plt.xticks(rotation=45, color='black', ha='right')  # Rotate X-axis labels 45 degrees, set color to black
    plt.yticks(color='black')  # Set Y-axis tick color
    plt.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.9)
    ax.grid(False)  # Remove grid lines
    ax.set_xlabel('User', color='black')  # X-axis title
    ax.set_ylabel('Score', color='black')  # Y-axis title

    # Save the chart to a byte stream
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Convert to Base64 encoding and embed in HTML
    img_base64 = base64.b64encode(img.read()).decode('utf8')

    # Pass ranking data and line chart to the template
    return render_template('Ranking.html', rankings=rankings, img_base64=img_base64)

def ranking_logic():
    """Logic for retrieving ranking data from the database"""
    post_scores = db.session.query(
        User.id.label('user_id'),
        (5 * func.count(Request.id)).label('score')
    ).join(Request, User.name == Request.username
    ).group_by(User.id).subquery()

    reply_scores = db.session.query(
        User.id.label('user_id'),
        (3 * func.count(Reply.id)).label('score')
    ).join(Reply, User.name == Reply.responderName
    ).group_by(User.id).subquery()

    like_scores = db.session.query(
        User.id.label('user_id'),
        func.count(Like.id).label('score')
    ).join(Like, User.id == Like.user_id
    ).group_by(User.id).subquery()

    received_like_scores = db.session.query(
        User.id.label('user_id'),
        (2 * func.count(Like.id)).label('score')
    ).join(Reply, Reply.responderName == User.name
    ).join(Like, Reply.id == Like.reply_id
    ).group_by(User.id).subquery()

    final_scores = db.session.query(
        User.id,
        User.name,
        (func.coalesce(post_scores.c.score, 0) +
         func.coalesce(reply_scores.c.score, 0) +
         func.coalesce(like_scores.c.score, 0) +
         func.coalesce(received_like_scores.c.score, 0)).label('score')
    ).select_from(User
    ).outerjoin(post_scores, User.id == post_scores.c.user_id
    ).outerjoin(reply_scores, User.id == reply_scores.c.user_id
    ).outerjoin(like_scores, User.id == like_scores.c.user_id
    ).outerjoin(received_like_scores, User.id == received_like_scores.c.user_id
    ).group_by(User.id, User.name
    ).order_by(db.desc('score'))

    results = final_scores.all()

    rankings = []
    rank = 1
    current_score = None
    for index, result in enumerate(results):
        user_id, name, score = result
        if score != current_score:
            rank = index + 1
            current_score = score
        rankings.append((rank, user_id, name, score))

    return rankings


# this is at the end of lines   
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)