from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Flight
import stripe

public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

tickets = Blueprint('tickets', __name__)


@tickets.route('/ticket')
def ticket():
    page = request.args.get('page', 1, type=int)
    flights = Flight.query.order_by(Flight.date.asc()).paginate(page=page, per_page=7)
    return render_template('ticket.html', flights=flights, public_key=public_key)


@tickets.route('/success')
def success():
    return render_template('success.html')


@tickets.route('/charge', methods=['POST'])
def charge():

    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1000,
        currency='usd',
        description='Ticket Charge'
    )

    return redirect(url_for("tickets.success"))