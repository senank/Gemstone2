<%inherit file="layout.mako"/>
%if auth_ == 'admin':
    <a href="${request.route_url('kpi_list')}">KPI List</a>
%endif
%for item in reports:
    <li>
    <span id='description_name'>${item.company} ${item.quarter} ${item.year}</span>
    %if auth_ == 'admin':
    <a href="${request.route_url('edit_report', id=item.id)}">edit</a>
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