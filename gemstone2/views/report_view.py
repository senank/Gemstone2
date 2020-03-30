from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden, HTTPFound

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import Report, KPI

from .report_actions import new_report

from datetime import datetime


import colander
import deform 
import pyramid_deform

import logging
log = logging.getLogger(__name__)

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token

@view_config(route_name='report_list', renderer='../templates/report.mako', permission = 'view')
def reports(request):
    
    user = request.user
    if user is not None:
        try:
            id_ = user.user_id
            auth_ = user.permissions
            query = request.dbsession.query(Report)
            reports = query.order_by(Report.year.desc(), Report.quarter.asc(), Report.company.asc()).all()
            

        except DBAPIError as ex:
            log.exception(ex)
            return Response(db_err_msg, content_type='text/plain', status=500)

    
    else:
        raise HTTPForbidden


    # class CSRFSchema(colander.MappingSchema):
    #     csrf_token = colander.SchemaNode(colander.String(), default=deferred_csrf_default, widget=deform.widget.HiddenWidget())

    # class MySchema(CSRFSchema):
    #     add_item = colander.SchemaNode(colander.String(),validator = colander.Length(min = 1, max = 24), description = 'Add new item', name = 'description')
   
    # schema = MySchema().bind(request=request)

    schema = colander.SchemaNode(colander.Mapping(), colander.SchemaNode(colander.String(), name = 'csrf_token',\
        default=deferred_csrf_default, widget=deform.widget.HiddenWidget()).bind(request=request))
    schema.add(colander.SchemaNode(colander.String(),validator = colander.Length(min = 1, max = 24), \
        widget = deform.widget.SelectWidget(values=((('MGR', 'MGR Plastics'), ('LP', 'Label & Pack'),))),
        name = 'company'))
    schema.add(colander.SchemaNode(colander.Integer(), \
        name = 'year'))
    schema.add(colander.SchemaNode(colander.Integer(),
        validator = colander.Range(min = 1, max = 4),
        widget = deform.widget.SelectWidget(values=(((1,1),(2,2),(3,3),(4,4),))),
        name = 'quarter',))


    myform = deform.Form(schema, buttons=('add',))
    form = myform.render()
    
    if 'add' in request.POST:
        
        control = request.params.items()
        try:
            form_data = myform.validate(control)

        except deform.exception.ValidationFailure as e:
            return {
                'auth_' : auth_,
                'reports': reports,
                'page_title': 'Gemstone II',
                'project': 'Gemstone II',
                'form': e.render(),
                 }

        new_report(request)
        return HTTPFound(location=request.route_url('report_list'))
    
    # elif 'delete' in request.POST:
    #     todo_item_delete(request)
    #     return HTTPFound(location=request.route_url('report_list'))

    return {
        'auth_' : auth_,
        'reports': reports,
        'page_title': 'Gemstone II',
        'project': 'Gemstone II',
        'form' : form
    }


@view_config(route_name = 'pdf_tester', renderer='../templates/pdf_tester.mako', permission = 'view')
def pdf_tester(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    report = request.dbsession.query(Report).filter(Report.id == id_).first()
    kpis = request.dbsession.query(KPI).filter(KPI.report_id == id_)

    #reports in this year for company of object report
    # (will include all current quarters)
    yearly_reports = request.dbsession.query(Report).filter(Report.year == report.year, Report.company == report.company)
    
    
    return {
        'report' : report,
        'yearly_reports' : yearly_reports,
        'page_title' : 'Gemstone II',
        'project' : 'Gemstone II',
        'kpis' : kpis,
    }


db_err_msg = 'Unable to load data'