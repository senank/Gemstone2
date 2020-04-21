from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import get_csrf_token
import pyramid.events

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models import Report, KPI
from .pdf_actions import create_pdf

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

def str_to_num(string):
    val = ''
    for i in string:
        if i.isdigit() == True or (i == '.' and '.' not in val):
            val = val + i
    int_val = float(val)
    return int_val

def str_to_num_kpi(string):
    val = ''
    for i in string:
        if (i.isdigit() == True) or (i == '.' and '.' not in val) or (i in ['<', '>', '=']):
            val = val + i
    return val

def dic_of_data(report):
    current = {
        'company' : report.company,
        'quarter' : report.quarter,
        'year' : report.year,

        'highlight' : ast.literal_eval(report.highlight),
        'operation' : ast.literal_eval(report.operation),
        'strategy' : ast.literal_eval(report.strategy),
        'customer' : ast.literal_eval(report.customer_gained),
        'order' : ast.literal_eval(report.order),

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

        'explain' : ast.literal_eval(report.explain),

        'filename' : report.filename,
        'unique_filename' : report.unique_filename
    }
    return current

def remove_files(path_name, item_name):
    for dirs, subdirs, files in os.walk(path_name):
        try:
            os.remove('{}/{}'.format(dirs, item_name.filename))
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
    report.year = request.params.get('year')
    report.last_updated = datetime.now()
    
    if request.params.get('quarter') != '1':
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

        report.revenue_4 = '0'
        report.revenue_YTD = 0
        report.revenue_FY = '0%'

        report.profit_4 = '0'
        report.profit_YTD = 0
        report.profit_FY = '0%'

        report.EBITDA_4 = '0'
        report.EBITDA_YTD = 0
        report.EBITDA_FY = '0%'

        report.cf_4 = '0'
        report.cf_YTD = 0
        report.cf_FY = '0%'

    else:
        report.revenue_1 = '0'
        report.revenue_2 = '0'
        report.revenue_3 = '0'
        report.revenue_4 = '0'
        report.revenue_YTD = 0
        report.revenue_FY = '0%'
        report.revenue_plan = '0'

        report.profit_1 = '0'
        report.profit_2 = '0'
        report.profit_3 = '0'
        report.profit_4 = '0'
        report.profit_YTD = 0
        report.profit_FY = '0%'
        report.profit_plan = '0'

        report.EBITDA_1 = '0'
        report.EBITDA_2= '0'
        report.EBITDA_3 = '0'
        report.EBITDA_4 = '0'
        report.EBITDA_YTD = 0
        report.EBITDA_FY = '0%'
        report.EBITDA_plan = '0'
        
        report.cf_1 = '0'
        report.cf_2 = '0'
        report.cf_3 = '0'
        report.cf_4 = '0'
        report.cf_YTD = 0
        report.cf_FY = '0%'
        report.cf_plan = '0'
        

    report.highlight = '[]'
    report.operation = '[]'
    report.strategy = '[]'
    report.customer_gained = "[]"
    report.order = "[]"

    report.explain = '[]'

    request.dbsession.add(report)
    
def field_save(fields):
    field_list = []
    new_list = None
    for key, val in fields.items():
        if key == 'new':
            new_list = val
        else:
            field_list.append(val)
    
    for new_field in new_list:
        for key, val in new_field.items():
            field_list.append(val)
    return field_list

