from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import Flight

tickets = Blueprint('tickets', __name__)

@tickets.route('/ticket')
def ticket():
    page = request.args.get('page', 1, type=int)
    flights = Flight.query.order_by(Flight.date.asc()).paginate(page=page, per_page=7)
    return render_template('ticket.html', flights=flights)