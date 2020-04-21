<%inherit file="layout.mako"/>
<div class="col-sm-3"></div>
<div class="col-sm-6">
    <div class="content">
        %if error:
            %for key, msg in error.items():
                <p class="alert alert-danger">
                    ${msg}
                </p>
            %endfor
        %endif

        ## ${form | n}

        <h1> Edit Your Profile </h1>
        <div class="form-group" id="hi">
            <form action = "${request.route_url('edit_user')}" method = "POST" class = "inline-block" \
            onsubmit = "return confirm('Are you sure you want to update?\n\nIf field is left empty, there will be no changes made to that field')">
                <div>
                    <label>First Name:
                        <input type="text" class='form-control' name = "first_name" placeholder="${request.user.first_name.capitalize()}">
                    </label>
                
                    <label>Last Name:
                        <input type="text" class='form-control' name = "last_name" placeholder="${request.user.last_name.capitalize()}">
                    </label>
                </div>

                <div class='form-group'>
                    <label>Password:
                        <input type = "password" class='form-control' name = "password" placeholder = "Password">
                    </label>
                    <label>Confirm:
                        <input type = "password" class='form-control' name = "confirm_password" placeholder = "Confirm">
                    </label>
                </div>
                <div>
                    <div class='form-group'>
                        <input type="hidden" name="csrf_token" value="${get_csrf_token()}">
                        ## <div style="float:left">
                        ## <input name = 'login_submit' type = "submit" class = "btn btn-labeled btn-primary">
                        <button type="submit" value="Login" name = 'login_submit' class = "btn btn-labeled btn-success"><span class="btn-label"><i class="glyphicon glyphicon-ok"></i></span>submit</button>
                        <a href="${request.route_url('home')}"><button class = 'btn btn-danger btn-labeled'><span class="btn-label"><i class="fas fa-times"></i></span>Cancel</button></a>
                        ## </div>
                        ## <div style='float:right'>
                        ## <input name="Delete" id='delete' formaction = "${request.route_url('delete_user')}" type="submit" class="btn btn-danger" \
                        ## value="Delete ${request.user.username.capitalize()}" onclick = "return confirm('THIS WILL DELETE YOUR ACCOUNT ARE YOU SURE YOU WANT TO CONTINUE?');">
                        ## </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<div class="col-sm-3"></div>

