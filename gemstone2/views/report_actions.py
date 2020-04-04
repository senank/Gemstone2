from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import get_csrf_token
import pyramid.events

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import Report, KPI

import uuid
from deform.interfaces import FileUploadTempStore

import psycopg2
import ast

import colander
import deform
# from .report_view import pdf_t
import os
import shutil

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def my_ruler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')
    
    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')

def dic_of_data(report):
    current = {
        'company' : report.company,
        'quarter' : report.quarter,
        'year' : report.year,

        'highlight1' : report.highlight1,
        'highlight2' : report.highlight2,
        'highlight3' : report.highlight3,
        'highlight4' : report.highlight4,
        'highlight5' : report.highlight5,
        'highlight6' : report.highlight6,
        'highlight7' : report.highlight7,
        'highlight8' : report.highlight8,
        'highlight9' : report.highlight9,

        'operation1' : report.operation1,
        'operation2' : report.operation2,
        'operation3' : report.operation3,
        'operation4' : report.operation4,
        'operation5' : report.operation5,
        'operation6' : report.operation6,
        'operation7' : report.operation7,
        'operation8' : report.operation8,
        'operation9' : report.operation9,

        'strategy1' : report.strategy1,
        'strategy2' : report.strategy2,
        'strategy3' : report.strategy3,
        'strategy4' : report.strategy4,
        'strategy5' : report.strategy5,
        'strategy6' : report.strategy6,
        'strategy7' : report.strategy7,
        'strategy8' : report.strategy8,
        'strategy9' : report.strategy9,
        
        'customer_gained1' : report.customer_gained1,
        'customer_gained2' : report.customer_gained2,
        'customer_gained3' : report.customer_gained3,
        'customer_gained4' : report.customer_gained4,
        'customer_gained5' : report.customer_gained5,
        'customer_gained6' : report.customer_gained6,
        'customer_gained7' : report.customer_gained7,
        'customer_gained8' : report.customer_gained8,
        'customer_gained9' : report.customer_gained9,
        
        'order1' : report.order1,
        'order2' : report.order2,
        'order3' : report.order3,
        'order4' : report.order4,
        'order5' : report.order5,
        'order6' : report.order6,
        'order7' : report.order7,
        'order8' : report.order8,
        'order9' : report.order9,
        
        'revenue_1' : report.revenue_1,
        'revenue_2' : report.revenue_2,
        'revenue_3' : report.revenue_3,
        'revenue_4' : report.revenue_4,
        'revenue_YTD' : report.revenue_YTD,
        'revenue_FY' : report.revenue_FY,
        'revenue_plan' : report.revenue_plan,

        'profit_1' : report.profit_1,
        'profit_2' : report.profit_2,
        'profit_3' : report.profit_3,
        'profit_4' : report.profit_4,
        'profit_YTD' : report.profit_YTD,
        'profit_FY' : report.profit_FY,
        'profit_plan' : report.profit_plan,

        'EBITDA_1' : report.EBITDA_1,
        'EBITDA_2' : report.EBITDA_2,
        'EBITDA_3' : report.EBITDA_3,
        'EBITDA_4' : report.EBITDA_4,
        'EBITDA_YTD' : report.EBITDA_YTD,
        'EBITDA_FY' : report.EBITDA_FY,
        'EBITDA_plan' : report.EBITDA_plan,

        'cf_1' : report.cf_1,
        'cf_2' : report.cf_2,
        'cf_3' : report.cf_3,
        'cf_4' : report.cf_4,
        'cf_YTD' : report.cf_YTD,
        'cf_FY' : report.cf_FY,
        'cf_plan' : report.cf_plan,

        'explain' : eval(report.explain),

        'filename' : report.filename,
        'unique_filename' : report.unique_filename
    }
    return current

def remove_files(path_name, item_name):
    for dirs, subdirs, files in os.walk(path_name):
        try:
            os.remove('{}/{}'.format(dirs, item_name.unique_filename))
        except:
            pass

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token


