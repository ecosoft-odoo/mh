# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2012-2012 Camptocamp (<http://www.camptocamp.at>)
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

# FIXME remove logger lines or change to debug
 
from openerp.osv import fields, osv
from openerp import netsvc

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def action_wait(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids):
            products = False
            for line in o.order_line:
                if line.product_id.type in ['product', 'consu']:
                    products = True
            if o.order_policy == 'picking' and not products:
                self.write(cr, uid, o.id, {'order_policy' : 'manual'})
        return super(sale_order,self).action_wait(cr, uid, ids, context)

sale_order()
    


