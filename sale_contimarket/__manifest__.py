# -*- coding: utf-8 -*-
{
    'name': "sale_contimarket",

    'summary': """
        Integración con la API de ContiMarket""",


    'author': "joonza",
    'website': "http://www.joonza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/api_views.xml',
        'views/product_views.xml',
        'data/actions.xml'
        # 'views/templates.xml',
    ],
}