@view_config(route_name = 'new_report', request_method = 'POST', permission = 'add')
def new_report(request):
    
    report = Report()
    
    report.company = request.params.get('company')
    report.quarter = request.params.get('quarter') or 1
    report.year = request.params.get('year') or date.today().year
    report.last_updated = datetime.now()
    
    if request.params.get('quarter') != 1:
        yearly_reports = request.dbsession.query(Report).filter(Report.year == request.params.get('year'))
        for quarter in yearly_reports:
            
            if quarter.quarter == 1:
                report.revenue_1 = quarter.revenue_1
                report.profit_1 = quarter.profit_1
                report.EBITDA_1 = quarter.EBITDA_1
                report.cf_1 = quarter.cf_1

                report.revenue_plan = quarter.revenue_plan
                report.profit_plan = quarter.profit_plan
                report.EBITDA_plan = quarter.EBITDA_plan
                report.cf_plan = quarter.cf_plan
                
            if quarter.quarter == 2:
                report.revenue_2 = quarter.revenue_2
                report.profit_2 = quarter.profit_2
                report.EBITDA_2 = quarter.EBITDA_2
                report.cf_2 = quarter.cf_2

                report.revenue_plan = quarter.revenue_plan
                report.profit_plan = quarter.profit_plan
                report.EBITDA_plan = quarter.EBITDA_plan
                report.cf_plan = quarter.cf_plan

            if quarter.quarter == 3:
                report.revenue_3 = quarter.revenue_3
                report.profit_3 = quarter.profit_3
                report.EBITDA_3 = quarter.EBITDA_3
                report.cf_3 = quarter.cf_3

                report.revenue_plan = quarter.revenue_plan
                report.profit_plan = quarter.profit_plan
                report.EBITDA_plan = quarter.EBITDA_plan
                report.cf_plan = quarter.cf_plan

        report.revenue_4 = 0
        report.revenue_YTD = 0
        report.revenue_FY = 0

        report.profit_4 = 0
        report.profit_YTD = 0
        report.profit_FY = 0

        report.EBITDA_4 = 0
        report.EBITDA_YTD = 0
        report.EBITDA_FY = 0

        report.cf_4 = 0
        report.cf_YTD = 0
        report.cf_FY = 0

    else:
        report.revenue_1 = 0
        report.revenue_2 = 0
        report.revenue_3 = 0
        report.revenue_4 = 0
        report.revenue_YTD = 0
        report.revenue_FY = 0
        report.revenue_plan = 0

        report.profit_1 = 0
        report.profit_2 = 0
        report.profit_3 = 0
        report.profit_4 = 0
        report.profit_YTD = 0
        report.profit_FY = 0
        report.profit_plan = 0

        report.EBITDA_1 = 0
        report.EBITDA_2= 0
        report.EBITDA_3 = 0
        report.EBITDA_4 = 0
        report.EBITDA_YTD = 0
        report.EBITDA_FY = 0
        report.EBITDA_plan = 0
        
        report.cf_1 = 0
        report.cf_2 = 0
        report.cf_3 = 0
        report.cf_4 = 0
        report.cf_YTD = 0
        report.cf_FY = 0
        report.cf_plan = 0
        

    report.highlight1 = '[""]'
    # report.highlight2 = [' vfds',]
    report.operation = []
    report.strategy = []
    report.customer_gained = []

    report.explain = []

    request.dbsession.add(report)
    

