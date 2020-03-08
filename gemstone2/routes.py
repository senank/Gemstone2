def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('front', '/')
    config.add_route('home', '/home')
    config.add_route('add_report', '/add')