@view_config(route_name = 'save_report', request_method = 'POST', permission = 'save_report')
def save_report(request, form_data, report):
    for field, data in form_data.items():
        if field == 'year' and len(str(data))==4:
            report.year = data
            
        if field == 'company' and data in ['L&P', 'MGR']:
            report.company = data

        if field == 'quarter' and data in (1,2,3,4):
            report.quarter = data
        
        if field == 'highlights':
            highlights = field_save(data)
            report.highlight = str(highlights)
                        

        if field == 'operations':
            operations = field_save(data)
            report.operation = str(operations)

        if field == 'strategies':
            strategies = field_save(data)
            report.strategy = str(strategies)

        if field == 'customer_gained':
            customers = field_save(data)
            report.customer_gained = str(customers)

        if field == 'orders':
            orders = field_save(data)
            report.order = str(orders)

        if field == 'revenue':
            r1 = str_to_num(data['revenue_1'])
            r2 = str_to_num(data['revenue_2'])
            r3 = str_to_num(data['revenue_3'])
            r4 = str_to_num(data['revenue_4'])
            r_plan = str_to_num(data['revenue_plan'])

            
            
            report.revenue_1 = "{:,.1f}".format(r1)
            report.revenue_2 = "{:,.1f}".format(r2)
            report.revenue_3 = "{:,.1f}".format(r3)
            report.revenue_4 = "{:,.1f}".format(r4)
            
            try:
                ytd = r1 + r2 + r3 + r4
                #adding commas
                r_ytd = "{:,.1f}".format(ytd)
                
                report.revenue_YTD = r_ytd
                report.revenue_plan = "{:,.1f}".format(r_plan)
                report.revenue_FY = '{:.1%}'.format(ytd/r_plan)
            except (TypeError, ValueError, ZeroDivisionError):
                report.revenue_FY  = 'N/A'
                

        if field == 'profit':
            p1 = str_to_num(data['profit_1'])
            p2 = str_to_num(data['profit_2'])
            p3 = str_to_num(data['profit_3'])
            p4 = str_to_num(data['profit_4'])
            p_plan = str_to_num(data['profit_plan'])

            report.profit_1 = "{:,.1f}".format(p1)
            report.profit_2 = "{:,.1f}".format(p2)
            report.profit_3 = "{:,.1f}".format(p3)
            report.profit_4 = "{:,.1f}".format(p4)
            
            try:
                ytd = p1 + p2 + p3 + p4
                #adding commas
                p_ytd = "{:,.1f}".format(ytd)

                report.profit_YTD = p_ytd
                report.profit_plan = "{:,.1f}".format(p_plan)
                report.profit_FY = '{:.1%}'.format(ytd/p_plan)
            except (TypeError, ValueError, ZeroDivisionError):
                report.profit_FY  = 'N/A'

        if field == 'EBITDA':
            e1 = str_to_num(data['EBITDA_1'])
            e2 = str_to_num(data['EBITDA_2'])
            e3 = str_to_num(data['EBITDA_3'])
            e4 = str_to_num(data['EBITDA_4'])
            e_plan = str_to_num(data['EBITDA_plan'])

            report.EBITDA_1 = "{:,.1f}".format(e1)
            report.EBITDA_2 = "{:,.1f}".format(e2)
            report.EBITDA_3 = "{:,.1f}".format(e3)
            report.EBITDA_4 = "{:,.1f}".format(e4)
            
            try:
                ytd = e1 + e2 + e3 + e4
                #adding commas
                e_ytd = "{:,.1f}".format(ytd)

                report.EBITDA_YTD = e_ytd
                report.EBITDA_plan = "{:,.1f}".format(e_plan)
                report.EBITDA_FY = '{:.1%}'.format(ytd/e_plan)
            except (TypeError, ValueError, ZeroDivisionError):
                report.EBITDA_FY  = 'N/A'

        if field == 'cf':
            c1 = str_to_num(data['cf_1'])
            c2 = str_to_num(data['cf_2'])
            c3 = str_to_num(data['cf_3'])
            c4 = str_to_num(data['cf_4'])
            c_plan = str_to_num(data['cf_plan'])

            report.cf_1 = "{:,.1f}".format(c1)
            report.cf_2 = "{:,.1f}".format(c2)
            report.cf_3 = "{:,.1f}".format(c3)
            report.cf_4 = "{:,.1f}".format(c4)
            try:
                ytd = c1 + c2 + c3 + c4
                #adding commas
                c_ytd = "{:,.1f}".format(ytd)

                report.cf_YTD = c_ytd
                report.cf_plan = "{:,.1f}".format(c_plan)
                report.cf_FY = '{:.1%}'.format(ytd/c_plan)
            except (TypeError, ValueError, ZeroDivisionError):
                report.cf_FY  = 'N/A'

        if field == 'explains':
            explain = field_save(data)
            report.explain = str(explain)

    report.last_updated = datetime.now()
    request.dbsession.add(report)



