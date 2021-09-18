# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from tools.translate import _

class account_billing(osv.osv):

    _inherit = 'account.billing'
    _columns = {
        'is_mh_novat': fields.boolean('MH No-VAT', readonly=True, states={'draft': [('readonly', False)]}),
    }
    
    _defaults = {
        'is_mh_novat': lambda self,cr,uid,c: c.get('is_mh_novat',False),
    }
    
    # A complete overwrite method
    def recompute_billing_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, date, context=None):
        """
        Returns a dict that contains new values and context

        @param partner_id: latest value from user input for field partner_id
        @param args: other arguments
        @param context: context arguments, like lang, time zone

        @return: Returns a dict which contains new values, and context
        """
        def _remove_noise_in_o2m():
            """if the line is partially reconciled, then we must pay attention to display it only once and
                in the good o2m.
                This function returns True if the line is considered as noise and should not be displayed
            """
            if line.reconcile_partial_id:
                sign = 1
                if currency_id == line.currency_id.id:
                    if line.amount_residual_currency * sign <= 0:
                        return True
                else:
                    if line.amount_residual * sign <= 0:
                        return True
            return False

        if context is None:
            context = {}
        context_multi_currency = context.copy()
        if date:
            context_multi_currency.update({'date': date})

        currency_pool = self.pool.get('res.currency')
        move_line_pool = self.pool.get('account.move.line')
        partner_pool = self.pool.get('res.partner')
        journal_pool = self.pool.get('account.journal')
        line_pool = self.pool.get('account.billing.line')

        #set default values
        default = {
            'value': {'line_cr_ids': [] },
        }

        #drop existing lines
        line_ids = ids and line_pool.search(cr, uid, [('billing_id', '=', ids[0])]) or False
        if line_ids:
            line_pool.unlink(cr, uid, line_ids)

        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id
        account_id = False
        if journal.type in ('sale','sale_refund'):
            account_id = partner.property_account_receivable.id
        elif journal.type in ('purchase', 'purchase_refund','expense'):
            account_id = partner.property_account_payable.id
        else:
            account_id = journal.default_credit_account_id.id or journal.default_debit_account_id.id

        default['value']['account_id'] = account_id

        if journal.type not in ('cash', 'bank'):
            return default

        total_credit = price or 0.0
        account_type = 'receivable'

        if not context.get('move_line_ids', False):
            # kittiu change from using maturity date to new billing_date 
#             ids = move_line_pool.search(cr, uid, 
#                                         [('state','=','valid'), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id), 
#                                          '|',('date_maturity', '=', False),('date_maturity', '<=', date)], 
#                                         context=context)
            is_mh_novat = context.get('is_mh_novat', False)
            cr.execute('''select aml.id, ai.billing_date from account_move_line aml \
                            join account_invoice ai on aml.move_id = ai.move_id \
                            join account_account aa on aa.id = aml.account_id \
                            where aa.type = %s \
                            and aml.state = 'valid' \
                            and aml.reconcile_id is null \
                            and aml.partner_id = %s \
                            and (ai.billing_date <= %s or ai.billing_date is null) \
                            and ai.is_mh_novat = %s ''', (account_type, partner_id, date, is_mh_novat))
            # -- kittiu
            ids = map(lambda x: x[0], cr.fetchall())
        else:
            ids = context['move_line_ids']
        invoice_id = context.get('invoice_id', False)
        company_currency = journal.company_id.currency_id.id
        move_line_found = False

        #order the lines by most old first
        ids.reverse()
        account_move_lines = move_line_pool.browse(cr, uid, ids, context=context)

        #compute the total debit/credit and look for a matching open amount or invoice
        for line in account_move_lines:
            if _remove_noise_in_o2m():
                continue

            if invoice_id:
                if line.invoice.id == invoice_id:
                    #if the invoice linked to the billing line is equal to the invoice_id in context
                    #then we assign the amount on that line, whatever the other billing lines
                    move_line_found = line.id
                    break
            elif currency_id == company_currency:
                #otherwise treatments is the same but with other field names
                if line.amount_residual == price:
                    #if the amount residual is equal the amount billing, we assign it to that billing
                    #line, whatever the other billing lines
                    move_line_found = line.id
                    break
                #otherwise we will split the billing amount on each line (by most old first)
                total_credit += line.credit or 0.0
            elif currency_id == line.currency_id.id:
                if line.amount_residual_currency == price:
                    move_line_found = line.id
                    break
                total_credit += line.credit and line.amount_currency or 0.0

        #billing line creation
        for line in account_move_lines:

            if _remove_noise_in_o2m():
                continue

            if line.currency_id and currency_id==line.currency_id.id:
                amount_original = abs(line.amount_currency)
                amount_unreconciled = abs(line.amount_residual_currency)
            else:
                amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or 0.0)
                amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual))
            line_currency_id = line.currency_id and line.currency_id.id or company_currency
            rs = {
                'move_line_id':line.id,
                'type': line.credit and 'dr' or 'cr',
                # kitti
                #'reference':line.invoice.reference,
                'reference':line.invoice.number_mh_vat or line.invoice.number_mh_safe,
                # -- kitti
                'account_id':line.account_id.id,
                'amount_original': amount_original,
                'amount': (move_line_found == line.id) and min(abs(price), amount_unreconciled) or amount_unreconciled,
                'date_original':line.date,
                'date_due':line.date_maturity,
                'amount_unreconciled': amount_unreconciled,
                'currency_id': line_currency_id,
            }
            
            # Negate DR records
            if rs['type'] == 'dr':
                rs['amount_original'] = - rs['amount_original']
                rs['amount'] = - rs['amount']
                rs['amount_unreconciled'] = - rs['amount_unreconciled']

            if rs['amount_unreconciled'] == rs['amount']:
                rs['reconcile'] = True
            else:
                rs['reconcile'] = False

            default['value']['line_cr_ids'].append(rs)

#            if ttype == 'payment' and len(default['value']['line_cr_ids']) > 0:
#                default['value']['pre_line'] = 1
#            elif ttype == 'receipt' and len(default['value']['line_dr_ids']) > 0:
#                default['value']['pre_line'] = 1
            default['value']['billing_amount'] = self._compute_billing_amount(cr, uid, default['value']['line_cr_ids'], price)
        return default

    def validate_billing(self, cr, uid, ids, context=None):

        self.write(cr, uid, ids, { 'state': 'billed' })

        billings = self.browse(cr, uid, ids)
        for billing in billings:
            if not billing.number:
                is_cust_novat = billing.is_mh_novat or False
                if is_cust_novat: # No Vat
                    billing_number_novat = self.pool.get('ir.sequence').get(cr, uid, 'account.billing.novat') or False
                    self.write(cr, uid, billing.id, {'number': billing_number_novat})
                else: # VAT
                    billing_number_vat = self.pool.get('ir.sequence').get(cr, uid, 'account.billing.vat') or False
                    self.write(cr, uid, billing.id, {'number': billing_number_vat})  
                          
        self.message_post(cr, uid, ids, body=_('Billing is billed.'), context=context)
                    
        return True

account_billing()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
