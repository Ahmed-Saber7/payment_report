# -*- coding: utf-8 -*-
{
    'name': "payment_receipt_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        This module allow To Make Customization For Payment Report and add feature that create sequence by save button not confirm button.and to convert amount number to words and showing in report.
    """,

    'author': "Ahmed Saber",
    'website': "http://www.marketme-it.com/",
    'images': ['static/description/new_logo.png'],


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_payment_methods'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
