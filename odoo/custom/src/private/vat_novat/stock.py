from osv import fields, osv

class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'
    
    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        """ Adding Flag VAT / No-VAT from SO into INV when created from DO """
        
        res = super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id,
                                                                group, type, context=context)
        # Loop through each id (DO), getting its SO's Additional Flag, Write it to Invoice
        sale_obj = self.pool.get('sale.order') 
        pickings = self.browse(cr, uid, ids)
        for picking in pickings:
            invoice_id = res[picking.id]
            sale_ids = sale_obj.search(cr, uid, [('name','=',picking.origin or '')])
            if sale_ids:
                results = sale_obj.read(cr, uid, sale_ids, ['is_mh_vat','is_mh_novat'])
                is_mh_vat = results and results[0] and results[0]['is_mh_vat'] or False
                is_mh_novat = results and results[0] and results[0]['is_mh_novat'] or False
                self.pool.get('account.invoice').write(cr, uid, [invoice_id], 
                                            {'is_mh_vat': is_mh_vat, 'is_mh_novat': is_mh_novat}, context)
        
        return res

