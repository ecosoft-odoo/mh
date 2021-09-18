from osv import fields, osv

class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'
    
    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        """ Adding PO Reference and PO Date from SO into INV when created from DO """
        
        res = super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id,
                                                                group, type, context=context)
        # Loop through each id (DO), getting its SO's Additional Flag, Write it to Invoice
        sale_obj = self.pool.get('sale.order') 
        pickings = self.browse(cr, uid, ids)
        for picking in pickings:
            invoice_id = res[picking.id]
            sale_ids = sale_obj.search(cr, uid, [('name','=',picking.origin or '')])
            if sale_ids:
                results = sale_obj.read(cr, uid, sale_ids, ['po_reference','po_date'])
                po_reference = results and results[0] and results[0]['po_reference'] or False
                po_date = results and results[0] and results[0]['po_date'] or False
                self.pool.get('account.invoice').write(cr, uid, [invoice_id], 
                                            {'po_reference': po_reference, 'po_date': po_date}, context)
        
        return res

