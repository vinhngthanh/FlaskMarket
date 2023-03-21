from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import AddProductForm, AddUserForm, LoginForm, DeleteUserForm
from models import db, User, Product
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/<int:user_id>/product/new', methods=['GET', 'POST'])
def new_product(user_id):
    form = AddProductForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id = user_id).first()
        product = Product(title=form.title.data, description=form.description.data, price=form.price.data)
        product.user_id = user.id
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_detail', product_id = product.id))
    return render_template('new_product.html', form = form)

@app.route('/redirect_new_product')
def redirect_new_product():
    if current_user.is_authenticated:
        return redirect(url_for('new_product', user_id=current_user.id))
    else:
        flash('You must be logged in!', 'danger')
        return redirect(url_for('login'))
    
@app.route('/user/new', methods=['GET', 'POST'])
def new_user():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        added = User.query.filter_by(email=form.email.data).first()
        login_user(added)
        flash('Account Created!', 'success')
        return redirect(url_for('user_profile', user_id=user.id))
    return render_template('new_user.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('user_profile', user_id=user.id))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('users'))

@app.route("/delete_user/<int:user_id>", methods = ["GET", "POST"])
def delete_user(user_id):
    form = DeleteUserForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(id=user_id).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            db.session.delete(user)
            db.session.commit()
            flash('Account Deleted!', 'success')
            return redirect(url_for('users'))
        flash('Wrong Email or Password!', 'danger')
        return redirect(url_for("delete_user", user_id = user_id))
    
    return render_template("delete_user.html", form = form, user_id=user_id)

@app.route("/delete_product/<int:product_id>", methods = ["GET", "POST"])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product Deleted!', 'success')
        return redirect(url_for('products'))
    return redirect(url_for("product_detail", product_id = product_id))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('error/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
