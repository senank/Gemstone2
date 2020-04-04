<%inherit file="layout.mako"/>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif
${form | n}

## <button><a href = "${request.route_url('kpi_list')}">CANCEL</a></button>

