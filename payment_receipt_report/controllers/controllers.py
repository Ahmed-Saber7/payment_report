# -*- coding: utf-8 -*-
from odoo import http

# class ReportsUpdates(http.Controller):
#     @http.route('/payment_receipt_report/payment_receipt_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_receipt_report/payment_receipt_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_receipt_report.listing', {
#             'root': '/payment_receipt_report/payment_receipt_report',
#             'objects': http.request.env['payment_receipt_report.payment_receipt_report'].search([]),
#         })

#     @http.route('/payment_receipt_report/payment_receipt_report/objects/<model("payment_receipt_report.payment_receipt_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_receipt_report.object', {
#             'object': obj
#         })