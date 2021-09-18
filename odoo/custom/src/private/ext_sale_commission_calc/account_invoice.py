# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'
    _columns = {
        'promo_code': fields.many2one(
            'promo.code', 'Promo Code',
            domain="[('product_id', '=', product_id)]"),
    }

account_invoice_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
