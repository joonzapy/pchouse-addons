# -*- coding: utf-8 -*-
{
    'name': "pchouse_stock",

    'summary': """
        Gestión personalizada del inventario para pchouse""",

    'description': """
        Módulo personalizado para la gestión avanzada de inventario:
- Creación de un nuevo grupo de usuarios: "Gestión de Inventario".
- Modificación de permisos para acciones específicas como el botón "Devolver" en transferencias de stock.

Este módulo está diseñado para satisfacer las necesidades específicas de la empresa, mejorando el control y la trazabilidad del inventario.
    """,

    'author': "joonza",
    'website': "http://www.joonza.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.1.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/pchouse_stock_groups.xml',
        'views/views.xml',
    ],
}
