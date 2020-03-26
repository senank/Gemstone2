<%inherit file="layout.mako"/>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif
${form | n}

%for kpi in kpis:
    ${kpi.kpi_name}
    ## ${kpi.kpi_id}
    <a href="${request.route_url('kpi_edit', id=kpi.kpi_id)}">edit</a>

%endfor

<a href = "${request.route_url('report_list')}"> Report List