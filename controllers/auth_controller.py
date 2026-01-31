from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.repository import Repository




auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    repo=Repository()
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        #hash the password
        password_hash = generate_password_hash(password)
        new_user = repo.add_user(first_name, last_name, email, password_hash)
        session['user_id'] = new_user.user_id
        return redirect(url_for('logbook.logbook_home'))
#if form not submitted, render signup template
    return render_template('signup.html')
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        repo=Repository()
        user=repo.get_user_by_email(email)

        if user is None:
            return render_template('login.html', error="Invalid email or password.")
        if not check_password_hash(user.password_hash, password):
            return render_template('login.html', error="Invalid email or password.")
        session['user_id']=user.user_id
        return redirect(url_for('logbook.logbook_home'))
    
    return render_template('login.html', error=None)

@auth_bp.route('/logout')
def logout():
    repo=Repository()
    session.clear() 
    return redirect(url_for("auth.login"))
