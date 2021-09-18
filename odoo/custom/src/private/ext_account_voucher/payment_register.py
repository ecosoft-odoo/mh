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
from openerp.osv import osv, fields
from tools.translate import _


class payment_register(osv.osv):

    def _is_mh_novat(self, cursor, user, ids, name, arg, context=None):
        res = {}
        cursor.execute('select pr1.id, \
                        (select (select distinct(is_mh_novat) from account_invoice where move_id in \
                        (select move_id from account_move_line where id in \
                        (select move_line_id from account_voucher_line where voucher_id = av.id \
                        )) limit 1) as is_mh_novat from payment_register pr \
                        join account_voucher av on av.id = pr.voucher_id \
                        AND pr.id = pr1.id) is_mh_novat \
                        from payment_register pr1 where pr1.id in %s',
                        (tuple(ids),))
        for id, is_mh_novat in cursor.fetchall():
            res[id] = is_mh_novat
        return res

    def _is_bangkok_customer(self, cursor, user, ids, name, arg, context=None):
        res = {}
        cursor.execute("select pr.id, (case when bkk.id is not null then true else false end) is_bkk \
                        from payment_register pr left outer join \
                        (select distinct p.id from res_partner p, res_partner_res_partner_category_rel r \
                        where r.partner_id = p.id and r.category_id in \
                        (select id from res_partner_category categ where name like %s or name ilike %s)) bkk \
                        on pr.partner_id = bkk.id \
                        where pr.id in %s", ('%กรุงเทพ%', '%bangkok%', tuple(ids),))
        rs = cursor.fetchall()
        for r in rs:
            res[r[0]] = r[1]
        return res

    def _is_bangkok(self, cursor, user, ids, name, arg, context=None):
        res = dict.fromkeys(ids, False)
        for pay in self.browse(cursor, user, ids, context=context):
            res[pay.id] = pay.is_bangkok_customer and 'Yes' or 'No'
        return res

    def _vat_novat(self, cursor, user, ids, name, arg, context=None):
        res = dict.fromkeys(ids, False)
        for pay in self.browse(cursor, user, ids, context=context):
            res[pay.id] = pay.is_mh_novat and 'NO-VAT' or 'VAT'
        return res

    _inherit = 'payment.register'

    _columns = {
        'is_mh_novat': fields.function(_is_mh_novat, string='No-VAT', type='boolean', store=True),
        'is_bangkok_customer': fields.function(_is_bangkok_customer, string='Is Bangkok?', type='boolean', store=True),
        'is_bangkok_label': fields.function(_is_bangkok, string='Bangkok?', type='char', size=5, readonly=True),
        'vat_novat_label': fields.function(_vat_novat, string='VAT/No-VAT', type='char', size=7, readonly=True)
    }

    def init(self, cr):
        # Update is_bangkok_customer
        cr.execute("update payment_register pr set is_bangkok_customer = \
                    (select (case when bkk.id is not null then true else false end) \
                    from payment_register pr1 left outer join \
                    (select distinct p.id from res_partner p, res_partner_res_partner_category_rel r \
                    where r.partner_id = p.id and r.category_id in \
                    (select id from res_partner_category categ where name like '%กรุงเทพ%' or name ilike '%bangkok%')) bkk \
                    on pr1.partner_id = bkk.id where pr1.id = pr.id) where pr.is_bangkok_customer is null")
        # update is_mh_novat
        cr.execute("update payment_register pr1 set is_mh_novat = \
                    (select (select distinct(is_mh_novat) from account_invoice where move_id in \
                    (select move_id from account_move_line where id in \
                    (select move_line_id from account_voucher_line where voucher_id = av.id \
                    )) limit 1) as is_mh_novat from payment_register pr \
                    join account_voucher av on av.id = pr.voucher_id \
                    AND pr.id = pr1.id \
                    ) where is_mh_novat is Null")

payment_register()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
