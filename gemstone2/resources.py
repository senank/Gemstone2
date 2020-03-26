from pyramid.security import Allow, Everyone

class Root(object):
    def __acl__(self):
        return [
            (Allow, 'admin', 'edit_report'),
            (Allow, 'admin', 'save_report'),
            (Allow, 'admin', 'add'),
            (Allow, 'admin', 'publish'),
            (Allow, 'admin', 'delete_report'),
            (Allow, 'admin', 'create'),
            (Allow, 'admin', 'edit_user'),
            (Allow, 'admin', 'delete_user'),
            (Allow, 'admin', 'create_pdf'),
            (Allow, 'admin', 'view'),
            (Allow, 'admin', 'kpi_list'),
            (Allow, 'admin', 'kpi_edit'),
            (Allow, 'admin', 'logged'),
            (Allow, 'admin', 'user_list'),

            (Allow, 'viewer', 'logged'),
            (Allow, 'viewer', 'view')]
               

    def __init__(self, request):
        pass