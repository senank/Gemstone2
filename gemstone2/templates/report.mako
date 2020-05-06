<%inherit file="layout.mako"/>
## %if auth_ == 'admin':
##     <a href="${request.route_url('kpi_list')}">KPI List</a>
## %endif
%if auth_ == 'admin':
<div class = 'row' style = "margin: 10px;">
    <div class = "col-md-6 text-center" style = "padding: 15px; height: 100%;"><h4 style = "text-decoration: underline;"><strong>MGR Plastics</strong></h4>
        <ul style = "list-style: none;">
            %for report in mgr_reports:
                <li class = "report_li">
                
                <span style="margin: 0 2vw 0 0">${report.quarter} ${report.year}</span>
                %if report.filename is not None:
                    <% filepath = 'gemstone2:static/pdfs/' + report.filename %>
                    <a style="margin: 0 2vw 0 0" href = "${request.static_url(filepath)}"><i class="far fa-file-pdf" style="display: inline-block; font-size: 25px; color: #ffbfbf; margin: 2px;"></i></a>
                %else:
                    <div style="margin: 0 3.4vw 0 0; display: inline-block;"></div>
                %endif
                <a href="${request.route_url('edit_report', id=report.id)}"><button class = 'btn btn-labeled btn-warning'><span class="btn-label"><i class="far fa-edit"></i></span>edit</button></a>
                <a href = "${request.route_url('delete_report', id=report.id)}"><button class = 'btn btn-labeled btn-danger' style="width:39px;" onclick = "return confirm('Are you sure you want to DELETE this report?')"><span class="btn-label"><i class="glyphicon glyphicon-trash"></i></span></button></a>
                ## %if report.published == True:
                ##     <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                ## %endif
                </li>
            %endfor
        </ul>
    </div>
    <div class = "col-md-6 text-center" style = "padding: 15px; height : 100%;"><h4 style = "text-decoration: underline;"><strong>Label and Pack</strong></h4>
        <ul style = "list-style: none;">
            %for report in lp_reports:
                <li class = "report_li">
                <span id='description_name'>${report.quarter} ${report.year}</span>
                %if report.filename is not None:
                    <% filepath = 'gemstone2:static/pdfs/' + report.filename %>
                    <a style="margin: 0 2vw 0 0" href = "${request.static_url(filepath)}"><i class="far fa-file-pdf" style="display: inline-block; font-size: 25px; color: #ffbfbf; margin: 2px;"></i></a>
                %else:
                    <div style="margin: 0 3.4vw 0 0; display: inline-block;"></div>
                %endif
                <a href="${request.route_url('edit_report', id=report.id)}"><button class = 'btn btn-labeled btn-warning'><span class="btn-label"><i class="far fa-edit"></i></span>edit</button></a>
                <a href = "${request.route_url('delete_report', id=report.id)}"><button class = 'btn btn-labeled btn-danger' style="width:39px;" onclick = "return confirm('Are you sure you want to DELETE this report?')"><span class="btn-label"><i class="glyphicon glyphicon-trash"></i></span></button></a>
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
        <div class = "col-md-3 text-center" style = "padding: 15px; height : 150px;"><h4 style = "text-decoration: underline; display: inline-block;"><strong>MGR Plastics</strong></h4>
            <ul style = "list-style: none; text-align:left;">
                %for report in mgr_reports:
                    %if report.published == True and report.filename is not None:
                        <% filepath = 'gemstone2:static/pdfs/' + report.filename %>
                        <li><a class = "tag_body" href = "${request.static_url(filepath)}"><i class="far fa-file-pdf"></i> ${report.filename}</a></li>
                    %endif
                %endfor
            </ul>
        </div>
        <div class = "col-md-3 text-center" style = "padding: 15px; height : 150px;"><h4 style = "text-decoration: underline;"><strong>Label and Pack</strong></h4>
            <ul style = "list-style: none; text-align:left;">
                %for report in lp_reports:
                    %if report.published == True and report.filename is not None:
                        <% filepath = 'gemstone2:static/pdfs/' + report.filename %>
                        <li><a class = "tag_body" href = "${request.static_url(filepath)}"><i class="far fa-file-pdf"></i> ${report.filename}</a></li>
                    %endif
                %endfor
            </ul>
        </div>
        <div class = "col-md-6 text-center" style = "padding: 15px; height: 100%;"><h4 style = "text-decoration: underline;"><strong>Key Performance Indicators</strong></h4>
        <div class = "col-md-6"><h5 style = "text-decoration: underline;">MGR Plastic</h5>
        %if mgr_kpi_display:
            %for kpi in mgr_kpi_display:
                <li class = "kpi_li">
                <span style = 'text-decoration: text-left'id='description_name'>${kpi.kpi_name} --- ${kpi.value}</span>
                ## <a href="${request.route_url('edit_report', id=report.id)}">edit</a>
                ## <a href = "${request.route_url('pdf_tester', id = report.id)}">pdf</a>
                </li>
            %endfor
        %endif
        </div>
        <div class = "col-md-6"><h5 style = "text-decoration: underline;">Label and Pack</h5>
        %if lp_kpi_display:
            %for kpi in lp_kpi_display:
                <li class = "kpi_li">
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

<%block name="page_script">
<script>
    var add = document.getElementById("deformadd");
    add.classList.remove('btn-primary');
    add.classList.add('btn-labeled','btn-success');

    add.innerHTML = '<span class="btn-label"><i class="fas fa-plus"></i></span>Add Report';
</script>
</%block>