def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('create', '/create')
    config.add_route('edit_user', '/edit')
    config.add_route('delete_user', '/delete')
    
    config.add_route('report_list', '/reports')
    config.add_route('edit_report', '/reports/edit/{id}')
    config.add_route('save_report', '/reports/edit/{id}/save')
    config.add_route('publish_report', '/reports/edit/{id}/publish')