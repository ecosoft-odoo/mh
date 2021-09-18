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

class sale_order(osv.osv):

    _inherit = 'sale.order'
    
    _columns = {
        'po_reference': fields.char('PO Reference', size=64),
        'po_date': fields.date('PO Date'),
        'partner_name': fields.char('Partner Name'),
        'name_phone': fields.char('Name/Phone'),
    }
    _order = 'id desc'

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        partner = self.pool.get('res.partner').browse(cr, uid, part)
        if partner:
            res['value'].update({'partner_name': partner.name})
        else:
            res['value'].update({'partner_name': False})
        return res
    
    def _make_invoice(self, cr, uid, order, lines, context=None):
        """Add a PO Reference and PO Date into Invoice
        """
        inv_obj = self.pool.get('account.invoice')
        # create the invoice
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
        # modify the invoice
        inv_obj.write(cr, uid, [inv_id], {'po_reference': order.po_reference or False,
                                          'po_date': order.po_date or False
                                          }, context)
        return inv_id

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
