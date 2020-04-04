<%inherit file="layout.mako"/>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif
${form | n}
## %for kpi in kpis:
##     ${kpi.kpi_name}
##     ## ${kpi.kpi_id}
##     <a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a>

## %endfor

<div class = "row text-center" id='kpi_list' style = "border-style: solid; border-width: 1px;"><h3><strong>Active Key Performance Indicators</strong></h3>
    %if checker is not None:
        ## <div class = "row" style = "padding: 10px; height : 25px;">
        ##     ## <div class = "col-md-10 text-left"><h5 style = "text-decoration: underline;">Name:</h5>
        ##     ## </div>
        ##     ## <div class = "col-md-2 text-right"><h5 style = "text-decoration: underline;">Edit</h5>
        ##     ## </div>
        ##     ## <div class = "col-md-2 text-center"><h5 style = "text-decoration: underline;">DELETE</h5>
        ##     ## </div>
        ## </div>
        %for kpi in kpis:
            <div class = "row" style = "padding: 10px; height : 25px;">
                <div class = "col-md-10 text-left">${kpi.kpi_name}</div>
                
                <div class = "col-md-2 text-right"><a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a></div>
                ## </div>
                ## <div class = "col-md-2 text-center"><a href="${request.route_url('kpi_delete', id=kpi.kpi_id)}">x</a>
                ## </div>
            </div>
        %endfor
        <div class = "row" style = "padding: 10px; height : 25px;">
    %endif
        ## %for kpi in kpis:
        ##     <div class = "row" style = "padding: 10px; height : 25px;">
        ##         <div class = "col-md-10 text-left">${kpi.kpi_name}</div>
                
        ##         <div class = "col-md-2 text-right"><a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a></div>
        ##         ## </div>
        ##         ## <div class = "col-md-2 text-center"><a href="${request.route_url('kpi_delete', id=kpi.kpi_id)}">x</a>
        ##         ## </div>
        ##     </div>
        ## %endfor
    
</div>