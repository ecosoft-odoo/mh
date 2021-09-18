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
from openerp.tools.translate import _

class account_invoice(osv.osv):
    
    _inherit = 'account.voucher'
    
    _columns = {
        'printed': fields.boolean('Printed'),
    }
    
    def receipt_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        voucher = self.browse(cr, uid, ids[0])
        if voucher.printed: # If printed, user must be in a special group to print it. Otherwise, error
            group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mh_print_buttons', 'group_force_print_receipt')[1]
            force_print = group_id in [x.id for x in self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id]
            if not force_print:
                raise osv.except_osv(_('Error!'), _('This voucher has been printed!'))

        self.write(cr, uid, ids, {'printed': True})
        datas = {
             'ids': ids,
             'model': 'account.voucher',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.print.voucher.mh',
            'datas': datas,
            'nodestroy' : True
        }
        
account_invoice()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
