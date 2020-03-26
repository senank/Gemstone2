<%inherit file="layout.mako"/>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif
${form | n}


