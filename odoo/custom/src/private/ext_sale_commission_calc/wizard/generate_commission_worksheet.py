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

from openerp.osv import osv
from openerp.tools.translate import _


class generate_commission_worksheet(osv.osv_memory):

    _inherit = "generate.commission.worksheet"

    def _create_worksheets(self, cr, uid, sales_worksheets, team_worksheets, context=None):
        new_sales_worksheets = []
        new_team_worksheets = []
        for sale_worksheet in sales_worksheets:
            new_sales_worksheets.append({'salesperson_id': sale_worksheet['salesperson_id'],
                                           'period_id': sale_worksheet['period_id'],
                                           'is_mh_novat': True})
            new_sales_worksheets.append({'salesperson_id': sale_worksheet['salesperson_id'],
                                           'period_id': sale_worksheet['period_id'],
                                           'is_mh_novat': False})
        for team_worksheet in team_worksheets:
            new_team_worksheets.append({'sale_team_id': team_worksheet['sale_team_id'],
                                           'period_id': team_worksheet['period_id'],
                                           'is_mh_novat': True})
            new_team_worksheets.append({'sale_team_id': team_worksheet['sale_team_id'],
                                           'period_id': team_worksheet['period_id'],
                                           'is_mh_novat': False})
        return super(generate_commission_worksheet, self)._create_worksheets(cr, uid, new_sales_worksheets, new_team_worksheets, context=context)

generate_commission_worksheet()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
