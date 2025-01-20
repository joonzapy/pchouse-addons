# -*- coding: utf-8 -*-
{
    'name': "pchouse_sale",

    'summary': """
        Desbloquea el campo 'precio unitario' en el presupuesto/pedido de venta.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "joonza",
    'website': "http://www.joonza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line_views.xml',
        'views/product_pricelist_views.xml'
    ],
}
