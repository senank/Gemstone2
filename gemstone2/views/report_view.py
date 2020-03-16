from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden, HTTPFound

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import Report

# from .report_actions import add

from datetime import datetime


# import colander
# import deform 
# import pyramid_deform

# import logging
# log = logging.getLogger(__name__)

# @colander.deferred
# def deferred_csrf_default(node, kw):
#     request = kw.get('request')
#     csrf_token = request.session.get_csrf_token()
#     return csrf_token

@view_config(route_name='report_list', renderer='../templates/report.mako')
def reports(request):
    
    # user = request.user
    # if user is not None:
    try:
        # id_ = user.user_id
        query = request.dbsession.query(Report)
        reports = query.order_by(Report.year.desc(), Report.quarter.asc(), Report.company.asc()).all()
        

    except DBAPIError as ex:
        log.exception(ex)
        return Response(db_err_msg, content_type='text/plain', status=500)

    # if 'add_test' in request.POST:
    #     add(request)
    #     return HTTPFound(location=request.route_url('home'))
    # else:
    #     raise HTTPForbidden


    # class CSRFSchema(colander.MappingSchema):
    #     csrf_token = colander.SchemaNode(colander.String(), default=deferred_csrf_default, widget=deform.widget.HiddenWidget())

    # class MySchema(CSRFSchema):
    #     add_item = colander.SchemaNode(colander.String(),validator = colander.Length(min = 1, max = 24), description = 'Add new item', name = 'description')
   
    # schema = MySchema().bind(request=request)

    # schema = colander.SchemaNode(colander.Mapping(), colander.SchemaNode(colander.String(), name = 'csrf_token',\
    #     default=deferred_csrf_default, widget=deform.widget.HiddenWidget()).bind(request=request))
    # schema.add(colander.SchemaNode(colander.String(),validator = colander.Length(min = 1, max = 24), \
    #     description = 'Add new item', name = 'description'))


    # myform = deform.Form(schema, buttons=('add', 'delete'))
    # form = myform.render()
    
    # if 'add' in request.POST:
        
    #     control = request.POST.items()
    #     try:
    #         myform.validate(control)
    #     except deform.exception.ValidationFailure as e:
    #         return {
    #             'todos': todos,
    #             'page_title': 'To-Do',
    #             'project': 'To-Do',
    #             'form': e.render()
    #             }
    #     todo_item_add(request)
    #     return HTTPFound(location=request.route_url('todo_list'))
    
    # elif 'delete' in request.POST:
    #     todo_item_delete(request)
    #     return HTTPFound(location=request.route_url('todo_list'))

    return {
       'reports': reports,
       'page_title': 'Gemstone II',
       'project': 'Gemstone II',
    #    'form' : form
    }


db_err_msg = 'Unable to load data'