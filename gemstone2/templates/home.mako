<%inherit file="layout.mako"/>
<div class="content">
  <section id="home">
    <div class="home-container">
    %if request.authenticated_userid is not None:

      <div class="contenedor">
			  <h1>Welcome ${request.user.first_name.capitalize()},<span>&#160;</span></h1>
	    </div>
      <div class = 'row'>
        <div class = 'col-md-7'><h2>Please visit the 'REPORTS' tab to view the latest reports</h2></div>
        <div class = 'col-md-5'><img class="logo img-responsive" id='arrowimg' src="${request.static_url('gemstone2:static/arrow.png')}" alt="pyramid web framework"></div>
      </div>
    %else:
      <h1><strong>GEMSTONE II</strong></h1>
      <h2>Investing for Growth</h2>
      ## </div>
    %endif
    </div>
  </section>
</div>
<div class="container">
  <div class="modal fade login" id="loginModal">
    <div class="modal-dialog login animated">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
          <h4 class="modal-title"><strong>Login</strong></h4>
          %if error:
            %for key, msg in error.items():
              <p class="alert alert-danger" style = 'margin-bottom : -10px; margin-top : 10px'>
                ${msg}
              </p>
            %endfor
          %endif
        </div>
        
        <div class="modal-body">
          <div class="box">
            <div class="content">


              ###### THIS IS FOR LOGIN USING SOCIAL MEDIA ######

              ## <div class="social">
              ##             <a class="circle github" href="#">
              ##                 <i class="fa fa-github fa-fw"></i>
              ##             </a>
              ##             <a id="google_login" class="circle google" href="#">
              ##                 <i class="fa fa-google-plus fa-fw"></i>
              ##             </a>
              ##             <a id="facebook_login" class="circle facebook" href="#">
              ##                 <i class="fa fa-facebook fa-fw"></i>
              ##             </a>
              ##         </div>
              ##         <div class="division">
              ##             <div class="line l"></div>
              ##               <span>or</span>
              ##             <div class="line r"></div>
              ##         </div>


              <div class="form loginBox">
                <form method="POST" action="${request.route_url('login')}" accept-charset="UTF-8">
                <input id="email" class="form-control" type="text" placeholder="Username" name="username">
                <input id="password" class="form-control" type="password" placeholder="Password" name="password">
                <input class="btn btn-default btn-login" type="submit" value="Login" name = 'login_submit'>
                </form>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
<div>
%if request.authenticated_userid is None:
  <script type="text/javascript">
      $(document).ready(function(){
          openLoginModal();
      });
  </script>
%endif