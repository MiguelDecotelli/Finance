from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import func
from my_shares import app, db
from my_shares.credit_card import check_credit_card
from my_shares.forms import *
from my_shares.models import User, Portfolio
from my_shares.my_functions import apology, lookup, usd
from werkzeug.security import check_password_hash, generate_password_hash

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.jinja_env.filters["usd"] = usd


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data,
                    password=form.password.data,
                    )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return apology('Username is already taken!')

        flash("Registered!")
        return redirect(url_for("login"))

    return render_template("/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            return apology("Invalid username or password", 403)

        login_user(user)
        flash(f'Welcome, {user.username}!')

        return redirect(url_for("index"))

    return render_template("/login.html", form=form)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change username's password"""

    form = ChangePassword()

    if form.validate_on_submit():
        user = User.query.filter_by(username=User.username).first()
        old_password = request.form.get("old_password")

        if not user.check_password(old_password):
            return apology("Password is incorrect!", 400)
        else:
            new_password = generate_password_hash(
                request.form.get("new_password"))

            current_user.password_hash = new_password

            db.session.commit()
            flash("Password changed!")
            return redirect("/")

    return render_template("change_password.html", form=form)


@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('See you soon!')
    return redirect(url_for('index'))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    form = QuoteForm()

    if form.validate_on_submit():
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        try:
            ticker = lookup(request.form.get("symbol"))
            return render_template("quoted.html", name=ticker["name"], symbol=ticker["symbol"], price=ticker["price"])
        except (KeyError, TypeError, ValueError):
            return apology("Invalid ticker symbol", 400)

    return render_template("quote.html", form=form)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    form = BuyForm()

    if form.validate_on_submit():

        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)

        try:
            new_shares = int(request.form.get("shares"))
        except:
            return apology("Must be integer", 400)

        try:
            ticker = lookup(request.form.get("symbol"))
            new_stocks = ticker["price"] * float(new_shares)
        except (KeyError, TypeError, ValueError):
            return apology("Invalid ticker symbol", 400)

        if new_shares <= 0:
            return apology("Must be positive number", 400)
        else:
            user_cash = current_user.cash

            if new_stocks > user_cash:
                return apology("Can't afford", 400)
            else:
                current_user.cash -= new_stocks

                portfolio = Portfolio(user_id=current_user.id,
                                      symbol=form.symbol.data.upper(),
                                      name=ticker["name"],
                                      shares=form.shares.data,
                                      transaction_type="Buy",
                                      price=ticker["price"],
                                      total=ticker["price"]*new_shares,
                                      )
                db.session.add(portfolio)
                db.session.commit()
                flash("Bought!")
                return redirect("/")

    return render_template("/buy.html", form=form)


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    my_portfolio = (
        db.session.query(
            Portfolio.symbol,
            Portfolio.name,
            func.sum(Portfolio.shares).label('shares'),
            func.max(Portfolio.price).label('price'),
            func.sum(Portfolio.total).label('total')
        )
        .filter_by(user_id=current_user.id)
        .group_by(Portfolio.symbol, Portfolio.name)
        .order_by(Portfolio.symbol)
        .all()
    )
    print(my_portfolio)
    # Creating an empty list to store updated share information
    portfolio = []

    # Updating prices and calculating totals for each share
    for share in my_portfolio:
        print(share)

        share_info = lookup(share.symbol)
        print(share.name)
        print(f"Info: {share_info}")
        if share_info is not None:
            current_price = lookup(share.symbol)["price"]
            total = current_price * int(share.shares)

            # Creating a dictionary with updated share information
            updated_share = {
                "symbol": share.symbol,
                "name": share.name,
                "shares": share.shares,
                "price": current_price,
                "total": total
            }

            # Appending the updated share to the list
            portfolio.append(updated_share)
        else:
            portfolio = []

    cash = current_user.cash
    total_cash = cash + sum(entry["total"] for entry in portfolio)
    print(portfolio)

    return render_template("index.html", portfolio=portfolio, cash=cash, total_cash=total_cash)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    portfolio = Portfolio.query.all()
    form = SellForm()

    if form.validate_on_submit():
        ticker = lookup(request.form.get("symbol"))

        if not ticker:
            return apology("Missing symbol", 400)

        if ticker is None:
            return apology("Invalid symbol", 400)

        try:
            shares_to_sell = int(request.form.get("shares"))
        except ValueError:
            return apology("Must be integer", 400)

        my_shares = (
            db.session.query(
                Portfolio.shares
            )
            .filter_by(
                user_id=current_user.id,
                symbol=ticker["symbol"])
            .all()
        )
        all_shares = sum(int(value.shares) for value in my_shares)

        if not my_shares:
            return apology("You don't have any of this shares!", 400)

        if shares_to_sell > all_shares:
            return apology("Not enough shares", 400)
        elif shares_to_sell <= 0:
            return apology("Must be positive number", 400)

        current_price = ticker["price"]

        new_sell = current_price * shares_to_sell

        current_user.cash += new_sell

        sold_shares = Portfolio(
            user_id=current_user.id,
            symbol=ticker["symbol"],
            name=ticker["name"],
            shares=-shares_to_sell,
            transaction_type="Sell",
            price=current_price,
            total=new_sell
        )
        db.session.add(sold_shares)

        db.session.commit()

        flash("Sold!")
        return redirect("/")

    return render_template("sell.html", form=form, portfolio=portfolio)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = Portfolio.query.filter_by(
        user_id=current_user.id).all()

    return render_template("history.html", transactions=transactions)


@app.route("/list_of_stocks", methods=["GET", "POST"])
@login_required
def list_of_stocks():
    """Show the list of all stocks"""

    form = StockListForm()

    import csv
    list_of_shares = []
    no_company = False

    if form.validate_on_submit():
        search_query = form.symbol_search.data.lower()

        with open('all_stocks.csv') as file:
            stocks = csv.DictReader(file)
            for row in stocks:
                if search_query in row["Company Name"].lower():
                    list_of_shares.append({"symbol": row["Symbol"], "company_name": row["Company Name"],
                                           "industry": row["Industry"], "market_cap": row["Market Cap"]})

        if not list_of_shares:
            no_company = True

    return render_template("list_of_stocks.html", form=form,  list_of_shares=list_of_shares, no_company=no_company)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add more cash into user's account"""

    form = CashForm()

    if form.validate_on_submit():
        user_password = current_user.password_hash
        if not check_password_hash(user_password, request.form.get("password")):
            return apology("Password is incorrect!", 403)
        else:
            card = request.form.get("add_card")
            if check_credit_card(card) == False:
                return apology("CARD IS INVALID", 403)
            else:
                add_cash = int(request.form.get("add_cash"))
                current_user.cash += add_cash
                db.session.commit()
                flash("Cash Added!")

            return redirect("/")

    return render_template("/add_cash.html", form=form)


if __name__ == "__main__":
    app.run(debug=False)
