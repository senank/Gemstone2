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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
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


# @view_config(route_name = 'create_pdf', request_method = 'POST', permission = 'create_pdf')
# def create_pdf(request, file_name, data):
#     if data['company'] == 'MGR':
#         data['company'] = 'MGR Plastics'
#     if data['company'] == 'L&P':
#         data['company'] == 'Label and Pack'
#     # pdf = SimpleDocTemplate(file_name, pagesize = letter)
#     pdf = canvas.Canvas(file_name)

#     #drawing on coordinates
#     my_ruler(pdf)

#     #setting document title
#     pdf.setTitle(file_name)

#     #inserting title
#     pdf.setFont("Helvetica", 16)
#     pdf.drawCentredString(300, 800, "GEMSTONEII")

#     ### RECTANGLES ###
#     # Company
#     pdf.setFont("Helvetica", 12)
#     pdf.rect(50, 750, 500, 35, stroke=1) 
#     pdf.drawString(60, 762, 'Company :')
#     pdf.drawString(125, 762, data['company'])
    
#     # Quarter & Year
#     pdf.drawString(375, 762, 'Quarter :')
#     pdf.drawString(430, 762, str(data['quarter']))

#     pdf.drawString(460, 762, 'Year :')
#     pdf.drawString(500, 762, str(data['year']))
    
#     # Industry and Business Major Highlights
#     pdf.rect(50, 575, 500, 170, stroke = 1, fill = 1) 

#     # Operations Update
#     pdf.rect(50, 445, 245, 125, stroke = 1, fill = 1)
   
#     # Strategic Initiative Update
#     pdf.rect(300, 445, 250, 125, stroke = 1, fill = 1)

#     # New Customers Gained During Quarter
#     pdf.rect(50, 315, 245, 125, stroke = 1, fill = 1)

#     # Major Orders Received During Quarter
#     pdf.rect(300, 315, 250, 125, stroke = 1, fill = 1)

#     ### Table : "Finicial Performance VS. Plan" ###
    
#     pdf.save()
    
    
    
    
    
    
    
    
    
#     # comp = request.POST.get('company')
#     # year = request.POST.get('year')

#     # report = Report()
#     # report.company = comp
#     # report.quarter = 1
#     # report.year = int(year)
#     # last_updated = datetime.now()

#     # request.dbsession.add(report)
#     # return HTTPFound(location=request.route_url('home'))


def genTable(report):
    reportTable = None
    reportWidth = 400

    #Build structure
    #Title
    titleTable = Table([['GEMSTONE II']], reportWidth)
    infoTable = Table([
        []
    ])
    
    #Add Style
    
    return report_table

