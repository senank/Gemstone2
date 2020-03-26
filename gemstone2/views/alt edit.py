# @view_config(route_name = 'edit_report', renderer='../templates/report_edit.mako')
# def edit_report(request):
    
#     try:
#         id_ = int(request.matchdict['id'])
#     except (ValueError, TypeError):
#         raise HTTPNotFound
    
#     report = request.dbsession.query(Report).filter(Report.id == id_).first()
    
#     current = {
#         'company' : report.company,
#         'quarter' : report.quarter,
#         'year' : report.year,

#         'highlights' : report.highlights,
#         'operation' : report.operation,
#         'strategy' : report.strategy,
#         'customer_gained' : report.customer_gained,
#         'orders' : report.orders,
        
#         'revenue_1' : report.revenue_1,
#         'revenue_2' : report.revenue_2,
#         'revenue_3' : report.revenue_3,
#         'revenue_4' : report.revenue_4,
#         'revenue_YTD' : report.revenue_YTD,
#         'revenue_FY' : report.revenue_FY,
#         'revenue_plan' : report.revenue_plan,

#         'profit_1' : report.profit_1,
#         'profit_2' : report.profit_2,
#         'profit_3' : report.profit_3,
#         'profit_4' : report.profit_4,
#         'profit_YTD' : report.profit_YTD,
#         'profit_FY' : report.profit_FY,
#         'profit_plan' : report.profit_plan,

#         'EBITDA_1' : report.EBITDA_1,
#         'EBITDA_2' : report.EBITDA_2,
#         'EBITDA_3' : report.EBITDA_3,
#         'EBITDA_4' : report.EBITDA_4,
#         'EBITDA_YTD' : report.EBITDA_YTD,
#         'EBITDA_FY' : report.EBITDA_FY,
#         'EBITDA_plan' : report.EBITDA_plan,

#         'cf_1' : report.cf_1,
#         'cf_2' : report.cf_2,
#         'cf_3' : report.cf_3,
#         'cf_4' : report.cf_4,
#         'cf_YTD' : report.cf_YTD,
#         'cf_FY' : report.cf_FY,
#         'cf_plan' : report.cf_plan,

#         'explain' : report.explain,

#         'filename' : report.filename,
#         'unique_filename' : report.unique_filename
#     }
    
#     if current['company'] == 'MGR':
#         current['company'] = 'MGR Plastics'
#     elif current['company'] == 'LP':
#         current['company'] = 'Label & Pack'
    
#     ### FORM SCHEMA SETUP ###
#     #CSRF Schema
#     class CSRFSchema(colander.MappingSchema): 
#         csrf_token = colander.SchemaNode(colander.String(), default=deferred_csrf_default, widget=deform.widget.HiddenWidget())
    

    
#     #Highlight Schema
#     class Highlight(colander.Schema):
#         highlight = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class HighlightsSchema(colander.SequenceSchema):
#         highlight = Highlight()


    
#     #Operations Schema
#     class Operation(colander.Schema):
#         operation = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class OperationSchema(colander.SequenceSchema):
#         operation = Operation()


    
#     #Strategy Schema
#     class Strategy(colander.Schema):
#         strategy = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class StrategySchema(colander.SequenceSchema):
#         strategy = Strategy()



#     #Customer_gained Schema
#     class Customer(colander.Schema):
#         customer = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class Customers(colander.SequenceSchema):
#         customers = Customer()



#     #Orders Schema
#     class Order(colander.Schema):
#         customer = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class Orders(colander.SequenceSchema):
#         order = Order()



#     #Revenue Schema
#     class RevenueSchema(colander.Schema):
#         revenue_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = 0, missing = colander.drop)
#         revenue_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = 0, missing = colander.drop)
#         revenue_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = 0, missing = colander.drop)
#         revenue_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = 0, missing = colander.drop)
#         revenue_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = 0, missing = colander.drop)
#         revenue_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = 0, missing = colander.drop)
#         revenue_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = 0, missing = colander.drop)



#     #Profit Schema
#     class ProfitSchema(colander.Schema):
#         profit_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = 0, missing = colander.drop)
#         profit_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = 0, missing = colander.drop)
#         profit_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = 0, missing = colander.drop)
#         profit_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = 0, missing = colander.drop)
#         profit_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = 0, missing = colander.drop)
#         profit_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = 0, missing = colander.drop)
#         profit_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = 0, missing = colander.drop)


    
#     #EBITDA Schema
#     class EBITDASchema(colander.Schema):
#         EBITDA_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = 0, missing = colander.drop)
#         EBITDA_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = 0, missing = colander.drop)
#         EBITDA_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = 0, missing = colander.drop)
#         EBITDA_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = 0, missing = colander.drop)
#         EBITDA_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = 0, missing = colander.drop)
#         EBITDA_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = 0, missing = colander.drop)
#         EBITDA_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = 0, missing = colander.drop)

