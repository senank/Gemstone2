<%inherit file="layout.mako"/>
<h1 style="margin-bottom: 5vw;">${report.company} Q${report.quarter} ${report.year}</h1>

${form | n}


<input type="checkbox" value="1" name="report" data-id="${report.id}"
    % if report.published:
    checked
    % else:
    onclick = "return confirm('Are you sure you want to publish?\n\n THIS WILL NOTIFY ALL USERS')"
    % endif
    > Publish
<%block name="page_script">
<script>
    var save = document.getElementById("deformsave");
    save.classList.remove('btn-primary');
    save.classList.add('btn-labeled','btn-success');
    
    var pdf = document.getElementById("deformpdf");
    pdf.classList.remove('btn-default');
    pdf.classList.add('btn-labeled','btn-warning');

    var back = document.getElementById("deformback");
    back.classList.remove('btn-default');
    back.classList.add('btn-labeled','btn-primary');

    var add = document.getElementsByClassName("deform-seq-add")
    
    for(var i = 0; i < add.length; i++){
        add[i].classList.add('btn-labeled','btn-success');
        add[i].style.width = '39px'
        add[i].innerHTML = '<span class="btn-label"><i class="fas fa-plus"></i></span>'
    }

    save.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-ok"></i></span>Save';
    pdf.innerHTML = '<span class="btn-label"><i class="far fa-file-pdf"></i></span>PDF';
    back.innerHTML = '<span class="btn-label"><i class="fas fa-arrow-alt-circle-left"></i></span>Back';
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