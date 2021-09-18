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

import netsvc
from osv import osv, fields
from tools.translate import _

class sale_order(osv.osv):
    
    _inherit = 'sale.order'
    _columns = {
        'write_date': fields.datetime('Date Modified', readonly=True),
        'write_uid':  fields.many2one('res.users', 'Last Modification User', readonly=True),
        'create_date': fields.datetime('Date Created', readonly=True),
        'create_uid':  fields.many2one('res.users', 'Creator', readonly=True),    
    }    
    
    def send_mail_confirm_order_to_sale(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        # Send email with template    
        template = self.pool.get('ir.model.data').get_object(cr, uid, 'ext_sale_mail', 'confirm_order_to_sale')
        for order in self.browse(cr, uid, ids, context):
            if order.user_id and order.user_id.notification_email_send != 'none' and order.user_id.email:
                self.pool.get('email.template').send_mail(cr, uid, template.id, order.id, False, context=context)
        return True

    def action_button_confirm(self, cr, uid, ids, context=None):
        super(sale_order,self).action_button_confirm(cr, uid, ids, context=context)
        # Also send email to sales person
        self.send_mail_confirm_order_to_sale(cr, uid, ids, context=context)
        
sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
