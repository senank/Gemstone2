<%inherit file="layout.mako"/>

<div class = "col-xs-3"></div>
<div class = "col-xs-6">
    <div class= 'content'>
        <h1>Create an Account</h1>
        <div class = 'form-group'>
            <form action = "${request.route_url('create')}" method = "POST" class = "inline-block">
                <div>
                    <label>Username:
                        <input type="text" class = 'form-control f-style' name = "username" placeholder="example@email.com">
                    </label>
                </div>
                <div class = 'form-group'>
                    <label>First Name:
                        <input type="text" class='form-control f-style' name = "first_name">
                    </label>
                    <label>Last Name:
                        <input type="text" class='form-control f-style' name = "last_name">
                    </label>
                </div>
                <div class = 'form-group'>
                    <label>Password:
                        <input type = "password" class = 'form-control f-style' name = "password">
                    </label>
                    <label>Confirm:
                        <input type = 'password' class = 'form-control f-style' name ="confirm_password">
                    </label>
                </div>
                <div class = 'form-group'>
                    <label>Permission:
                        <select name = 'permission' class='inline-block f-style' style="width:100%;">
                            <option value = 'admin'>Admin</option>
                            <option value = 'viewer' selected>Viewer</option>
                        </select>
                    </label>
                </div>
                <div>
                    <div class='form-group'>
                        <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                        <button type="submit" style = "display: block !important; margin: 1vw 0 0 0;"value="Login" name = 'login_submit' class = "btn btn-labeled btn-success"><span class="btn-label"><i class="fas fa-user-plus"></i></span>Create</button>
                    </div>
                </div>
            </form>
        </div>
    %if error:
        %for key, msg in error.items():
            <p class="alert alert-danger">
                ${msg}
            </p>
        %endfor
    %endif
    </div>
</div>
<div class = "col-xs-3"></div>