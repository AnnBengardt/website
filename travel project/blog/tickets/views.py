from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Flight, Ticket
import stripe

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

tickets = Blueprint('tickets', __name__)


@tickets.route('/ticket')
def ticket():
    page = request.args.get('page', 1, type=int)
    flights = Flight.query.order_by(Flight.date.asc()).paginate(page=page, per_page=7)
    return render_template('ticket.html', flights=flights, public_key=public_key)


@tickets.route('/success/<flight_id>')
def success(flight_id):
    info = Flight.query.filter_by(id=flight_id).first()
    if info:
        new_ticket = Ticket(info.date, info.departure, info.arrival, current_user.id, info.id)
        db.session.add(new_ticket)
        db.session.commit()
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
