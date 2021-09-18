# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class invoice_info(osv.osv):

    _inherit = "invoice.info"

    def _prepare_invoice_info_line(self, line):
        res = super(invoice_info, self)._prepare_invoice_info_line(line)
        res["promo_code"] = line and line.promo_code and line.promo_code.id or False
        return res

    def update_promo_code(self, cr, uid, ids, context={}):
        invoice_line_obj = self.pool.get('account.invoice.line')
        for rec in self.pool.get('invoice.info').browse(cr, uid, ids):
            for line in rec.invoice_info_line:
                promo_code = line.promo_code and line.promo_code.id or False
                invoice_line_id = line.invoice_line_id and line.invoice_line_id.id or False
                invoice_line_obj.write(cr, uid, [invoice_line_id], {'promo_code': promo_code})
        return


invoice_info()


class invoice_info_line(osv.osv):

    _inherit = "invoice.info.line"
    _columns = {
        "promo_code": fields.many2one(
            "promo.code", "Promo Code", domain="[('product_id', '=', product_id)]"
        ),
    }


invoice_info_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
