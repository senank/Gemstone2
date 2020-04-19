from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.csrf import new_csrf_token

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..security import check_password, hash_password

from ..models import User
from ..models import Report

import colander
import deform


@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='GET', permission = 'create')
def create(request):
    return {
        'project': 'Gemstone II',
        'page_title': 'Create'
    }

@view_config(route_name='create', renderer='../templates/create_acc.mako', request_method='POST', permission = 'create')
def create_acc(request):
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    valid = True

    try:
        
        form_username = request.POST.get('username')
        if form_username:
            db_username = request.dbsession.query(User).filter(User.username == form_username).first()
            if db_username is None:
                form_data['username'] = form_username
            else:
                valid = False
                error['username_taken'] = 'That username has been taken'
        else:
            valid = False
            error['username_invalid'] = 'Please enter a valid username'

        form_first_name = request.POST.get('first_name')
        if form_first_name:
            form_data['first_name'] = form_first_name
        else:
            form_data['first_name'] = 'User'

        form_last_name = request.POST.get('last_name')
        if form_first_name:
            form_data['last_name'] = form_last_name
        else:
            form_data['last_name'] = '___'
        
        form_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if form_password:
            if form_password == confirm_password:
                chars = True
                for char in forbidden:
                    if char in form_password:
                        error['password'] = \
                            'Please avoid the following:   {  ,  }  ,  |  ,  \'  ,  ^  ,  ~  ,  [ , ] , ` '
                        chars = False
                        valid = False
                if chars:
                    form_data['password'] = form_password
            elif form_password != confirm_password:
                error['nomatch'] = 'Password did not match'
                valid = False
        elif confirm_password:
            error['nopassword'] = 'Please enter a password'
            valid = False
        else:
            form_data['password'] = 'g123456'
        
        form_permission = request.POST.get('permission')
        if form_permission in ['admin', 'viewer']:
            form_data['permission'] = form_permission
        else:
            error['invalidpermission'] = 'Please select from the following options'            
    except (ValueError, TypeError, KeyError) as e:
        valid = False

    if valid:
        new_user = User()
        new_user.username = form_data['username'].lower()

        password_hashed = hash_password(form_data['password'])
        new_user.password = password_hashed

        new_user.permissions = form_data['permission']
        new_user.first_name = form_data['first_name']
        new_user.last_name = form_data['last_name']

        # new_user.picture = 'avatar.png'

        request.dbsession.add(new_user)
        request.dbsession.flush()
        new_csrf_token(request)
        return HTTPFound(location=request.route_url('user_list'))
    else:
        return {
            'project': 'Gemstone II',
            'page_title': 'Create',
            'error': error,
            }

@view_config(route_name='edit_user', renderer = "../templates/edit_user.mako",\
     request_method='GET', permission = 'logged')
def edit(request):
    
    # id_ = request.user.user_id
    # user = request.dbsession.query(User).filter_by(user_id = id_).first()

    # schema = colander.SchemaNode(colander.Mapping(), 
    #     colander.SchemaNode(colander.String(), 
    #     name = 'csrf_token',
    #     default=deferred_csrf_default,
    #     widget=deform.widget.HiddenWidget(),
    #     ).bind(request=request))

    # class MemoryTmpStore(dict):
    #     """ Instances of this class implement the
    #     :class:`deform.interfaces.FileUploadTempStore` interface"""

    #     def preview_url(self, uid):
    #         return None
    
    # tmpstore = MemoryTmpStore()        
    # schema.add(colander.SchemaNode(
    #     deform.FileData(),
    #     widget = deform.widget.FileUploadWidget(tmpstore),
    #     name = 'upload profile picture',
    #     missing = None
    #     ))

    # myform = deform.Form(schema, buttons = ('set',))
    # form = myform.render()
    
    return {
        'project': 'Gemstone II',
        'page_title': 'Edit',
        # 'form' : form
    }


@view_config(route_name='edit_user', renderer = "../templates/edit_user.mako", request_method='POST', permission = 'logged')
def edit_handler(request):
    form_data = {}
    error = {}
    forbidden = ["{","}", "|", "\'","^", "~", "[", "]", "`"]
    valid = True

    id_ = request.user.user_id
    user = request.dbsession.query(User).filter_by(user_id = id_).first()
    

    try:
        #Form first_name checker
        form_first_name = request.POST.get('first_name')
        if form_first_name:
            form_data['first_name'] = form_first_name
            
        else:
            form_data['first_name'] = user.first_name

        #Form last_name checker
        form_last_name = request.POST.get('last_name')
        if form_last_name:
            form_data['last_name'] = form_last_name
            
        else:
            form_data['last_name'] = user.last_name

        #form password and confirm password checker
        form_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if form_password:
            if (form_password == confirm_password):
                chars = True    
                for char in forbidden:
                    if char in form_password:
                        error['password'] = \
                             'Please avoid the following:   {  ,  }  ,  |  ,  \'  ,  ^  ,  ~  ,  [ , ] , ` '
                        chars = False
                        valid = False
                if chars:
                    password = hash_password(form_password)
                    form_data['password'] = password
            elif (form_password != confirm_password):
                error['nomatch'] = 'Password did not match'
                valid = False
        elif confirm_password != '':
            error['nopassword'] = 'Please enter a password'
            valid = False
        else:
            form_data['password'] = user.password
            
    except (ValueError, TypeError, KeyError):
        valid = False
    
    if valid:
        user.first_name = form_data['first_name'].lower()
        user.last_name = form_data['last_name'].lower()
        user.password = form_data['password']

        request.dbsession.add(user)
        return HTTPFound(location=request.route_url('home'))

    return {
        'project': 'Gemstone II',
        'page_title': 'Edit',
        'error': error,
    }


