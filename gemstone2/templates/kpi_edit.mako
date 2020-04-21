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

<%block name="page_script">
<script>
    var save = document.getElementById("deformsave");
    save.classList.remove('btn-primary');
    save.classList.add('btn-labeled','btn-success');
    
    var del = document.getElementById("deformdelete");
    del.classList.remove('btn-default');
    del.classList.add('btn-labeled','btn-danger');

    var back = document.getElementById("deformback");
    back.classList.remove('btn-default');
    back.classList.add('btn-labeled','btn-primary');


    save.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-ok"></i></span>Save';
    del.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-trash"></i></span>Delete';
    back.innerHTML = '<span class="btn-label"><i class="fas fa-arrow-alt-circle-left"></i></span>Cancel';
</script>
</%block>