@view_config(route_name = 'save_report', request_method = 'POST', permission = 'save_report')
def save_report(request, form_data, report):
    for key, val in form_data.items():
        if key == 'year' and len(str(val))==4:
            report.year = val
            
        if key == 'company' and val in ['L&P', 'MGR']:
            report.company = val

        if key == 'quarter' and val in (1,2,3,4):
            report.quarter = val
        
        if key == 'highlights':
            report.highlight1 = val['highlight_1']
            report.highlight2 = val['highlight_2']
            report.highlight3 = val['highlight_3']
            report.highlight4 = val['highlight_4']
            report.highlight5 = val['highlight_5']
            report.highlight6 = val['highlight_6']
            report.highlight7 = val['highlight_7']
            # report.highlight8 = val['highlight_8']
            # report.highlight9 = val['highlight_9']

        if key == 'operations':
            report.operation1 = val['operation_1']
            report.operation2 = val['operation_2']
            report.operation3 = val['operation_3']
            report.operation4 = val['operation_4']
            # report.operation5 = val['operation_5']
            # report.operation6 = val['operation_6']
            # report.operation7 = val['operation_7']
            # report.operation8 = val['operation_8']
            # report.operation9 = val['operation_9']

        if key == 'strategies':
            report.strategy1 = val['strategy_1']
            report.strategy2 = val['strategy_2']
            report.strategy3 = val['strategy_3']
            report.strategy4 = val['strategy_4']
            # report.strategy5 = val['strategy_5']
            # report.strategy6 = val['strategy_6']
            # report.strategy7 = val['strategy_7']
            # report.strategy8 = val['strategy_8']
            # report.strategy9 = val['strategy_9']

        if key == 'customers':
            report.customer_gained1 = val['customer_gained_1']
            report.customer_gained2 = val['customer_gained_2']
            report.customer_gained3 = val['customer_gained_3']
            report.customer_gained4 = val['customer_gained_4']
            # report.customer_gained5 = val['customer_gained_5']
            # report.customer_gained6 = val['customer_gained_6']
            # report.customer_gained7 = val['customer_gained_7']
            # report.customer_gained8 = val['customer_gained_8']
            # report.customer_gained9 = val['customer_gained_9']

        if key == 'orders':
            report.order1 = val['order_1']
            report.order2 = val['order_2']
            report.order3 = val['order_3']
            report.order4 = val['order_4']
            # report.order5 = val['order_5']
            # report.order6 = val['order_6']
            # report.order7 = val['order_7']
            # report.order8 = val['order_8']
            # report.order9 = val['order_9']

        if key == 'revenue':
            report.revenue_1 = val['revenue_1']
            report.revenue_2 = val['revenue_2']
            report.revenue_3 = val['revenue_3']
            report.revenue_4 = val['revenue_4']
            report.revenue_YTD = val['revenue_YTD']
            report.revenue_FY = val['revenue_FY']
            report.revenue_plan = val['revenue_plan']

        if key == 'profit':
            report.profit_1 = val['profit_1']
            report.profit_2 = val['profit_2']
            report.profit_3 = val['profit_3']
            report.profit_4 = val['profit_4']
            report.profit_YTD = val['profit_YTD']
            report.profit_FY = val['profit_FY']
            report.profit_plan = val['profit_plan']

        if key == 'EBITDA':
            report.EBITDA_1 = val['EBITDA_1']
            report.EBITDA_2 = val['EBITDA_2']
            report.EBITDA_3 = val['EBITDA_3']
            report.EBITDA_4 = val['EBITDA_4']
            report.EBITDA_YTD = val['EBITDA_YTD']
            report.EBITDA_FY = val['EBITDA_FY']
            report.EBITDA_plan = val['EBITDA_plan']

        if key == 'cf':
            report.cf_1 = val['cf_1']
            report.cf_2 = val['cf_2']
            report.cf_3 = val['cf_3']
            report.cf_4 = val['cf_4']
            report.cf_YTD = val['cf_YTD']
            report.cf_FY = val['cf_FY']
            report.cf_plan = val['cf_plan']
    report.last_updated = datetime.now()
    request.dbsession.add(report)


