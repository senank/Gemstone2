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
        <div class = "col-xs-10"></div>
        ##     ## <div class = "col-xs-10 text-left"><h5 style = "text-decoration: underline;">Name:</h5>
        ##     ## </div>
        
        <div class = "col-xs-2 text-right"><h4><strong>EDIT</strong></h4>
        </div>
        ##     ## <div class = "col-xs-2 text-center"><h5 style = "text-decoration: underline;">DELETE</h5>
        ##     ## </div>
        ## </div>
        %for kpi in kpis:
            <div class = "row" style = "padding: 10px; height : 25px;">
                <div class = "col-xs-10 text-left">${kpi.kpi_name}</div>
                
                <div class = "col-xs-2 text-right"><a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}"><button class = 'btn btn-labeled btn-warning' style='width:39px; margin-left: 0; margin-right: 0.3vw'><span class="btn-label"><i class="far fa-edit"></i></span></button></i></button></a></div>
                ## <div class = "col-xs-2 text-right"><a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a></div>

                ## </div>
                ## <div class = "col-xs-2 text-center"><a href="${request.route_url('kpi_delete', id=kpi.kpi_id)}">x</a>
                ## </div>
            </div>
        %endfor
        <div class = "row" style = "padding: 10px; height : 25px;">
    %endif
        ## %for kpi in kpis:
        ##     <div class = "row" style = "padding: 10px; height : 25px;">
        ##         <div class = "col-xs-10 text-left">${kpi.kpi_name}</div>
                
        ##         <div class = "col-xs-2 text-right"><a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a></div>
        ##         ## </div>
        ##         ## <div class = "col-xs-2 text-center"><a href="${request.route_url('kpi_delete', id=kpi.kpi_id)}">x</a>
        ##         ## </div>
        ##     </div>
        ## %endfor
    
</div>
<%block name="page_script">
<script>
    var add = document.getElementById("deformadd");
    add.classList.remove('btn-primary');
    add.classList.add('btn-labeled','btn-success');

    add.innerHTML = '<span class="btn-label"><i class="fas fa-plus"></i></span>Add KPI';
</script>
</%block>