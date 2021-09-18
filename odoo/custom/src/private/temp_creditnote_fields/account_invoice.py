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

    _inherit = "account.invoice"
    
    _columns = {
        'tmp_ref_invoice': fields.char('อ้างถึง'),
        'tmp_old_amt': fields.float('มุลค่าเดิม'),
        'tmp_new_amt': fields.float('มูลค่าที่ถูกต้อง'),
        'tmp_diff_amt': fields.float('ผลต่าง'),
        'tmp_ref_date': fields.date('วันที่'),
    }
    
account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
