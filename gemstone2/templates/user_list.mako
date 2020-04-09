<%inherit file="layout.mako"/>


## %for item in users:
##     %if item.user_id != request.user.user_id:
##     <li>
##     <span id = 'user_username'>${item.first_name} - ${item.username} ----- ${item.permissions}</span>
##     <a href="${request.route_url('user_list_edit', id=item.user_id)}">edit</a>
##     <a href = "${request.route_url('reset_user', id=item.user_id)}">reset</a>
##     </li>
##     %endif
## %endfor


<div class = "row" style = "padding: 10px; height : 25px;">
    <div class = "col-md-3 text-center" style = "text-decoration: underline;">Name
    </div>
    <div class = "col-md-3 text-center" style = "text-decoration: underline;">Username
    </div>
    <div class = "col-md-3 text-center" style = "text-decoration: underline;">Permission
    </div>
    <div class = "col-md-2 text-center" style = "text-decoration: underline;">Edit
    </div>
    <div class = "col-md-1 text-center" style = "text-decoration: underline;">RESET
    </div>
</div>
%for x in users:
    ## %if x.user_id != request.user.user_id:
    <div class = "row" style = "padding: 10px; height : 25px;">
        <div class = "col-md-3 text-center">${x.first_name.capitalize()} ${x.last_name.capitalize()}
        </div>
        <div class = "col-md-3 text-center">${x.username}
        </div>
        <div class = "col-md-3 text-center">${x.permissions}
        </div>
        <div class = "col-md-2 text-center">
            <a href="${request.route_url('user_list_edit', id=x.user_id)}"><button class = 'btn btn-primary'></button></a>
        </div>
        <div class = "col-md-1 text-center">
            <a href = "${request.route_url('reset_user', id=x.user_id)}"><button class = 'btn btn-danger' onclick = "return confirm('Are you sure you want to reset this password?')"></button></a>
        </div>
    </div>
    ## %endif
%endfor
        


<div class = "row" style = "padding: 50px; height: 25px;">
    <div class= 'col-md-10'></div>
    <div class = "col-md-2">
        <a href = "${request.route_url('create')}"><button class = 'btn btn-success'>CREATE A NEW USER</button></a>
    </div>
</div>