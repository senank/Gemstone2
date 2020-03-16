<%inherit file="layout.mako"/>
%for item in reports:
    <li>
    <span id='description_name'>${item.company} ${item.quarter} ${item.year}</span>
    </li>
%endfor
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