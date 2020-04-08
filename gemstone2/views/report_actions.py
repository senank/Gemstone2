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

        if field == 'customers':
            customers = field_save(data)
            report.customer_gained = str(customers)

        if field == 'orders':
            orders = field_save(data)
            report.order = str(orders)

        if field == 'revenue':
            report.revenue_1 = data['revenue_1']
            report.revenue_2 = data['revenue_2']
            report.revenue_3 = data['revenue_3']
            report.revenue_4 = data['revenue_4']
            report.revenue_YTD = data['revenue_YTD']
            report.revenue_FY  = data['revenue_FY']
            report.revenue_plan = data['revenue_plan']

        if field == 'profit':
            report.profit_1 = data['profit_1']
            report.profit_2 = data['profit_2']
            report.profit_3 = data['profit_3']
            report.profit_4 = data['profit_4']
            report.profit_YTD = data['profit_YTD']
            report.profit_FY = data['profit_FY']
            report.profit_plan = data['profit_plan']

        if field == 'EBITDA':
            report.EBITDA_1 = data['EBITDA_1']
            report.EBITDA_2 = data['EBITDA_2']
            report.EBITDA_3 = data['EBITDA_3']
            report.EBITDA_4 = data['EBITDA_4']
            report.EBITDA_YTD = data['EBITDA_YTD']
            report.EBITDA_FY = data['EBITDA_FY']
            report.EBITDA_plan = data['EBITDA_plan']

        if field == 'cf':
            report.cf_1 = data['cf_1']
            report.cf_2 = data['cf_2']
            report.cf_3 = data['cf_3']
            report.cf_4 = data['cf_4']
            report.cf_YTD = data['cf_YTD']
            report.cf_FY = data['cf_FY']
            report.cf_plan = data['cf_plan']
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
            os.remove(filepath + report.unique_filename)
            remove_files(filepath+'cache/', report)
        except:
            pass
    
    kpis.delete()
    request.dbsession.delete(report)
    return HTTPFound(location = request.route_url('report_list'))


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
        highlight = colander.SchemaNode(colander.String(), missing = colander.drop)

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
        operation = colander.SchemaNode(colander.String(), missing = colander.drop)

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
        strategy = colander.SchemaNode(colander.String(), missing = colander.drop)

    class Strategys_New_Schema(colander.SequenceSchema):
        strategy = Strategy_New()

    strategys = ast.literal_eval(report.strategy)
    strategy_count = 1
    strategy_schema_list = []
    strategyschemas = colander.SchemaNode(colander.Mapping(), name = 'strategys', 
                        title = 'Strategic Initiative Update',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for strat in strategys:
        strategyschemas.add(colander.SchemaNode(colander.String(),
            name = str(strategy_count),
            default = strat,
            missing = colander.drop))
        strategy_count += 1
    
    strategyschemas.add(Strategys_New_Schema(name = 'new', title = ''))


    #Customer_gained Schema
    class Customer_gained_New(colander.Schema):
        customer_gained = colander.SchemaNode(colander.String(), missing = colander.drop)

    class Customer_gaineds_New_Schema(colander.SequenceSchema):
        customer_gained = Customer_gained_New()

    customer_gaineds = ast.literal_eval(report.customer_gained)
    customer_gained_count = 1
    customer_gained_schema_list = []
    customer_gainedschemas = colander.SchemaNode(colander.Mapping(), name = 'customer_gaineds', 
                        title = 'New Customers Gained During Quarter',
                        widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False))

    for customer in customer_gaineds:
        customer_gainedschemas.add(colander.SchemaNode(colander.String(),
            name = str(customer_gained_count),
            default = customer,
            missing = colander.drop))
        customer_gained_count += 1
    
    customer_gainedschemas.add(Customer_gaineds_New_Schema(name = 'new', title = ''))

    #Orders Schema
    class Order_New(colander.Schema):
        order = colander.SchemaNode(colander.String(), missing = colander.drop)

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
    class Explain_New(colander.Schema):
        explain = colander.SchemaNode(colander.String(), missing = colander.drop)

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
        
        # highlights = Highlight(title = 'Industry & Business Major Highlights')
        # operations = Operation(title = 'Operations Update')
        # strategies = Strategy(title = 'Strategic Initiative Update')
        # customers = Customer(title = 'New Customers Gained During Quarter')
        # orders = Order(title = 'Major Orders Received During Quarter')

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
    
    kpischemas = colander.SchemaNode(colander.Mapping(), name = 'kpis', title = 'KPIS',
    widget=deform.widget.MappingWidget(template="mapping_accordion", open=False))
    
    for item in kpi_schema_list:
        kpischemas.add(item)
    
    schema.add(highlightschemas)
    schema.add(operationschemas)
    schema.add(strategyschemas)
    schema.add(customer_gainedschemas)
    schema.add(orderschemas)
    schema.add(RevenueSchema(name = 'revenue', widget=deform.widget.MappingWidget(
                        template="mapping_accordion",
                        open=False)))
    schema.add(ProfitSchema(name = 'profit', widget=deform.widget.MappingWidget(
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
    

    myform = deform.Form(schema, buttons=('save', 'pdf',))
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