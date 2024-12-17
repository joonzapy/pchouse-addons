# -*- coding: utf-8 -*-
{
    'name': "l10n_py_selfprinter",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "joonza",
    'website': "http://www.joonza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'talonario_py'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/invoice_report_autoprint.xml',
        'views/stamping_views.xml',
        'views/talonario_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
