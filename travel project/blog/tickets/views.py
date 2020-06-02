from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from blog import db, mail
from blog.models import Flight, Ticket
from blog.tickets.forms import SearchForm
from flask_mail import Message
import stripe

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

tickets = Blueprint('tickets', __name__)


@login_required
@tickets.route('/ticket', methods=['GET', 'POST'])
def ticket():
    form = SearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        if form.select.data == 'Departure location':
            flights = Flight.query.filter_by(departure=form.search.data).paginate(page=page, per_page=5)
        else:
            flights = Flight.query.filter_by(arrival=form.search.data).paginate(page=page, per_page=5)
        return render_template('ticket.html', flights=flights, public_key=public_key, form=form)
    else:
        page = request.args.get('page', 1, type=int)
        flights = Flight.query.order_by(Flight.date.asc()).paginate(page=page, per_page=7)

        return render_template('ticket.html', flights=flights, public_key=public_key, form=form)


@tickets.route('/success/<flight_id>')
def success(flight_id):
    info = Flight.query.filter_by(id=flight_id).first()
    if info:
        new_ticket = Ticket(info.date, info.departure, info.arrival, current_user.id, info.id)
        db.session.add(new_ticket)
        db.session.commit()
        msg = Message('Purchase confirmation!', sender='ann.bengardt@gmail.com', recipients=[current_user.email])
        msg.body = "You've bought a ticket\n{} - {}\n{}".format(info.departure, info.arrival, info.date)
        mail.send(msg)

    return render_template('success.html')


@tickets.route('/charge', methods=['POST'])
def charge():

    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        currency='rub',
        description='Ticket Charge'
    )
