<%inherit file="layout.mako"/>
${form | n}


<input type="checkbox" value="1" name="report" data-id="${report.id}"
    % if report.published:
    checked
    % endif
    > Publish


<%block name="page_script">
<script>
var csrfToken = "${get_csrf_token()}";
jQuery(function($){
    $(document).on('change', 'input[name^="report"]', function(){
        $.post("${request.route_url('publish_report')}", {id: $(this).data('id'), checked: $(this).is(':checked'), 'csrf_token' : csrfToken});
    });
});
</script>
</%block>