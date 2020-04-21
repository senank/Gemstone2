<%inherit file="layout.mako"/>
<div class = "col-md-4"></div>
<div class = "col-md-4">
    ${form | n}
</div>
<div class = "col-md-4"></div>


<%block name="page_script">
<script>
    var save = document.getElementById("deformsubmit");
    save.classList.remove('btn-primary');
    save.classList.add('btn-labeled','btn-success')
    
    var pdf = document.getElementById("deformdelete")
    pdf.classList.remove('btn-default');
    pdf.classList.add('btn-labeled','btn-danger')

    var back = document.getElementById("deformcancel");
    back.classList.remove('btn-default');
    back.classList.add('btn-labeled','btn-primary')
    
    save.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-ok"></i></span>save';
    pdf.innerHTML = '<span class="btn-label"><i class="glyphicon glyphicon-trash"></i></span>delete';
    back.innerHTML = '<span class="btn-label"><i class="fas fa-arrow-alt-circle-left"></i></span>cancel';
</script>
</%block>