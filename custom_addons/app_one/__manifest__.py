{
    'name': "app_one",
    'author': "Ahmed Elhabashy",
    'category': "Custom",
    'version': "17.0.1.0.0",
    'depends': ['base'],
    'data': [
          'security/ir.model.access.csv',
         'views/property_view.xml',
         'views/agent_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/base_menu.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,

}