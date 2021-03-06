from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import get_csrf_token
import pyramid.events

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import Report

import uuid
from deform.interfaces import FileUploadTempStore

import colander
import deform

import os
import shutil

from ..models import KPI

import pyramid_deform

import logging
log = logging.getLogger(__name__)

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token

@view_config(route_name='kpi_list', renderer='../templates/kpi_list.mako', permission = 'kpi_list')
def kpis(request):
    
    user = request.user
    if user is not None:
        try:
            id_ = user.user_id

            query = request.dbsession.query(KPI).filter(KPI.report_id == 987654321)

            kpis = query.distinct(KPI.kpi_name)
            checker = query.first()
            

        except DBAPIError as ex:
            log.exception(ex)
            return Response(db_err_msg, content_type='text/plain', status=500)

    
    else:
        raise HTTPForbidden

    schema = colander.SchemaNode(colander.Mapping(), colander.SchemaNode(colander.String(), name = 'csrf_token',\
        default=deferred_csrf_default, widget=deform.widget.HiddenWidget()).bind(request=request))
    schema.add(colander.SchemaNode(colander.String(), validator = colander.Length(min = 1, max = 60), \
        name = 'kpi', title = 'KPI Description'))


    myform = deform.Form(schema, buttons=('add',))
    form = myform.render()
    
    if 'add' in request.POST:
        error = {}
        control = request.params.items()
        try:
            form_data = myform.validate(control)

        except deform.exception.ValidationFailure as e:
            return {
                'checker': checker,
                'kpis': kpis,
                'page_title': 'Gemstone II',
                'project': 'Gemstone II',
                'form': e.render(),
                 }
        db_kpi = request.dbsession.query(KPI).filter(KPI.kpi_name == form_data['kpi'], KPI.report_id == 987654321).first()
        
        if db_kpi is None:
            kpi = KPI()
            kpi.report_id = 987654321
            kpi.kpi_name = form_data['kpi'].title()
            kpi.value = '---'
            kpi.target = '---'
            request.dbsession.add(kpi)
            return HTTPFound(location=request.route_url('kpi_list'))
        
        error['x'] = 'This is already a KPI'
        return {
            'checker' : checker,
            'error' : error,
            'kpis' : kpis,
            'page_title': 'Gemstone II',
            'project': 'Gemstone II',
            'form' : form
            
        }

    return {
        'checker': checker,
        'kpis': kpis,
        'page_title': 'Gemstone II',
        'project': 'Gemstone II',
        'form' : form
    }

@view_config(route_name = 'kpi_edit', renderer='../templates/kpi_edit.mako', permission = 'kpi_edit')
def kpi_edit(request):
    
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    kpi = request.dbsession.query(KPI).filter(KPI.kpi_id == id_, KPI.report_id == 987654321).first()
    
    if kpi is None:
        raise HTTPForbidden

    schema = colander.SchemaNode(colander.Mapping(), 
        colander.SchemaNode(colander.String(), 
        name = 'csrf_token',
        default=deferred_csrf_default,
        widget=deform.widget.HiddenWidget(),
        ).bind(request=request))

    
    #rename
    schema.add(colander.SchemaNode(colander.String(),
        validator = colander.Length(min = 1, max = 60),
        name = 'name',
        default = kpi.kpi_name,
        title="KPI Description"))

    myform = deform.Form(schema, buttons = ('save', 'delete', 'back'))
    form = myform.render()

    if 'save' in request.POST:
        control = request.params.items()

        try:
            form_data = myform.validate(control)
            
        except deform.exception.ValidationFailure as e:
            return {
                'kpi' : kpi,
                'id' : id_,
                'form' : e.render(),
                # 'desc': current['description']
                }
        
        kpi.kpi_name = form_data['name'].title()
        return HTTPFound(location = request.route_url('kpi_list'))

    if 'delete' in request.POST:
        request.dbsession.delete(kpi)
        request.dbsession.flush()
        return HTTPFound(location = request.route_url('kpi_list'))

    if 'back' in request.POST:
        return HTTPFound(location = request.route_url('kpi_list'))
    
    return {
        'kpi' : kpi,
        'id' : id_,
        'form' : form,
        # 'desc' : current['description'],
        # 'img' : img
    }

db_err_msg = 'Unable to load data'

@view_config(route_name = 'kpi_delete', permission = 'kpi_delete')
def kpi_delete(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    kpi = request.dbsession.query(KPI).filter(KPI.kpi_id == id_, KPI.report_id == 987654321).first()
    request.dbsession.delete(kpi)
    request.dbsession.flush()
    return HTTPFound(location = request.route_url('kpi_list'))