@view_config(route_name='login', renderer = "../templates/home.mako", request_method='GET', require_csrf=False)
def login(request):
    return {
        'project': 'Gemstone II',
        'page_title': 'Login',
    }

@view_config(route_name='login', renderer = "../templates/home.mako", request_method='POST', require_csrf=False)
def login_handler(request):
    valid = True
    error = {}

    form_username = request.POST.get('username').lower()
    form_password = request.POST.get('password')
    
    db_user = request.dbsession.query(User).filter_by(username = form_username).first()
    
    if db_user and check_password(form_password, db_user.password):
        permissions = db_user.permissions
        id_ = db_user.user_id
        headers = remember(request, id_)
        new_csrf_token(request)
        return HTTPFound(location=request.route_url('home'), headers=headers)
 
    error['incorrect'] = 'Check username or password'
    return {
            'error': error,
            'page_title': 'Login',
            'project': 'Gemstone II',
            }

@view_config(route_name='logout', require_csrf=False)
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name = 'user_list', renderer = "../templates/user_list.mako", permission = 'user_list')
def user_list(request):
    user = request.user
    if user is not None:
        try:
            id_ = user.user_id
            auth_ = user.permissions
            query = request.dbsession.query(User)
            users = query.order_by(User.username.desc())
        except:
            log.exception(ex)
            return Response(db_err_msg, content_type = 'text/plain', status = 500)
    else:
        raise HTTPForbidden

    return{
        'users' : users,
        'page_title' : 'Gemstone 2'
    }

@view_config(route_name = 'user_list_edit', renderer = '../templates/user_list_edit.mako', permission = "edit_user")
def user_list_edit(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    user = request.dbsession.query(User).filter(User.user_id == id_).first()
    current = {
        'username' : user.username,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'permission' : user.permissions
    }

    ### FORM BUILDING ###
    #CSRF
    schema = colander.SchemaNode(colander.Mapping(), 
        colander.SchemaNode(colander.String(), 
        name = 'csrf_token',
        default=deferred_csrf_default,
        widget=deform.widget.HiddenWidget(),
        ).bind(request=request))

    #Username    
    schema.add(colander.SchemaNode(colander.String(),
        name = 'username',
        default = current['username'],
        validator = colander.Length(min = 1, max = 24)
        ))

    #Full Name
    schema.add(colander.SchemaNode(colander.String(),
        name = 'first_name',
        validator = colander.Length(min = 1, max = 24),
        default = current['first_name']
        ))

    schema.add(colander.SchemaNode(colander.String(),
        name = 'last_name',
        validator = colander.Length(min = 1, max = 24),
        default = current['last_name']
        ))

    #Permission
    schema.add(colander.SchemaNode(colander.String(),
        widget = deform.widget.SelectWidget(values=((('admin','admin'),('viewer','viewer'),))),
        name = 'permission',
        default = current['permission']))
    
    myform = deform.Form(schema, buttons = ('submit', 'delete', 'cancel',))
    form = myform.render()

    if 'submit' in request.POST:
        control = request.params.items()

        try:
            form_data = myform.validate(control)
            
        except deform.exception.ValidationFailure as e:
            return {
                'user' : user,
                'id' : id_,
                'form' : e.render(),
                }

        user.username = form_data['username']
        user.first_name = form_data['first_name']
        user.last_name = form_data['last_name']
        user.permissions = form_data['permission']
        return HTTPFound(location = request.route_url('user_list'))

    if 'delete' in request.POST:
        request.dbsession.delete(user)
        request.dbsession.flush()
        return HTTPFound(location = request.route_url('user_list'))


    if 'cancel' in request.POST:
        return HTTPFound(location = request.route_url('user_list'))

    return{
        'id_' : id_,
        'form' : form
    }



@view_config(route_name='reset_user', permission = "reset_user")
def reset_user(request):
    try:
        id_ = int(request.matchdict['id'])
    except (ValueError, TypeError):
        raise HTTPNotFound
    
    user = request.dbsession.query(User).filter(User.user_id == id_).first()
    user.password = hash_password('g123456')
    return HTTPFound(location = request.route_url('user_list'))