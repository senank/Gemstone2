<%inherit file="layout.mako"/>

<h1>Create an Account! :)</h1>
<form action = "${request.route_url('create')}" method = "POST">
    <div class = 'form-group'>
        <div class = 'form-group'>
            <label>Username:
                <input type="text" class = 'form-control' name = "username" placeholder = 'username' required>
            </label>
        </div>
        <div class = 'form-group'>
            <label>First Name:
                <input type="text" class='form-control' name = "first_name" placeholder="${request.user.first_name.capitalize()}">
            </label>
        
            <label>Last Name:
                <input type="text" class='form-control' name = "last_name" placeholder="${request.user.last_name.capitalize()}">
            </label>
        </div>
        <div class = 'form-group'>
            <label>Password:
                <input type = "password" class = 'form-control' name = "password" placeholder = 'Password'required>
            </label>
            <label>Confirm:
                <input type = 'password' class = 'form-control' name ="confirm_password" placeholder = 'Confirm' required>
            </label>
        </div>
        <div class = 'form-group'>
            <label>Permission:
                <select name = 'permission'>
                    <option value = 'admin'>admin</option>
                    <option value = 'viewer' selected>viewer</option>
            </label>
        </div>
    </div>
    <div class='form-group'>
        <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
        <input name = 'login_submit' type = "submit" class = "btn btn-primary" value='Create'>
    </div>
</form>
%if error:
    %for key, msg in error.items():
        <p class="alert alert-danger">
            ${msg}
        </p>
    %endfor
%endif