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

from openerp.osv import osv, fields


class payment_register(osv.osv):
    _inherit = 'payment.register'
    
    _columns = {
        'is_cleared': fields.boolean('Cleared', readonly=True),
        'property_payment_term': fields.related('partner_id', 'property_payment_term', type='many2one', relation='account.payment.term', string='Credit Term', store=True, readonly=True),
    }
    _defaults = {
        'is_cleared': False
    }
    
    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        context.update({'bounce_check': True})  # Assume always bounce
        return super(payment_register, self).copy(cr, uid, id, default, context=context)

    def action_clear(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'is_cleared': False})
        
    def action_unclear(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'is_cleared': True})
        

payment_register()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
