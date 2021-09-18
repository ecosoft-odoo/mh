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

TAX_RATE = 6.54205608

class sale_order(osv.osv):

    _inherit = 'sale.order'
    _columns = {
        'is_mh_novat': fields.boolean('MH No-VAT', readonly=True, states={'draft': [('readonly', False)]}),
        'is_mh_vat': fields.boolean('MH VAT', readonly=True, states={'draft': [('readonly', False)]}),
    }
    
    _defaults = {
        'is_mh_novat': lambda self,cr,uid,c: c.get('is_mh_novat',False),
        'is_mh_vat': lambda self,cr,uid,c: c.get('is_mh_vat',False),
        # If MH VAT, Discount % = 7/100 = 6.54%
        'add_disc': lambda self,cr,uid,c: c.get('is_mh_vat',False) and TAX_RATE or 0.0,
    }
    
    def is_mh_vat_change(self, cr, uid, ids, is_mh_vat, is_mh_novat, context=None):
        if is_mh_novat and is_mh_vat:
            is_mh_novat = not is_mh_vat
        return {'value':{'is_mh_vat': is_mh_vat,
                         'is_mh_novat': is_mh_novat,
                         'add_disc': is_mh_vat and TAX_RATE or 0.0}}  
    
    def is_mh_novat_change(self, cr, uid, ids, is_mh_vat, is_mh_novat, context=None):
        if is_mh_vat and is_mh_novat:
            is_mh_vat = not is_mh_novat
        return {'value':{'is_mh_vat': is_mh_vat,
                         'is_mh_novat': is_mh_novat,
                         'add_disc': is_mh_vat and TAX_RATE or 0.0}}
    
#    def create(self, cr, uid, vals, context=None):
#        is_cust_novat = context.get('is_mh_novat',False)
#        if is_cust_novat and vals.get('name','/')=='/':
#            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order.novat') or '/'
#        return super(sale_order, self).create(cr, uid, vals, context=context)

    def _make_invoice(self, cr, uid, order, lines, context=None):
        """Add a VAT, No-VAT flag into Invoice Created from Sale Order
        """
        inv_obj = self.pool.get('account.invoice')
        # create the invoice
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
        # modify the invoice
        inv_obj.write(cr, uid, [inv_id], {'is_mh_vat': order.is_mh_vat or False,
                                          'is_mh_novat': order.is_mh_novat or False
                                          }, context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('is_mh_novat', False):
            line_obj = self.pool.get('sale.order.line')
            line_ids = line_obj.search(cr, uid, [('order_id', 'in', ids)])
            line_obj.write(cr, uid, line_ids, {'tax_id': [(6,0,[])]})
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)
    
sale_order()

class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id,
                                                                lang, update_tax, date_order, packaging, fiscal_position, flag, context)

        # If called from Sales Order (No-VAT), no tax.
        if context.get('is_mh_novat',False):
            res['value'].update({'tax_id': False})

        return res

sale_order_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
