<%inherit file="layout.mako"/>
## %if auth_ == 'admin':
##     <a href="${request.route_url('kpi_list')}">KPI List</a>
## %endif
%if auth_ == 'admin':
<div class = 'row' style = "margin: 10px;">
    <div class = "col-md-6 text-center" style = "padding: 15px; height : height: 100%;"><h5 style = "text-decoration: underline;">MGR Plastics</h5>
        <ul>
            %for report in mgr_reports:
                <li>
                <span id='description_name'>${report.quarter} ${report.year}</span>
                <a href="${request.route_url('edit_report', id=report.id)}"><button class = 'btn btn-primary'>edit</button></a>
                <a href = "${request.route_url('delete_report', id=report.id)}"><button class = 'btn btn-danger' onclick = "return confirm('Are you sure you want to DELETE this report?')">delete</button></a>
                %if report.published == True:
                    <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                %endif
                </li>
            %endfor
        </ul>
    </div>
    <div class = "col-md-6 text-center" style = "padding: 15px; height : height: 100%;"><h5 style = "text-decoration: underline;">Label and Pack</h5>
        <ul>
            %for report in lp_reports:
                <li>
                <span id='description_name'>${report.quarter} ${report.year}</span>
                <a href="${request.route_url('edit_report', id=report.id)}"><button class = 'btn btn-primary'>edit</button></a>
                <a href = "${request.route_url('delete_report', id=report.id)}"><button class = 'btn btn-danger' onclick = "return confirm('Are you sure you want to DELETE this report?')">delete</button></a>
                %if report.published == True:
                    <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                %endif
                </li>
            %endfor
        </ul>
    </div>
</div>


###### Checking if the reports are correct ######

## %if mgr_max_report:
##     ${mgr_max_report.quarter} ${mgr_max_report.year}
## %endif
## %if lp_max_report:
##     ${lp_max_report.quarter} ${lp_max_report.year}
## %endif
## ${maxs.year} ${maxs.quarter}


${form | n} 

%else:
    <div class = 'row' style = "margin: 10px;">
        <div class = "col-md-3 text-center" style = "padding: 15px; height : 150px;"><h5 style = "text-decoration: underline;">MGR Plastics</h5>
            <ul>
                %for report in mgr_reports:
                    %if report.published == True:
                        <li>
                        <span id='description_name'>${report.quarter} ${report.year}</span>
                        <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                        </li>
                    %endif
                %endfor
            </ul>
        </div>
        <div class = "col-md-3 text-center" style = "padding: 15px; height : 150px;"><h5 style = "text-decoration: underline;">Label and Pack</h5>
            <ul>
                %for report in lp_reports:
                    %if report.published == True:
                        <li>
                        <span id='description_name'>${report.quarter} ${report.year}</span>
                        <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                        </li>
                    %endif
                %endfor
            </ul>
        </div>
        <div class = "col-md-6 text-center" style = "padding: 15px; height : height: 100%;"><h5 style = "text-decoration: underline;">Key Performance Indicators</h5>
        <div class = "col-md-6"><h6 style = "text-decoration: underline;">MGR Plastic</h6>
        %if mgr_kpi_display:
            %for kpi in mgr_kpi_display:
                <li>
                <span style = 'text-decoration: text-left'id='description_name'>${kpi.kpi_name} - ${kpi.value}</span>
                ## <a href="${request.route_url('edit_report', id=report.id)}">edit</a>
                ## <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                </li>
            %endfor
        %endif
        </div>
        <div class = "col-md-6"><h6 style = "text-decoration: underline;">Label and Pack</h6>
        %if lp_kpi_display:
            %for kpi in lp_kpi_display:
                <li>
                <span id='description_name'>${kpi.kpi_name} - ${kpi.value}</span>
                ## <a href="${request.route_url('edit_report', id=report.id)}">edit</a>
                ## <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                </li>
            %endfor
        %endif
        </div>
    </div>
    </div>
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