#     #cf Schema
#     class CFSchema(colander.Schema):
#         cf_1 = colander.SchemaNode(colander.Integer(), description = 'Q1', default = 0, missing = colander.drop)
#         cf_2 = colander.SchemaNode(colander.Integer(), description = 'Q2', default = 0, missing = colander.drop)
#         cf_3 = colander.SchemaNode(colander.Integer(), description = 'Q3', default = 0, missing = colander.drop)
#         cf_4 = colander.SchemaNode(colander.Integer(), description = 'Q4', default = 0, missing = colander.drop)
#         cf_YTD = colander.SchemaNode(colander.Integer(), description = 'YTD Actual', default = 0, missing = colander.drop)
#         cf_FY = colander.SchemaNode(colander.Integer(), description = "% of FY Plan", default = 0, missing = colander.drop)
#         cf_plan = colander.SchemaNode(colander.Integer(), description = 'FY Plan', default = 0, missing = colander.drop)



#     #Explain Schema
#     class Explaination(colander.Schema):
#         explain = colander.SchemaNode(colander.String(), missing = colander.drop)

#     class Explainations(colander.SequenceSchema):
#         explanation = Explaination()



#     #Form schema
#     class MySchema(CSRFSchema):
#         company = colander.SchemaNode(colander.String(), 
#             validator = colander.Length(min = 1, max = 24), 
#             widget = deform.widget.SelectWidget(values=((('MGR', 'MGR Plastics'), ('LP', 'Label & Pack'),))),
#             default = current['company'])
#         quarter = colander.SchemaNode(colander.Integer(), 
#             validator = colander.Range(min = 1, max = 4),
#             widget = deform.widget.SelectWidget(values=(((1,1),(2,2),(3,3),(4,4),))),)
#         year = colander.SchemaNode(colander.Integer())

#         highlights = HighlightsSchema(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
#         operations = OperationSchema(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
#         strategies = StrategySchema(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
#         customers = Customers(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
#         orders = Orders(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10)) 
        
#         revenue = RevenueSchema()
#         profit = ProfitSchema()
#         EBITDA = EBITDASchema(title = 'EBITDA')
#         cf = CFSchema(title = 'CF')
        
#         explain = Explainations(validator = colander.Length(min = 1, max = 10), 
#             widget=deform.widget.SequenceWidget(min_len=1, max_len=10))
    
#     ### FORM SCHEMA SETUP FINISHED ###
    
#     schema = MySchema().bind(request=request)
    
#     #fileupload
#     class MemoryTmpStore(dict):
#         """ Instances of this class implement the
#         :class:`deform.interfaces.FileUploadTempStore` interface"""

#         def preview_url(self, uid):
#             return None
    
#     tmpstore = MemoryTmpStore()        
#     schema.add(colander.SchemaNode(
#         deform.FileData(),
#         widget = deform.widget.FileUploadWidget(tmpstore),
#         name = 'upload',
#         missing = None
#         ))
    

#     myform = deform.Form(schema, buttons=('save', 'publish'))
#     form = myform.render()


#     if 'save' in request.POST:
#         control = request.params.items()

#         try:
#             form_data = myform.validate(control)

#         except deform.exception.ValidationFailure as e:
#             return {
#                 'report' : report,
#                 'id' : id_,
#                 'form' : e.render(),
#                 # 'desc': current['description']
#                 }

#         highlight_lst = None
#         operation_lst = None
#         strategy_lst = None
#         customer_lst = None
#         order_lst = None
#         explain_lst = None

#         highlight_update = []
#         operation_update = []
#         strategy_update = []
#         customer_update = []
#         order_update = []
#         explain_update = []
        
#         for field, data in form_data.items():
#             if field == 'highlights':
#                 highlight_lst = data
#             elif field == 'operations':
#                 operations_lst = data
#             elif field == 'strategies':
#                 strategy_lst = data
#             elif field == 'customers':
#                 customer_lst = data
#             elif field == 'orders':
#                 orders_lst = data
#             elif field == 'explain':
#                 explain_lst = data
        
#         def append_to_lst(prior_list, update_list):
#             try:
#                 for item in prior_list:
#                     for key, val in item.items():
#                         update_list.append(val)

#             except (TypeError):
#                 pass

        
#         for highlight in highlight_lst:
#             for key,val in highlight.items():
#                 highlight_update.append(val)

#         append_to_lst(operation_lst, operation_update)
#         append_to_lst(strategy_lst, strategy_update)
#         append_to_lst(order_lst, order_update)
#         append_to_lst(explain_lst, explain_update)
        
#         #finish the updating of the report object and return to reports page
#         request.dbsession.add(report)
        

#     return {
#         'report' : report,
#         'id' : id_,
#         'form' : form,
#         # 'desc' : current['description'],
#         # 'img' : img
#     }