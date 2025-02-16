# -*- coding: utf-8 -*-
{
    'name': "pchouse_account",

    'summary': """
        Muestra el total del costo en la lista de facturas de cliente""",

    'description': """
        Long description of module's purpose
    """,

    'author': "joonza",
    'website': "http://www.joonza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '14.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'data/account_groups.xml',
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/account_invoice_report_views.xml'
    ],
}