@view_config(route_name = 'delete_report', permission = 'delete_report')
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
            os.remove(filepath + report.filename)
            remove_files(filepath+'cache/', report)
        except:
            pass
    
    kpis.delete()
    request.dbsession.delete(report)
    return HTTPFound(location = request.route_url('report_list'))


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
    
    # Highlight Schema
    class Highlight_New(colander.Schema):
        highlight = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Highlights_New_Schema(colander.SequenceSchema):
        highlight = Highlight_New()

    highlights = ast.literal_eval(report.highlight)
    highlight_count = 1
    highlight_schema_list = []
    highlightschemas = colander.SchemaNode(colander.Mapping(), name = 'highlights', 
                        title = 'Industry and Business Major Highlights',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for high in highlights:
        highlightschemas.add(colander.SchemaNode(colander.String(),
            name = str(highlight_count),
            default = high,
            missing = colander.drop))
        highlight_count += 1
    
    highlightschemas.add(Highlights_New_Schema(name = 'new', title = ''))

    #Operations Schema
    class Operation_New(colander.Schema):
        operation = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Operations_New_Schema(colander.SequenceSchema):
        operation = Operation_New()

    operations = ast.literal_eval(report.operation)
    operation_count = 1
    operation_schema_list = []
    operationschemas = colander.SchemaNode(colander.Mapping(), name = 'operations', 
                        title = 'Operations Update',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for op in operations:
        operationschemas.add(colander.SchemaNode(colander.String(),
            name = str(operation_count),
            default = op,
            missing = colander.drop))
        operation_count += 1
    
    operationschemas.add(Operations_New_Schema(name = 'new', title = ''))

    #Strategy Schema
    class Strategy_New(colander.Schema):
        strategy = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Strategies_New_Schema(colander.SequenceSchema):
        strategy = Strategy_New()

    strategies = ast.literal_eval(report.strategy)
    strategy_count = 1
    strategy_schema_list = []
    strategieschemas = colander.SchemaNode(colander.Mapping(), name = 'strategies', 
                        title = 'Strategic Initiative Update',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for strat in strategies:
        strategieschemas.add(colander.SchemaNode(colander.String(),
            name = str(strategy_count),
            default = strat,
            missing = colander.drop))
        strategy_count += 1
    
    strategieschemas.add(Strategies_New_Schema(name = 'new', title = ''))


    #Customer_gained Schema
    class Customer_gained_New(colander.Schema):
        customer_gained = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Customer_gained_New_Schema(colander.SequenceSchema):
        customer_gained = Customer_gained_New()

    customer_gained = ast.literal_eval(report.customer_gained)
    customer_gained_count = 1
    customer_gained_schema_list = []
    customer_gainedschemas = colander.SchemaNode(colander.Mapping(), name = 'customer_gained', 
                        title = 'New Customers Gained During Quarter',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for customer in customer_gained:
        customer_gainedschemas.add(colander.SchemaNode(colander.String(),
            name = str(customer_gained_count),
            default = customer,
            missing = colander.drop))
        customer_gained_count += 1
    
    customer_gainedschemas.add(Customer_gained_New_Schema(name = 'new', title = ''))

    #Orders Schema
    class Order_New(colander.Schema):
        order = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Orders_New_Schema(colander.SequenceSchema):
        order = Order_New()

    orders = ast.literal_eval(report.order)
    order_count = 1
    order_schema_list = []
    orderschemas = colander.SchemaNode(colander.Mapping(), name = 'orders',
                        title = 'Major Orders Received During Quarter',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for x in orders:
        orderschemas.add(colander.SchemaNode(colander.String(),
            name = str(order_count),
            default = x,
            missing = colander.drop))
        order_count += 1
    
    orderschemas.add(Orders_New_Schema(name = 'new', title = ''))

    #Revenue Schema
    class RevenueSchema(colander.Schema):
        revenue_1 = colander.SchemaNode(colander.String(), description = 'Q1', default = current['revenue_1'], missing = '0', title = '')
        revenue_2 = colander.SchemaNode(colander.String(), description = 'Q2', default = current['revenue_2'], missing = '0', title = '')
        revenue_3 = colander.SchemaNode(colander.String(), description = 'Q3', default = current['revenue_3'], missing = '0', title = '')
        revenue_4 = colander.SchemaNode(colander.String(), description = 'Q4', default = current['revenue_4'], missing = '0', title = '')
        # revenue_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['revenue_YTD'], missing = current['revenue_YTD'], title = '')
        # revenue_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['revenue_FY'], missing = current['revenue_FY'], title = '')
        revenue_plan = colander.SchemaNode(colander.String(), description = 'FY Plan', default = current['revenue_plan'], missing = current['revenue_plan'], title = '')


    #Profit Schema
    class ProfitSchema(colander.Schema):
        profit_1 = colander.SchemaNode(colander.String(), description = 'Q1', default = current['profit_1'], missing = '0', title = '')
        profit_2 = colander.SchemaNode(colander.String(), description = 'Q2', default = current['profit_2'], missing = '0', title = '')
        profit_3 = colander.SchemaNode(colander.String(), description = 'Q3', default = current['profit_3'], missing = '0', title = '')
        profit_4 = colander.SchemaNode(colander.String(), description = 'Q4', default = current['profit_4'], missing = '0', title = '')
        # profit_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['profit_YTD'], missing = current['profit_YTD'], title = '')
        # profit_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['profit_FY'], missing = current['profit_FY'], title = '')
        profit_plan = colander.SchemaNode(colander.String(), description = 'FY Plan', default = current['profit_plan'], missing = current['profit_plan'], title = '')


    #EBITDA Schema
    class EBITDASchema(colander.Schema):
        EBITDA_1 = colander.SchemaNode(colander.String(), description = 'Q1', default = current['EBITDA_1'], missing = '0', title = '')
        EBITDA_2 = colander.SchemaNode(colander.String(), description = 'Q2', default = current['EBITDA_2'], missing = '0', title = '')
        EBITDA_3 = colander.SchemaNode(colander.String(), description = 'Q3', default = current['EBITDA_3'], missing = '0', title = '')
        EBITDA_4 = colander.SchemaNode(colander.String(), description = 'Q4', default = current['EBITDA_4'], missing = '0', title = '')
        # EBITDA_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['EBITDA_YTD'], missing = current['EBITDA_YTD'], title = '')
        # EBITDA_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['EBITDA_FY'], missing = current['EBITDA_FY'], title = '')
        EBITDA_plan = colander.SchemaNode(colander.String(), description = 'FY Plan', default = current['EBITDA_plan'], missing = current['EBITDA_plan'], title = '')


    #cf Schema
    class CFSchema(colander.Schema):
        cf_1 = colander.SchemaNode(colander.String(), description = 'Q1', default = current['cf_1'], missing = '0', title = '')
        cf_2 = colander.SchemaNode(colander.String(), description = 'Q2', default = current['cf_2'], missing = '0', title = '')
        cf_3 = colander.SchemaNode(colander.String(), description = 'Q3', default = current['cf_3'], missing = '0', title = '')
        cf_4 = colander.SchemaNode(colander.String(), description = 'Q4', default = current['cf_4'], missing = '0', title = '')
        # cf_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = current['cf_YTD'], missing = current['cf_YTD'], title = '')
        # cf_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = current['cf_FY'], missing = current['cf_FY'], title = '')
        cf_plan = colander.SchemaNode(colander.String(), description = 'FY Plan', default = current['cf_plan'], missing = current['cf_plan'], title = '')


    # Explain Schema
    class Explain_New(colander.Schema):
        explain = colander.SchemaNode(colander.String(), missing = colander.drop, title = '')

    class Explains_New_Schema(colander.SequenceSchema):
        Explaination = Explain_New()

    explains = ast.literal_eval(report.explain)
    explain_count = 1
    explain_schema_list = []
    explainschemas = colander.SchemaNode(colander.Mapping(), name = 'explains', 
                        title = 'Variance Explanation & Mitigation',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for ex in explains:
        explainschemas.add(colander.SchemaNode(colander.String(),
            name = str(explain_count),
            default = ex,
            missing = colander.drop))
        explain_count += 1
    
    explainschemas.add(Explains_New_Schema(name = 'new', title = ''))


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
    
    schema = MySchema().bind(request=request)
    

    #KPI Schema
    kpi_schema_list = []
    kpis_used_list = []
    for distinct_kpi in distinct_kpis:

        if distinct_kpi.kpi_name in db_kpis_data:
            
            class KPISchema(colander.MappingSchema):
                kpi_value = colander.SchemaNode(colander.String(),
                description = 'Value',
                default = db_kpis_data[distinct_kpi.kpi_name][0],
                missing = db_kpis_data[distinct_kpi.kpi_name][0],
                title = '')
            
                kpi_target = colander.SchemaNode(colander.String(),
                description = 'Target', 
                default = db_kpis_data[distinct_kpi.kpi_name][1],
                missing = db_kpis_data[distinct_kpi.kpi_name][1],
                title = '')

            kpi_schema_list.append(KPISchema(name = distinct_kpi.kpi_name))
            kpis_used_list.append(distinct_kpi.kpi_name)
        
    for new_kpi in working_kpis:
        if new_kpi.kpi_name not in kpis_used_list:
            class KPISchema(colander.MappingSchema):
                kpi_value = colander.SchemaNode(colander.String(),
                description = 'Value',
                default = '0',
                missing = '0',
                title = '')
            
                kpi_target = colander.SchemaNode(colander.String(),
                description = 'Target', 
                default = '0',
                missing = '0',
                title = '')
            
            kpi_schema_list.append(KPISchema(name = new_kpi.kpi_name))
    
    kpischemas = colander.SchemaNode(colander.Mapping(), name = 'kpis', title = 'KPIS',
    widget=deform.widget.MappingWidget(template="mapping_accordion", open=False))
    
    for item in kpi_schema_list:
        kpischemas.add(item)
    
    schema.add(highlightschemas)
    schema.add(operationschemas)
    schema.add(strategieschemas)
    schema.add(customer_gainedschemas)
    schema.add(orderschemas)
    schema.add(RevenueSchema(name = 'revenue', widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False)))
    schema.add(ProfitSchema(name = 'profit', title = 'Gross Profit', widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False)))
    schema.add(EBITDASchema(name = 'EBITDA', title = 'EBITDA', widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False)))
    schema.add(CFSchema(name = 'cf', title = 'Cash Flow', widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False)))
    schema.add(explainschemas)
    schema.add(kpischemas)

        ### fileupload ###
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

    ### FORM SCHEMA SETUP FINISHED ###

    myform = deform.Form(schema, buttons=('save', 'pdf', 'back'))
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
                db_kpi = None
            if db_kpi is not None:

                k_v = str_to_num(val['kpi_value'])
                k_t = str_to_num(val['kpi_target'])
                k_t_ = str_to_num_kpi(val['kpi_target'])
                
                logic_symbol = ''
                for char in k_t_:
                    if (char in ['<', '>', '=']) and (logic_symbol == ''):
                        logic_symbol = char

                db_kpi.value = "{:,.1f}".format(k_v)
                db_kpi.target = "{} {:,.1f}".format(logic_symbol, k_t)
                request.dbsession.add(db_kpi)
            else:
                kpi = KPI()
                kpi.kpi_name = key

                k_v = str_to_num(val['kpi_value'])
                k_t = str_to_num(val['kpi_target'])
                k_t_ = str_to_num_kpi(val['kpi_target'])
                
                logic_symbol = ''
                for char in k_t_:
                    if (char in ['<', '>', '=']) and (logic_symbol == ''):
                        logic_symbol = char

                kpi.value = "{:,.1f}".format(k_v)
                kpi.target = "{} {:,.1f}".format(logic_symbol, k_t)
                kpi.report_id = id_

                request.dbsession.add(kpi)
        return HTTPFound(location=request.route_url('edit_report', id = id_))
        
    # elif 'delete' in request.POST:
    #     delete_report(request)
    #     return HTTPFound(location = request.route_url('report_list'))
    
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
        
        file_path = os.getcwd() + '/gemstone2/static/pdfs/'
        if report.filename:
            try:
                remove_files(filepath, report)
            except:
                pass
                
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
        


        ### making pdf document ###
        file_name = "{0}_Quarterly_{1}_{2}.pdf".format(form_data['company'], form_data['quarter'], form_data['year'])
        file_ = file_path + file_name
        
        #function
        func_data = dic_of_data(report)
        
        create_pdf(request, file_, func_data, db_kpis)
        report.filename = file_name
        request.dbsession.add(report)

        return HTTPFound(location=request.route_url('report_list')) 

    if 'back' in request.POST:
        return HTTPFound(location=request.route_url('report_list'))
        
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
    highlights = ast.literal_eval(report.highlight)
    operations = ast.literal_eval(report.operation)
    customer_gained = ast.literal_eval(report.customer_gained)
    strategy = ast.literal_eval(report.strategy)
    #reports in this year for company of object report
    # (will include all current quarters)
    yearly_reports = request.dbsession.query(Report).filter(Report.year == report.year, Report.company == report.company)
    
    data = {
        'id_' : report.id,
        'year' : report.year,
        'company' : report.company,
        'quarter' : report.quarter,

        'highlights' : highlights,
        'operations' : [],
        'strategies' : [],
        'customers_gained' : [],
        'order' : [],
        'revenue' : []

    }
    
    return {
        'highlights' : highlights,
        'operations' : operations,
        'customer_gained' : customer_gained,
        'strategy' : strategy,
        'orders' : ast.literal_eval(report.order),

        'report' : report,
        'yearly_reports' : yearly_reports,
        'page_title' : 'Gemstone II',
        'project' : 'Gemstone II',
        'kpis' : kpis,
    }


db_err_msg = 'Unable to load data'