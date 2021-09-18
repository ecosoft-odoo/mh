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

MH_SAFE_MAX_INV_NO = 200

class account_invoice(osv.osv):
    
    def _number_mh_safe(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cursor, user, ids, context=context):
            res[invoice.id] = ''
            if invoice.number_mh:
                is_debitnote = invoice.journal_id.type in ('sale_debitnote', 'purchase_debitnote')
                if invoice.type in ('out_invoice','in_invoice') and not is_debitnote:
                    res[invoice.id] = (int(invoice.number_mh) % MH_SAFE_MAX_INV_NO) or MH_SAFE_MAX_INV_NO
                elif invoice.type in ('out_invoice','in_invoice') and is_debitnote:
                    res[invoice.id] = invoice.number_mh      
                elif invoice.type in ('out_refund','in_refund'):
                    res[invoice.id] = invoice.number_mh
        return res
    
    _inherit = 'account.invoice'
    _columns = {
        'billing_date': fields.date('Billing Date', select=True),
        'is_mh_novat': fields.boolean('No-VAT', readonly=True),
        'is_mh_vat': fields.boolean('VAT', readonly=True),
        'number_mh': fields.char('MH Internal No.', readonly=True),
        'number_mh_safe': fields.function(_number_mh_safe, string='MH No.', type='char', select=True, store=True, readonly=True),
        'number_mh_vat': fields.char('MH VAT No.', readonly=True),
    }
    
    def invoice_validate(self, cr, uid, ids, context=None):
        invoices = self.browse(cr, uid, ids)
        for invoice in invoices:
            if invoice.type in ('in_invoice','in_refund'): # not applicable for purchase
                continue
            is_cust_novat = invoice.is_mh_novat or False
            if is_cust_novat: # No Vat
                if not invoice.number_mh: # only when number not there yet.
                    if invoice.type == 'out_invoice' and not invoice.is_debitnote:
                        number_mh = self.pool.get('ir.sequence').get(cr, uid, 'account.invoice.novat') or False
                    elif invoice.type == 'out_invoice' and invoice.is_debitnote:
                        number_mh = self.pool.get('ir.sequence').get(cr, uid, 'account.debitnote.novat') or False
                    elif invoice.type == 'out_refund':
                        number_mh = self.pool.get('ir.sequence').get(cr, uid, 'account.refund.novat') or False
                    self.write(cr, uid, invoice.id, {'number_mh': number_mh})
            else: # VAT
                if not invoice.number_mh_vat: # only when number not there yet.
                    if invoice.type == 'out_invoice'and not invoice.is_debitnote:
                        number_mh_vat = self.pool.get('ir.sequence').get(cr, uid, 'account.invoice.vat') or False
                    elif invoice.type == 'out_invoice'and invoice.is_debitnote:
                        number_mh_vat = self.pool.get('ir.sequence').get(cr, uid, 'account.debitnote.vat') or False                        
                    elif invoice.type == 'out_refund':
                        number_mh_vat = self.pool.get('ir.sequence').get(cr, uid, 'account.refund.vat') or False
                    self.write(cr, uid, invoice.id, {'number_mh_vat': number_mh_vat})
        
        return super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)
    
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'number_mh':False,
            'number_mh_safe':False,
            'number_mh_vat':False,
        })
        return super(account_invoice, self).copy(cr, uid, id, default, context)
        
    def _prepare_refund(self, cr, uid, invoice, date=None, period_id=None, description=None, journal_id=None, context=None):
        invoice_data = super(account_invoice, self)._prepare_refund(cr, uid, invoice, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        invoice_data.update({
            'is_mh_vat': invoice.is_mh_vat,
            'is_mh_novat': invoice.is_mh_novat,
            'add_disc': invoice.add_disc
        })
        return invoice_data
    
    def _prepare_debitnote(self, cr, uid, invoice, date=None, period_id=None, description=None, journal_id=None, context=None):
        invoice_data = super(account_invoice, self)._prepare_debitnote(cr, uid, invoice, date=date, period_id=period_id, description=description, journal_id=journal_id, context=context)
        invoice_data.update({
            'is_mh_vat': invoice.is_mh_vat,
            'is_mh_novat': invoice.is_mh_novat,
            'add_disc': invoice.add_disc
        })
        return invoice_data
        
account_invoice()    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