@view_config(route_name = 'create_pdf', request_method = 'POST', permission = 'create_pdf')
def create_pdf(request, file_name, data, kpis):
    if data['company'] == 'MGR':
        data['company'] = 'MGR Plastics'
    if data['company'] == 'L&P':
        data['company'] == 'Label and Pack'
    
    
    pdf = SimpleDocTemplate(file_name, pagesize = letter)
    elems = []
    reportWidth = 500

    #styling tables
    body_heading = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.Color(red=(237.0/255),green=(237.0/255),blue=(237.0/255)))
    ])

    title_style = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 14), 
    ])
    
    heading_style = TableStyle([
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold")
    ])

    body_style = TableStyle([
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBEFORE', (1, 0), (-1, -1), 1, colors.black)
        # ('FONTNAME', (0, 0), (-1, -1), "Helvetica")
    ])

    table_heading_style = TableStyle([
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ])

    info_table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.Color(red=(255.0/255),green=(255.0/255),blue=(173.0/255)))
    ])
    
    #setting document title
    

    #inserting title
    titleTable = Table([['GEMSTONE II']], reportWidth)
    titleTable.setStyle(heading_style)
    titleTable.setStyle(title_style)
    elems.append(titleTable)

    # BLANK SPACE BETWEEN TABLES
    blankTable = Table([
        ['']], reportWidth
    )
    elems.append(blankTable)
    ### BOXES ###
    # Company, Quarter, Year
    infoTable = Table([
        ['Company : ', data['company'], 
        'Quarter : ', int(data['quarter']), 
        'Year : ', int(data['year'])]],
        [85, 215, 70, 30, 60, 40])
    infoTable.setStyle(info_table_style)
    elems.append(infoTable)

    elems.append(blankTable)

    # Industry and Business Major Highlights
    ### Made extra columns not rows ###
    # h_counter = 0
    # for highlight in data['highlight']:
    #     h_counter += 1
    # try:
    #     h_width = reportWidth/h_counter
    #     for i in range(h_counter):
    #         h_list.append(h_width)
        
    # except(ZeroDivisionError):
    #     data['highlight'] = ['']
    #     h_width = reportWidth
    
    h_list = [['Industry & Business Major Highlights']]
    for highlight in data['highlight']:
        h_list.append(['- '+highlight])

    highlightTable = Table(
        h_list, reportWidth
    )
    highlightTable.setStyle(body_heading)
    highlightTable.setStyle(body_style)
    highlightTable.setStyle(heading_style)

    elems.append(highlightTable)
    

    # Operations Update & Strategic Initiative Update
    # osTableTitle = Table([['Operations Update', 'Strategic Initiative Update']],[reportWidth/2, reportWidth/2])
    # osTableTitle.setStyle(heading_style)

    os_list = [['Operations Update', 'Strategic Initiative Update']]
    min_index = min(len(data['operation']),len(data['strategy']))
    max_index = max(len(data['operation']),len(data['strategy']))
    
    for i in range(min_index):
        os_list.append(['- '+data['operation'][i], '- '+data['strategy'][i]])
    
    if len(data['operation']) == max_index:
        for i in range(min_index, max_index):
            os_list.append(['- '+data['operation'][i], ''])
          
    elif len(data['strategy']) == max_index:
        for i in range(min_index, max_index):
            os_list.append(['', '- '+data['strategy'][i]])

    osTable = Table(os_list, [reportWidth/2, reportWidth/2])
    
    osTable.setStyle(body_heading)
    osTable.setStyle(heading_style)
    osTable.setStyle(body_style)

    elems.append(osTable)

    # New Customers Gained During Quarter & Major Orders Received During Quarter
    # coTableTitle = Table([['New Customers Gained During Quarter', 'Major Orders Received During Quarter']],[reportWidth/2, reportWidth/2])
    # coTableTitle.setStyle(heading_style)

    co_list = [['New Customers Gained During Quarter', 'Major Orders Received During Quarter']]
    min_index = min(len(data['customer']),len(data['order']))
    max_index = max(len(data['customer']),len(data['order']))
    
    for i in range(min_index):
        co_list.append(['- '+data['customer'][i], '- '+data['order'][i]])
    
    if len(data['customer']) == max_index:
        for i in range(min_index, max_index):
            co_list.append(['- '+data['customer'][i], ''])
          
    elif len(data['order']) == max_index:
        for i in range(min_index, max_index):
            co_list.append(['', '- '+data['order'][i]])

    
    coTable = Table(co_list, [reportWidth/2, reportWidth/2])

    coTable.setStyle(body_heading)
    coTable.setStyle(heading_style)
    coTable.setStyle(body_style)
    
    elems.append(coTable)
    elems.append(blankTable)

    ### Table : "Finicial Performance VS. Plan" ###
    finTableTitle = Table([['Finicial Performance VS. Plan']], reportWidth)
    finTableTitle.setStyle(heading_style)
    
    finTable = Table([
        ['', 'Q1', 'Q2', 'Q3', 'Q4', 'YTD', "% of FY", 'FY Plan'],
        ['Revenue', data['revenue_1'], data['revenue_2'], data['revenue_3'], data['revenue_4'], data['revenue_YTD'], data['revenue_FY'], data['revenue_plan']],
        ['Gross Profit', data['profit_1'], data['profit_2'], data['profit_3'], data['profit_4'], data['profit_YTD'], data['profit_FY'], data['profit_plan']],
        ['EBITDA', data['EBITDA_1'], data['EBITDA_2'], data['EBITDA_3'], data['EBITDA_4'], data['EBITDA_YTD'], data['EBITDA_FY'], data['EBITDA_plan']],
        ['Free Cash Flow', data['cf_1'], data['cf_2'], data['cf_3'], data['cf_4'], data['cf_YTD'], data['cf_FY'], data['cf_plan']]
    ], [140, 40, 40, 40, 40, 60, 70, 90])
    finTable.setStyle(table_heading_style)
    finTable.setStyle(body_heading)

    elems.append(finTableTitle)
    elems.append(finTable)
    
    elems.append(blankTable)
    # Explanation and Variance
    # explainTableTitle = Table([['Variance Explanation & Mitigation']],reportWidth)
    # explainTableTitle.setStyle(heading_style)

    e_list = [['Variance Explanation & Mitigation']]
    for explain in data['explain']:
        e_list.append(['- '+explain])

    explainTable = Table(
        e_list, reportWidth
    )
    
    explainTable.setStyle(body_heading)
    explainTable.setStyle(body_style)
    explainTable.setStyle(heading_style)
    # if e_list != [['Variance Explanation & Mitigation']]:
    elems.append(explainTable)

    elems.append(blankTable)

    #KPIS
    kpiTableTitle = Table([['Key Performance Indicators']],reportWidth)
    kpiTableTitle.setStyle(heading_style)

    kpi_list = [['Description', 'Value', 'Target']]
    
    for kpi in kpis:
        kpi_list.append([kpi.kpi_name, str(kpi.value), str(kpi.target)])
    
    kpiTable = Table(kpi_list, [300, 100, 100])

    kpiTable.setStyle(heading_style)
    kpiTable.setStyle(body_style)
    kpiTable.setStyle(body_heading)
    for i in range(1, len(kpi_list)):
        if i % 2 == 0:
            clr = colors.burlywood
        else:
            clr = colors.beige

        ts = TableStyle([
            ('BACKGROUND', (0, i), (-1, i), clr)
        ])
        kpiTable.setStyle(ts)
    elems.append(kpiTableTitle)    
    elems.append(kpiTable)
    pdf.build(elems)

    # pdf.save()
    
    
    
    
    
    
    
    
    
    # comp = request.POST.get('company')
    # year = request.POST.get('year')

    # report = Report()
    # report.company = comp
    # report.quarter = 1
    # report.year = int(year)
    # last_updated = datetime.now()

    # request.dbsession.add(report)
    # return HTTPFound(location=request.route_url('home'))