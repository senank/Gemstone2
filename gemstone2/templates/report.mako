<%inherit file="layout.mako"/>
%if auth_ == 'admin':
    <a href="${request.route_url('kpi_list')}">KPI List</a>
%endif
%for report in reports:
    <li>
    <span id='description_name'>${report.company} ${report.quarter} ${report.year}</span>
    %if auth_ == 'admin':
    <a href="${request.route_url('edit_report', id=report.id)}">edit</a>
    <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
    %endif
    </li>
%endfor
%if auth_ == 'admin':
${form | n} 
%endif
## <form action = "${request.route_url('add_test')}" method = "POST">
##     <div class = 'form-row'>
##         <div class = 'col' >
##             <label>company:<input type="text" class = 'form-control' name = "company" placeholder="username"></label>
##         </div>
##         <div class = 'col' >
##             <label>year<input type = "password" class = 'form-control' name = "year" placeholder = "password"></label>
##         </div>
##     </div> 
##     <div class = 'form-group' >  
##         <input name = 'add' type = "submit" class = "btn btn-primary" value='add'>
##     </div>   
## </form>