@view_config(route_name = 'delete_report', request_method = 'POST', permission = 'delete_report')
def delete_report(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    report = request.dbsession.query(Report).filter(Report.id == id_).first()
    kpis = request.dbsession.query(KPI).filter(KPI.report_id == id_)
    
    filepath = os.getcwd() + '/gemstone2/static/pdfs/'
        
    if report.filename:
        try:
            os.remove(filepath + report.unique_filename)
            remove_files(filepath+'cache/', report)
        except:
            pass
    
    kpis.delete()
    request.dbsession.delete(report)


@view_config(route_name = 'create_pdf', request_method = 'POST', permission = 'create_pdf')
def create_pdf(request, file_name, data):
    # pdf = SimpleDocTemplate(file_name, pagesize = letter)
    pdf = canvas.Canvas(file_name)

    #drawing on coordinates
    my_ruler(pdf)

    #setting document title
    pdf.setTitle(file_name)

    #inserting title
    pdf.drawCentredString(300, 800, "GEMSTONEII")

    ### RECTANGLES ###
    # Company
    pdf.rect(105, 760, 130, 20, stroke=1, fill=1) 
    
    # Quarter & Year
    pdf.rect(375, 760, 130, 20, stroke=1, fill=1)
    
    # Industry and Business Major Highlights,
    pdf.rect(50, 575, 500, 170, stroke = 1, fill = 1) 

    # Operations Update
    pdf.rect(50, 445, 245, 125, stroke = 1, fill = 1)
   
    # Strategic Initiative Update
    pdf.rect(300, 445, 250, 125, stroke = 1, fill = 1)

    # New Customers Gained During Quarter
    pdf.rect(50, 315, 245, 125, stroke = 1, fill = 1)

    # Major Orders Received During Quarter
    pdf.rect(300, 315, 250, 125, stroke = 1, fill = 1)

    ### Table : "Finicial Performance VS. Plan" ###
    
    pdf.save()
    
    
    
    
    
    
    
    
    
    # comp = request.POST.get('company')
    # year = request.POST.get('year')

    # report = Report()
    # report.company = comp
    # report.quarter = 1
    # report.year = int(year)
    # last_updated = datetime.now()

    # request.dbsession.add(report)
    # return HTTPFound(location=request.route_url('home'))


@view_config(route_name = 'publish_report', permission = 'publish')
def publish_report(request):
    report = None
    try:
        if request.params.get('id') is not None:
            report = request.dbsession.query(Report).get(request.params['id'])
    except DBAPIError as ex:
        log.exception(ex)
        return Response(db_err_msg, content_type='text/plain', status=500)


    if report:
        completed = request.params.get('checked') == 'true'
        report.published = completed
        if completed:
            report.last_updated = datetime.now()
        request.dbsession.add(report)
    else:
        return Response('Not Found', content_type='text/plain', status=404)

    return Response('OK', content_type='text/plain', status=200)


@view_config(route_name = 'edit_report', renderer='../templates/report_edit.mako', permission = 'edit_report')
def edit_report(request):
    
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    report = request.dbsession.query(Report).filter(Report.id == id_).first()
    if report is None:
        raise HTTPForbidden
    
    # x = report.highlight1
    # f = ast.literal_eval(report.highlight1)

    kpis_query = request.dbsession.query(KPI).filter(KPI.report_id == 987654321)
    working_kpis = kpis_query.distinct(KPI.kpi_name)
    
    distinct_kpis = request.dbsession.query(KPI).distinct(KPI.kpi_name)

    db_kpis = request.dbsession.query(KPI).filter(KPI.report_id == id_)

    db_kpis_data = {}

    for kpi in db_kpis:
        db_kpis_data[kpi.kpi_name] = [kpi.value, kpi.target]
    
    current = dic_of_data(report)
    for key, val in current.items():
        if val == 'None':
            val = None    
    ### FORM SCHEMA SETUP ###
    #CSRF Schema
    class CSRFSchema(colander.MappingSchema): 
        csrf_token = colander.SchemaNode(colander.String(), default=deferred_csrf_default, widget=deform.widget.HiddenWidget())
    
    #Highlight Schema
    class Highlight(colander.Schema):
        highlight_1 = colander.SchemaNode(colander.String(), description = '1', default = current['highlight1'], missing = current['highlight1'])
        highlight_2 = colander.SchemaNode(colander.String(), description = '2', default = current['highlight2'], missing = current['highlight2'])
        highlight_3 = colander.SchemaNode(colander.String(), description = '3', default = current['highlight3'], missing = current['highlight3'])
        highlight_4 = colander.SchemaNode(colander.String(), description = '4', default = current['highlight4'], missing = current['highlight4'])
        highlight_5 = colander.SchemaNode(colander.String(), description = '5', default = current['highlight5'], missing = current['highlight5'])
        highlight_6 = colander.SchemaNode(colander.String(), description = "6", default = current['highlight6'], missing = current['highlight6'])
        highlight_7 = colander.SchemaNode(colander.String(), description = '7', default = current['highlight7'], missing = current['highlight7'])
        # highlight_8 = colander.SchemaNode(colander.String(), description = '8', default = current['highlight8'], missing = current['highlight8'])
        # highlight_9 = colander.SchemaNode(colander.String(), description = '9', default = current['highlight9'], missing = current['highlight9'])
        

    #Operations Schema
    class Operation(colander.Schema):
        operation_1 = colander.SchemaNode(colander.String(), description = '1', default = current['operation1'], missing = current['operation1'])
        operation_2 = colander.SchemaNode(colander.String(), description = '2', default = current['operation2'], missing = current['operation2'])
        operation_3 = colander.SchemaNode(colander.String(), description = '3', default = current['operation3'], missing = current['operation3'])
        operation_4 = colander.SchemaNode(colander.String(), description = '4', default = current['operation4'], missing = current['operation4'])
        # operation_5 = colander.SchemaNode(colander.String(), description = '5', default = current['operation5'], missing = current['operation5'])
        # operation_6 = colander.SchemaNode(colander.String(), description = "6", default = current['operation6'], missing = current['operation6'])
        # operation_7 = colander.SchemaNode(colander.String(), description = '7', default = current['operation7'], missing = current['operation7'])
        # operation_8 = colander.SchemaNode(colander.String(), description = '8', default = current['operation8'], missing = current['operation8'])
        # operation_9 = colander.SchemaNode(colander.String(), description = '9', default = current['operation9'], missing = current['operation9'])


    #Strategy Schema
    class Strategy(colander.Schema):
        strategy_1 = colander.SchemaNode(colander.String(), description = '1', default = current['strategy1'], missing = current['strategy1'])
        strategy_2 = colander.SchemaNode(colander.String(), description = '2', default = current['strategy2'], missing = current['strategy2'])
        strategy_3 = colander.SchemaNode(colander.String(), description = '3', default = current['strategy3'], missing = current['strategy3'])
        strategy_4 = colander.SchemaNode(colander.String(), description = '4', default = current['strategy4'], missing = current['strategy4'])
        # strategy_5 = colander.SchemaNode(colander.String(), description = '5', default = current['strategy5'], missing = current['strategy5'])
        # strategy_6 = colander.SchemaNode(colander.String(), description = "6", default = current['strategy6'], missing = current['strategy6'])
        # strategy_7 = colander.SchemaNode(colander.String(), description = '7', default = current['strategy7'], missing = current['strategy7'])
        # strategy_8 = colander.SchemaNode(colander.String(), description = '8', default = current['strategy8'], missing = current['strategy8'])
        # strategy_9 = colander.SchemaNode(colander.String(), description = '9', default = current['strategy9'], missing = current['strategy9'])


    #Customer_gained Schema
    class Customer(colander.Schema):
        customer_gained_1 = colander.SchemaNode(colander.String(), description = '1', default = current['customer_gained1'], missing = current['customer_gained1'])
        customer_gained_2 = colander.SchemaNode(colander.String(), description = '2', default = current['customer_gained2'], missing = current['customer_gained2'])
        customer_gained_3 = colander.SchemaNode(colander.String(), description = '3', default = current['customer_gained3'], missing = current['customer_gained3'])
        customer_gained_4 = colander.SchemaNode(colander.String(), description = '4', default = current['customer_gained4'], missing = current['customer_gained4'])
        # customer_gained_5 = colander.SchemaNode(colander.String(), description = '5', default = current['customer_gained5'], missing = current['customer_gained5'])
        # customer_gained_6 = colander.SchemaNode(colander.String(), description = "6", default = current['customer_gained6'], missing = current['customer_gained6'])
        # customer_gained_7 = colander.SchemaNode(colander.String(), description = '7', default = current['customer_gained7'], missing = current['customer_gained7'])
        # customer_gained_8 = colander.SchemaNode(colander.String(), description = '8', default = current['customer_gained8'], missing = current['customer_gained8'])
        # customer_gained_9 = colander.SchemaNode(colander.String(), description = '9', default = current['customer_gained9'], missing = current['customer_gained9'])


    #Orders Schema
    class Order(colander.Schema):
        order_1 = colander.SchemaNode(colander.String(), description = '1', default = current['order1'], missing = current['order1'])
        order_2 = colander.SchemaNode(colander.String(), description = '2', default = current['order2'], missing = current['order2'])
        order_3 = colander.SchemaNode(colander.String(), description = '3', default = current['order3'], missing = current['order3'])
        order_4 = colander.SchemaNode(colander.String(), description = '4', default = current['order4'], missing = current['order4'])
        # order_5 = colander.SchemaNode(colander.String(), description = '5', default = current['order5'], missing = current['order5'])
        # order_6 = colander.SchemaNode(colander.String(), description = "6", default = current['order6'], missing = current['order6'])
        # order_7 = colander.SchemaNode(colander.String(), description = '7', default = current['order7'], missing = current['order7'])
        # order_8 = colander.SchemaNode(colander.String(), description = '8', default = current['order8'], missing = current['order8'])
        # order_9 = colander.SchemaNode(colander.String(), description = '9', default = current['order9'], missing = current['order9'])


    #Revenue Schema
    class RevenueSchema(colander.Schema):
        revenue_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = current['revenue_1'], missing = current['revenue_1'])
        revenue_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = current['revenue_2'], missing = current['revenue_2'])
        revenue_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = current['revenue_3'], missing = current['revenue_3'])
        revenue_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = current['revenue_4'], missing = current['revenue_4'])
        revenue_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['revenue_YTD'], missing = current['revenue_YTD'])
        revenue_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['revenue_FY'], missing = current['revenue_FY'])
        revenue_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = current['revenue_plan'], missing = current['revenue_plan'])


    #Profit Schema
    class ProfitSchema(colander.Schema):
        profit_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = current['profit_1'], missing = current['profit_1'])
        profit_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = current['profit_2'], missing = current['profit_2'])
        profit_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = current['profit_3'], missing = current['profit_3'])
        profit_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = current['profit_4'], missing = current['profit_4'])
        profit_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['profit_YTD'], missing = current['profit_YTD'])
        profit_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['profit_FY'], missing = current['profit_FY'])
        profit_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = current['profit_plan'], missing = current['profit_plan'])


    #EBITDA Schema
    class EBITDASchema(colander.Schema):
        EBITDA_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = current['EBITDA_1'], missing = current['EBITDA_1'])
        EBITDA_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = current['EBITDA_2'], missing = current['EBITDA_2'])
        EBITDA_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = current['EBITDA_3'], missing = current['EBITDA_3'])
        EBITDA_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = current['EBITDA_4'], missing = current['EBITDA_4'])
        EBITDA_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['EBITDA_YTD'], missing = current['EBITDA_YTD'])
        EBITDA_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['EBITDA_FY'], missing = current['EBITDA_FY'])
        EBITDA_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = current['EBITDA_plan'], missing = current['EBITDA_plan'])


    #cf Schema
    class CFSchema(colander.Schema):
        cf_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = current['cf_1'], missing = current['cf_1'])
        cf_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = current['cf_2'], missing = current['cf_2'])
        cf_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = current['cf_3'], missing = current['cf_3'])
        cf_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = current['cf_4'], missing = current['cf_4'])
        cf_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['cf_YTD'], missing = current['cf_YTD'])
        cf_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['cf_FY'], missing = current['cf_FY'])
        cf_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = current['cf_plan'], missing = current['cf_plan'])


    # Explain Schema
    class Explaination(colander.Schema):
        explain = colander.SchemaNode(colander.String(), missing = colander.drop)

    class Explainations(colander.SequenceSchema):
        explanation = Explaination()


    #Form schema
    class MySchema(CSRFSchema):
        company = colander.SchemaNode(colander.String(), 
            validator = colander.Length(min = 1, max = 24), 
            widget = deform.widget.SelectWidget(values=((('MGR', 'MGR Plastics'), ('L&P', 'Label & Pack'),))),
            default = current['company'])
        quarter = colander.SchemaNode(colander.Integer(), 
            validator = colander.Range(min = 1, max = 4),
            widget = deform.widget.SelectWidget(values=(((1,1),(2,2),(3,3),(4,4),))),
            default = current['quarter'])
        year = colander.SchemaNode(colander.Integer(), default = current['year'], missing = current['year'])

        # highlights = HighlightsSchema(validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
        # operations = OperationSchema(validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
        # strategies = StrategySchema(validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
        # customers = Customers(validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
        # orders = Orders(validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10)) 
        
        highlights = Highlight(title = 'Industry & Business Major Highlights')
        operations = Operation(title = 'Operations Update')
        strategies = Strategy(title = 'Strategic Initiative Update')
        customers = Customer(title = 'New Customers Gained During Quarter')
        orders = Order(title = 'Major Orders Received During Quarter')

        revenue = RevenueSchema()
        profit = ProfitSchema()
        EBITDA = EBITDASchema(title = 'EBITDA')
        cf = CFSchema(title = 'CF')

        # explain = Explainations(
        #     validator = colander.Length(min = 1, max = 10), 
        #     widget=deform.widget.SequenceWidget(min_len=1, max_len=10)
            
        #     )
    ### FORM SCHEMA SETUP FINISHED ###
    
    schema = MySchema().bind(request=request)
    
    kpi_schema_list = []
    kpis_used_list = []
    for distinct_kpi in distinct_kpis:

        if distinct_kpi.kpi_name in db_kpis_data:
            
            class KPISchema(colander.MappingSchema):
                kpi_value = colander.SchemaNode(colander.Integer(),
                description = 'Value',
                default = db_kpis_data[distinct_kpi.kpi_name][0],
                missing = db_kpis_data[distinct_kpi.kpi_name][0])
            
                kpi_target = colander.SchemaNode(colander.Integer(),
                description = 'Target', 
                default = db_kpis_data[distinct_kpi.kpi_name][1],
                missing = db_kpis_data[distinct_kpi.kpi_name][1])

            kpi_schema_list.append(KPISchema(name = distinct_kpi.kpi_name))
            kpis_used_list.append(distinct_kpi.kpi_name)
        
    for new_kpi in working_kpis:
        if new_kpi.kpi_name not in kpis_used_list:
            class KPISchema(colander.MappingSchema):
                kpi_value = colander.SchemaNode(colander.Integer(),
                description = 'Value',
                default = 0,
                missing = 0)
            
                kpi_target = colander.SchemaNode(colander.Integer(),
                description = 'Target', 
                default = 0,
                missing = 0)
            
            kpi_schema_list.append(KPISchema(name = new_kpi.kpi_name))
    
    kpischemas = colander.SchemaNode(colander.Mapping(), name = 'kpis', title = 'KPIS')
    
    for item in kpi_schema_list:
        kpischemas.add(item)
    
    schema.add(kpischemas)
        
    #fileupload
    # class MemoryTmpStore(dict):
    #     """ Instances of this class implement the
    #     :class:`deform.interfaces.FileUploadTempStore` interface"""

    #     def preview_url(self, uid):
    #         return None
    

    # tmpstore = MemoryTmpStore()        
    # schema.add(colander.SchemaNode(
    #     deform.FileData(),
    #     widget = deform.widget.FileUploadWidget(tmpstore),
    #     name = 'upload',
    #     missing = None
    #     ))
    

    myform = deform.Form(schema, buttons=('save', 'pdf', 'delete'))
    form = myform.render()


    if 'save' in request.POST:
        control = request.params.items()

        try:
            form_data = myform.validate(control)
            
        except deform.exception.ValidationFailure as e:
            return {
                'report' : report,
                'id' : id_,
                'form' : e.render(),
                }
        save_report(request, form_data, report)
        
        kpi_form_data = None
        if 'kpis' in form_data.keys():
            kpi_form_data = form_data['kpis']

        for key, val in form_data['kpis'].items():
            
            try:
                db_kpi = request.dbsession.query(KPI).filter(KPI.kpi_name == key, KPI.report_id == id_).first()
            except:
                pass
            if db_kpi is not None:
                db_kpi.value = val['kpi_value']
                db_kpi.target = val['kpi_target']
                request.dbsession.add(db_kpi)
            else:
                kpi = KPI()
                kpi.kpi_name = key
                kpi.value = val['kpi_value']
                kpi.target = val['kpi_target']
                kpi.report_id = id_

                request.dbsession.add(kpi)
            
            
                    

        return HTTPFound(location=request.route_url('report_list'))
        
    elif 'delete' in request.POST:
        delete_report(request)
        return HTTPFound(location = request.route_url('report_list'))
    
    if 'pdf' in request.POST:
        control = request.params.items()

        try:
            form_data = myform.validate(control)
        except deform.exception.ValidationFailure as e:
            return{
                'report' : report,
                'id' : id_,
                'form' : e.render(),
            }

        # file_path = os.getcwd() + '\\gemstone2\\static\\pdfs\\'
        # file_name = "{0}_{1}_{2}.pdf".format(form_data['company'], form_data['quarter'], form_data['year'])
        # file_ = file_path + file_name
        
        # create_pdf(request, file_, form_data)
        
        
        # create_pdf()
        save_report(request, form_data, report)
        
        kpi_form_data = None
        if 'kpis' in form_data.keys():
            kpi_form_data = form_data['kpis']

        for key, val in form_data['kpis'].items():
            
            try:
                db_kpi = request.dbsession.query(KPI).filter(KPI.kpi_name == key, KPI.report_id == id_).first()
            except:
                pass
            if db_kpi is not None:
                db_kpi.value = val['kpi_value']
                db_kpi.target = val['kpi_target']
                request.dbsession.add(db_kpi)
            else:
                kpi = KPI()
                kpi.kpi_name = key
                kpi.value = val['kpi_value']
                kpi.target = val['kpi_target']
                kpi.report_id = id_

                request.dbsession.add(kpi)
        return HTTPFound(location = request.route_url('pdf_tester', id=id_))

    return {
        'report' : report,
        'id' : id_,
        'form' : form,
        'db_kpis' : db_kpis,
        # 'desc' : current['description'],
        # 'img' : img
    }


@view_config(route_name = 'pdf_tester', renderer='../templates/pdf_tester.mako', permission = 'report_view')
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
    
    data = {
        'id_' : report.id,
        'year' : report.year,
        'company' : report.company,
        'quarter' : report.quarter,

        'highlights' : [],
        'operations' : [],
        'strategies' : [],
        'customers_gained' : [],
        'order' : [],
        'revenue' : []

    }
    
    return {
        'report' : report,
        'yearly_reports' : yearly_reports,
        'page_title' : 'Gemstone II',
        'project' : 'Gemstone II',
        'kpis' : kpis,
    }


db_err_msg = 'Unable to load data'