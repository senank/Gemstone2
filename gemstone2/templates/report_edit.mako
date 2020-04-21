<%inherit file="layout.mako"/>
${form | n}


<input type="checkbox" value="1" name="report" data-id="${report.id}"
    % if report.published:
    checked
    % endif
    > Publish
<%block name="page_script">
<script>
    var save = document.getElementById("deformsave");
    save.classList.remove('btn-primary');
    save.classList.add('btn-labeled','btn-success')
    
    var pdf = document.getElementById("deformpdf")
    pdf.classList.remove('btn-default');
    pdf.classList.add('btn-labeled','btn-warning')

    var back = document.getElementById("deformback");
    back.classList.remove('btn-default');
    back.classList.add('btn-labeled','btn-primary')
    
    save.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-ok"></i></span>save';
    pdf.innerHTML = '<span class="btn-label"><i class="far fa-file-pdf"></i></span>pdf';
    back.innerHTML = '<span class="btn-label"><i class="fas fa-arrow-alt-circle-left"></i></span>back';
</script>
<script>
var csrfToken = "${get_csrf_token()}";
jQuery(function($){
    $(document).on('change', 'input[name^="report"]', function(){
        $.post("${request.route_url('publish_report')}", {id: $(this).data('id'), checked: $(this).is(':checked'), 'csrf_token' : csrfToken});
    });
});
</script>
</%block>