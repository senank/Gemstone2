<%inherit file="layout.mako"/>

<a href = "${request.route_url('create')}">CREATE AN ACCOUNT</a>

%for item in users:
    %if item.user_id != request.user.user_id:
    <li>
    <span id = 'user_username'>${item.first_name} - ${item.username} ----- ${item.permissions}</span>
    <a href="${request.route_url('user_list_edit', id=item.user_id)}">edit</a>
    <a href = "${request.route_url('reset_user', id = item.user_id)}">reset</a>
    </li>
    %endif
%endfor
