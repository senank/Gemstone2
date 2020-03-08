from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
import pyramid.events

from datetime import datetime

from ..models import Report

@view_config(route_name='add_report', request_method='POST')
def add_report(request):
    pass
    # comp = request.POST.get('company')
    # year = request.POST.get('year')

    # report = Report()
    # report.company = comp
    # report.quarter = 1
    # report.year = int(year)
    # last_updated = datetime.now()

    # request.dbsession.add(report)
    # return HTTPFound(location=request.route_url('home'))