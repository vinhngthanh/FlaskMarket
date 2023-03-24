from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

from ..models import User, Product
from . import main
from .. import db
from .forms import AddUserForm, AddProductForm, LoginForm, DeleteUserForm

@main.route("/")
def home():
    return render_template('home.html')

@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@main.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main.route('/<int:user_id>/product/new', methods=['GET', 'POST'])
@login_required
def new_product(user_id):
    form = AddProductForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id = user_id).first()
        product = Product(title=form.title.data, description=form.description.data, price=form.price.data)
        product.user_id = user.id
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.product_detail', product_id = product.id))
    return render_template('new_product.html', form = form)

@main.route('/redirect_new_product')
def redirect_new_product():
    if current_user.is_authenticated:
        return redirect(url_for('main.new_product', user_id=current_user.id))
    else:
        flash('You must be logged in!', 'danger')
        return redirect(url_for('main.login'))
    
@main.route('/user/new', methods=['GET', 'POST'])
def new_user():
    form = AddUserForm()
    if form.validate_on_submit():
        search_email = User.query.filter_by(email=form.email.data).first()
        search_username = User.query.filter_by(username=form.username.data).first()
        if search_email is not None or search_username is not None:
            return render_template('new_user.html', form=form)
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        added = User.query.filter_by(email=form.email.data).first()
        login_user(added)
        flash('Account Created!', 'success')
        return redirect(url_for('main.user_profile', user_id=user.id))
    return render_template('new_user.html', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.user_profile', user_id=user.id))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.users'))

@main.route("/delete_user/<int:user_id>", methods = ["GET", "POST"])
def delete_user(user_id):
    form = DeleteUserForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(id=user_id).first()
        if user is not None and user.verify_password(form.password.data):
            db.session.delete(user)
            db.session.commit()
            flash('Account Deleted!', 'success')
            return redirect(url_for('main.users'))
        flash('Wrong Email or Password!', 'danger')
        return redirect(url_for("main.delete_user", user_id = user_id))
    
    return render_template("delete_user.html", form = form, user_id=user_id)

@main.route("/delete_product/<int:product_id>", methods = ["GET", "POST"])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product Deleted!', 'success')
        return redirect(url_for('main.products'))
    return redirect(url_for("main.product_detail", product_id = product_id))
    
