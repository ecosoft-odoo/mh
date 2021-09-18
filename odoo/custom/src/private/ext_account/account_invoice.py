# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

class account_invoice(osv.osv):

    def _is_bangkok_customer(self, cursor, user, ids, name, arg, context=None):
        res = {}
        cursor.execute("select inv.id, (case when bkk.id is not null then true else false end) is_bkk \
                        from account_invoice inv left outer join \
                        (select distinct p.id from res_partner p, res_partner_res_partner_category_rel r \
                        where r.partner_id = p.id and r.category_id in \
                        (select id from res_partner_category categ where name like %s or name ilike %s)) bkk \
                        on inv.partner_id = bkk.id \
                        where inv.id in %s", ('%กรุงเทพ%', '%bangkok%', tuple(ids),))
        rs = cursor.fetchall()
        for r in rs:
            res[r[0]] = r[1]
        return res    
    
    _inherit = "account.invoice"
    
    _columns = {
        'plate_id': fields.many2one('vehicle.plate', 'Car Plate'),
        'driver_id': fields.many2one('vehicle.driver', 'Car Driver'),
        'write_uid': fields.many2one('res.users', 'Modified By',readonly=True),
        'is_bangkok_customer': fields.function(_is_bangkok_customer, string='Is Bangkok?', type='boolean', store=True),
        'no_stock_return': fields.boolean('No Stock Return')
    }
    

    def init(self, cr):
        cr.execute("update account_invoice ai set is_bangkok_customer = \
                    (select (case when bkk.id is not null then true else false end) \
                    from account_invoice inv left outer join \
                    (select distinct p.id from res_partner p, res_partner_res_partner_category_rel r \
                    where r.partner_id = p.id and r.category_id in \
                    (select id from res_partner_category categ where name like '%กรุงเทพฯ%' or name ilike '%bangkok%')) bkk \
                    on inv.partner_id = bkk.id where inv.id = ai.id) where ai.is_bangkok_customer is null")
        
account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
