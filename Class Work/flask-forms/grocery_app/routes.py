from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login.utils import login_user, logout_user, login_required, current_user
from .models import GroceryStore, GroceryItem, User
from .forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from . import app, db, bcrypt

# Import app and db from events_app package so that we can run app
# from grocery_app import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("New user created!")

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form, action="/signup")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page if next_page else url_for("main.homepage"))

    return render_template("login.html", form=form, action="/login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))


@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)


@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_grocery_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by_id=current_user.id
        )

        db.session.add(new_grocery_store)
        db.session.commit()

        flash("New Grocery Store succesfully created!")

        return redirect(url_for("main.store_detail", store_id=new_grocery_store.id))

    return render_template('new_store.html', form=form)


@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()

    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by_id=current_user.id
        )

        db.session.add(new_item)
        db.session.commit()

        flash("New Grocery Item succesfully created!")

        return redirect(url_for("main.item_detail", item_id=new_item.id))

    return render_template('new_item.html', form=form)


@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data

        db.session.commit()

        flash("Grocery Store succesfully updated!")

        return redirect(url_for("main.store_detail", store_id=store.id))

    return render_template('store_detail.html', store=store, form=form)


@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data

        db.session.commit()

        flash("Grocery Item succesfully updated!")

        return redirect(url_for("main.item_detail", item_id=item.id))

    return render_template('item_detail.html', item=item, form=form)


@main.route("/add_to_shopping_list/<item_id>", methods=["POST"])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    user = User.query.get(current_user.id)
    if item:
        user.shopping_list_items.append(item)

        db.session.commit()

    return redirect(url_for("main.shopping_list"))


@main.route("/shopping_list")
@login_required
def shopping_list():
    user = User.query.get(current_user.id)
    shopping_list = user.shopping_list_items

    return render_template("shopping_list.html", shopping_list=shopping_list)
