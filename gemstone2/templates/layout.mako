<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="pyramid web application">
    <meta name="author" content="Pylons Project">
    <link rel="shortcut icon" href="${request.static_url('gemstone2:static/pyramid-16x16.png')}">

    <title>Gemstone II</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('gemstone2:static/theme.css')}" rel="stylesheet">

    <!-- HTML5 shiv and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js" integrity="sha384-0s5Pv64cNZJieYFkXYOTId2HMA2Lfb6q2nAcx2n0RTLUnCAoTTsS0nKEO27XyKcY" crossorigin="anonymous"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js" integrity="sha384-ZoaMbDF+4LeFxg6WdScQ9nnR1QC2MIRxA1O9KWEXQwns1G8UNyIEZIQidzb0T1fo" crossorigin="anonymous"></script>
    <![endif]-->
  </head>

  <body>
    <nav>
      <ul>
        ## <li><a href="${request.route_url('home')}">Home</a></li>
        % if request.authenticated_userid is not None:
          <li>GEMSTONE II</li>
          <li><a href="${request.route_url('report_list')}">Reports</a></li>
          ## <li><a href="${request.route_url('edit_user')}">${request.user.username}</a></li>
          <li><a href="${request.route_url('logout')}">logout</a></li>
        %else:
          <li><a href="${request.route_url('login')}">login</a></li>
          ## <li><a href="${request.route_url('create')}">Create Account</a></li>

        %endif
      </ul>
    </nav>
    <div class="starter-template">
      <div class="container">
        <div class="row">
          ## <div class="col-md-2">
          ##   <img class="logo img-responsive" src="${request.static_url('gemstone2:static/pyramid.png') }" alt="pyramid web framework">
          ## </div>
          ${ next.body() }
        </div>
        <div class="row">
          <div class="links">
            
          </div>
        </div>
        <div class="row">
          <div class="copyright">
            ## Copyright &copy; Pylons Project
          </div>
        </div>
      </div>
    </div>


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ=" crossorigin="anonymous"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </body>
</html>

