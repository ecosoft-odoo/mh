# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2009 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
	"name" : "Invoice List Report",
	"version" : "1.0",
	"author" : "Ecosoft",
	"website" : "www.zikzakmedia.com",
    "license" : "GPL-3",
	"depends" : ["account","vat_novat","ext_account","picking_invoice_relation"],
	"category" : "Accounting",
	"description": """
""",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [
        "wizard/wizard_invoice_list_report_view.xml",
		"account_report_wizard.xml",
	],
	"active": False,
	"installable": True
}
