def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('create', '/create')
    config.add_route('edit_user', '/edit')

    config.add_route('report_list', '/reports')

    config.add_route('new_report', '/reports/add')
    config.add_route('edit_report', '/reports/edit/{id}')
    config.add_route('save_report', '/reports/edit/{id}/save')
    config.add_route('create_pdf', '/reports/edit/{id}/create')
    config.add_route('publish_report', '/reports/publish')
    config.add_route('delete_report', '/reports/delete/{id}')
    
    config.add_route('pdf_tester', '/reports/pdf_tester/{id}')

    config.add_route('kpi_list', '/reports/kpi')
    config.add_route('kpi_add', '/reports/kpi/add')
    config.add_route('kpi_edit', '/reports/kpi/edit/{id}')
    config.add_route('kpi_edit_save', 'reports/kpi/edit/{id}/save')
    config.add_route('kpi_show', '/reports/kpi/show')
    config.add_route('kpi_delete', '/reports/kpi/delete/{id}')

    config.add_route('user_list', '/users')
    config.add_route('user_list_edit', '/users/edit/{id}')
    config.add_route('reset_user', '/users/reset/{id}')
