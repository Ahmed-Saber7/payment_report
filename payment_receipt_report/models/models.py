# -*- coding: utf-8 -*-

from num2words import num2words
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    check_date = fields.Date(string="Check Date", required=False, )
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_text")

    @api.multi
    def amount_to_text(self):
        self.text_amount = self.currency_id.amount_to_text(self.amount)

    @api.onchange('payment_method')
    def filter_journals(self):
        for rec in self:
            if rec.payment_method in ['transfer_bank', 'check', 'pay']:
                return {
                    'domain': {'journal_id': [('type', '=', 'bank')]}
                }
            if rec.payment_method == 'cash':
                return {
                    'domain': {'journal_id': [('type', '=', 'cash')]}
                }

    @api.model
    def create(self, vals):
        payment_type = vals.get('payment_type', False)
        partner_type = vals.get('partner_type', False)
        payment_date = vals.get('payment_date', False)
        if payment_type == 'transfer':
            sequence_code = 'account.payment.transfer'
        else:
            if partner_type == 'customer':
                if payment_type == 'inbound':
                    sequence_code = 'account.payment.customer.invoice'
                    print(sequence_code)
                if payment_type == 'outbound':
                    sequence_code = 'account.payment.customer.refund'
            if partner_type == 'supplier':
                if payment_type == 'inbound':
                    sequence_code = 'account.payment.supplier.refund'
                if payment_type == 'outbound':
                    sequence_code = 'account.payment.supplier.invoice'
        vals.update({'name': self.env['ir.sequence'].with_context(ir_sequence_date=payment_date).next_by_code(
            sequence_code)})
        return super(AccountPayment, self).create(vals)
    @api.multi
    def post(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))
            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(
                    lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name
            rec.write({'state': 'posted', 'move_name': persist_move_name})
        return True
