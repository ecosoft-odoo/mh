﻿# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 CodUP (<http://codup.com>).
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

import time

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import netsvc

class mro_order(osv.osv):
    """
    Maintenance Orders
    """
    _name = 'mro.order'
    _description = 'Maintenance Order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    STATE_SELECTION = [
        ('draft', 'DRAFT'),
        ('released', 'WAITING PARTS'),
        ('ready', 'READY TO MAINTENANCE'),
        ('parts_except', 'PARTS EXCEPTION'),
        ('done', 'DONE'),
        ('cancel', 'CANCELED')
    ]
    
    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('cm', 'Corrective')
    ]
    _track = {
        'state': {
            'mro.mt_order_confirmed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'ready',
        },
    }
    _columns = {
        'name': fields.char('Reference', size=64),
        'origin': fields.char('Source Document', size=64, readonly=True, states={'draft': [('readonly', False)]},
            help="Reference of the document that generated this maintenance order."),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True,
            help="When the maintenance order is created the status is set to 'Draft'.\n\
            If the order is confirmed the status is set to 'Waiting Parts'.\n\
            If any exceptions are there, the status is set to 'Picking Exception'.\n\
            If the stock is available then the status is set to 'Ready to Maintenance'.\n\
            When the maintenance order gets started then the status is set to 'In Progress'.\n\
            When the maintenance is over, the status is set to 'Done'."),
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'task_id': fields.many2one('mro.task', 'Task', readonly=True, states={'draft': [('readonly', False)]}),
        'description': fields.char('Description', size=64, translate=True, required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'asset_id': fields.many2one('asset.asset', 'Asset', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_planned': fields.datetime('Planned Date', required=True, select=1, readonly=True, states={'draft':[('readonly',False)]}),
        'date_scheduled': fields.datetime('Scheduled Date', required=True, select=1, readonly=True, states={'draft':[('readonly',False)],'released':[('readonly',False)],'ready':[('readonly',False)]}),
        'date_execution': fields.datetime('Execution Date', required=True, select=1, readonly=True, states={'draft':[('readonly',False)],'released':[('readonly',False)],'ready':[('readonly',False)]}),
        'parts_location_id': fields.many2one('stock.location', 'Parts Location', required=True,
            readonly=True, states={'draft':[('readonly',False)]},
            help="Location where the system will look for parts."),
        'parts_lines': fields.one2many('mro.order.parts.line', 'maintenance_id', 'Planned parts',
            readonly=True, states={'draft':[('readonly',False)]}),
        'parts_picking_id': fields.many2one('stock.picking', 'Parts Picking List', readonly=True, ondelete="restrict",
            help="This is the Internal Picking List that brings parts to the asset"),
        'parts_ready_lines': fields.related('parts_picking_id', 'move_lines', type='one2many', relation="stock.move", string='Available Parts',
            readonly=True),
        'parts_move_lines': fields.many2many('stock.move', 'mro_maintenance_move_ids', 'maintenance_id', 'move_id', 'Parts to Consume',
            domain=[('state','=', ('assigned'))], readonly=True, states={'draft':[('readonly',False)]}),
        'parts_moved_lines': fields.many2many('stock.move', 'mro_maintenance_move_ids', 'maintenance_id', 'move_id', 'Consumed Parts',
            domain=[('state','=', ('done'))], readonly=True, states={'draft':[('readonly',False)]}),
        'tools_description': fields.text('Tools Description',translate=True),
        'labor_description': fields.text('Labor Description',translate=True),
        'operations_description': fields.text('Operations Description',translate=True),
        'documentation_description': fields.text('Documentation Description',translate=True),
        'problem_description': fields.text('Problem Description'),
        'company_id': fields.many2one('res.company','Company',required=True, readonly=True, states={'draft':[('readonly',False)]}),
    }
    
    _defaults = {
        'state': lambda *a: 'draft',
        'maintenance_type': lambda *a: 'bm',
        'date_planned': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_scheduled': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_execution': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'mro.order', context=c),
        'parts_location_id': lambda self, cr, uid, c: self.pool.get('ir.model.data').get_object(cr, uid, 'stock', 'stock_location_stock', context=c).id,
    }
    
    _order = 'date_execution'
    
    def onchange_planned_date(self, cr, uid, ids, date):
        """
        onchange handler of date_planned.
        """
        return {'value': {
            'date_scheduled': date,
        }}
        
    def onchange_scheduled_date(self, cr, uid, ids, date):
        """
        onchange handler of date_scheduled.
        """
        return {'value': {
            'date_execution': date,
        }}
    
    def onchange_execution_date(self, cr, uid, ids, date, state):
        """
        onchange handler of date_execution.
        """
        value = {}
        if state == 'draft':
            value['value'] = {'date_planned': date}
        else:
            value['value'] = {'date_scheduled': date}
        return value
        
    def onchange_task(self, cr, uid, ids, task_id, parts_lines):
        """
        onchange handler of task_id.
        """
        task = self.pool.get('mro.task').browse(cr, uid, task_id)
        #clear old parts
        new_parts_lines = [[2,line[1],line[2]] for line in parts_lines if line[0]]
        #copy parts from task
        for line in task.parts_lines:
            new_parts_lines.append([0,0,{
                'name': line.name,
                'parts_id': line.parts_id.id,
                'parts_qty': line.parts_qty,
                'parts_uom': line.parts_uom.id,
                }])
        return {'value': {
            'parts_lines': new_parts_lines,
            'description': task.name,
            'tools_description': task.tools_description,
            'labor_description': task.labor_description,
            'operations_description': task.operations_description,
            'documentation_description': task.documentation_description
        }}
    
    def _get_auto_picking(self, cr, uid, order):
        return True
    
    def _create_picking_parts(self, cr, uid, order, context=None):
        stock_picking = self.pool.get('stock.picking')
        pick_type = 'internal'
        partner_id = False

        picking_id = stock_picking.create(cr, uid, {
            'origin': order.name,
            'type': pick_type,
            'move_type': 'one',
            'state': 'auto',
            'partner_id': partner_id,
            'auto_picking': self._get_auto_picking(cr, uid, order),
            'company_id': order.company_id.id,
        })
        order.write({'parts_picking_id': picking_id}, context=context)
        return picking_id
        
    def _add_picking_parts_line(self, cr, uid, parts_line, picking_parts_id, parent_move_id, context=None):
        stock_move = self.pool.get('stock.move')
        order = parts_line.maintenance_id
        # Internal shipment is created for Stockable and Consumer Products
        if parts_line.parts_id.type not in ('product', 'consu'):
            return False
        return stock_move.create(cr, uid, {
                        'name': order.name,
                        'picking_id': picking_parts_id,
                        'product_id': parts_line.parts_id.id,
                        'product_qty': parts_line.parts_qty,
                        'product_uom': parts_line.parts_uom.id,
                        'date': order.date_planned,
                        'move_dest_id': parent_move_id,
                        'location_id': order.parts_location_id.id,
                        'location_dest_id': order.parts_location_id.id,
                        'state': 'waiting',
                        'company_id': order.company_id.id,
                })
                
    def _make_procurement_parts_line(self, cr, uid, parts_line, picking_parts_move_id, context=None):
        wf_service = netsvc.LocalService("workflow")
        procurement_order = self.pool.get('procurement.order')
        order = parts_line.maintenance_id
        procurement_id = procurement_order.create(cr, uid, {
                    'name': order.name,
                    'origin': order.name,
                    'date_planned': order.date_planned,
                    'product_id': parts_line.parts_id.id,
                    'product_qty': parts_line.parts_qty,
                    'product_uom': parts_line.parts_uom.id,
                    'location_id': order.parts_location_id.id,
                    'procure_method': parts_line.parts_id.procure_method,
                    'move_id': picking_parts_move_id,
                    'company_id': order.company_id.id,
                })
        wf_service.trg_validate(uid, procurement_order._name, procurement_id, 'button_confirm', cr)
        return procurement_id
        
    def _make_consume_parts_line(self, cr, uid, parts_line, context=None):
        stock_move = self.pool.get('stock.move')
        order = parts_line.maintenance_id
        # Internal shipment is created for Stockable and Consumer Products
        if parts_line.parts_id.type not in ('product', 'consu'):
            return False
        move_id = stock_move.create(cr, uid, {
            'name': order.name,
            'date': order.date_planned,
            'product_id': parts_line.parts_id.id,
            'product_qty': parts_line.parts_qty,
            'product_uom': parts_line.parts_uom.id,
            'location_id': order.parts_location_id.id,
            'location_dest_id': order.asset_id.property_stock_asset.id,
            'state': 'waiting',
            'company_id': order.company_id.id,
        })
        order.write({'parts_move_lines': [(4, move_id)]}, context=context)
        return move_id
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms maintenance order.
        @return: Newly generated Parts Picking Id.
        """
        picking_id = False
        wf_service = netsvc.LocalService("workflow")
        for order in self.browse(cr, uid, ids, context=context):
            picking_parts_id = self._create_picking_parts(cr, uid, order, context=context)
            
            #make supply chain for each parts
            for line in order.parts_lines:
                consume_parts_move_id = self._make_consume_parts_line(cr, uid, line, context=context)
                picking_parts_move_id = self._add_picking_parts_line(cr, uid, line, picking_parts_id, consume_parts_move_id, context=context)
                self._make_procurement_parts_line(cr, uid, line, picking_parts_move_id, context=context)

            wf_service.trg_validate(uid, 'stock.picking', picking_parts_id, 'button_confirm', cr)
            order.write({'state':'released'}, context=context)
        return picking_parts_id    
    
    def action_ready(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'ready'})
        return True

    def action_parts_except(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.pool.get('stock.move').action_cancel(cr, uid, [x.id for x in order.parts_move_lines])
        self.write(cr, uid, ids, {'state': 'parts_except'})
        return True

    def action_done(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            self.pool.get('stock.move').action_done(cr, uid, [x.id for x in order.parts_move_lines])
        self.write(cr, uid, ids, {'state': 'done', 'date_execution': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            if order.state == 'released' and order.parts_picking_id.state not in ('draft', 'cancel'):
                raise osv.except_osv(
                    _('Cannot cancel maintenance order!'),
                    _('You must first cancel related internal picking attached to this maintenance order.'))
            self.pool.get('stock.move').action_cancel(cr, uid, [x.id for x in order.parts_move_lines])
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True
        
    def test_if_parts(self, cr, uid, ids):
        """
        @return: True or False
        """
        res = True
        for order in self.browse(cr, uid, ids):
            if not order.parts_lines:
                res = False
        return res
        
    def force_done(self, cr, uid, ids, context=None):
        """ Assign and consume parts.
        @return: True
        """
        self.force_parts_reservation(cr, uid, ids)
        wf_service = netsvc.LocalService("workflow")
        for order in self.browse(cr, uid, ids, context=context):
            wf_service.trg_validate(uid, 'mro.order', order.id, 'button_done', cr)
        return True
        
    def force_parts_reservation(self, cr, uid, ids, context=None):
        """ Assign parts.
        @return: True
        """
        pick_obj = self.pool.get('stock.picking')
        pick_obj.force_assign(cr, uid, [order.parts_picking_id.id for order in self.browse(cr, uid, ids)])
        return True
        
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mro.order') or '/'
        return super(mro_order, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('date_execution') and not vals.get('state'):
            # constraint for calendar view
            for order in self.browse(cr, uid, ids):
                if order.state == 'draft':
                    vals['date_planned'] = vals['date_execution']
                    vals['date_scheduled'] = vals['date_execution']
                elif order.state in ('released','ready'):
                    vals['date_scheduled'] = vals['date_execution']
                else: del vals['date_execution']
        return super(mro_order, self).write(cr, uid, ids, vals, context=context)


class mro_order_parts_line(osv.osv):
    _name = 'mro.order.parts.line'
    _description = 'Maintenance Planned Parts'
    _columns = {
        'name': fields.char('Description', size=64),
        'parts_id': fields.many2one('product.product', 'Parts', required=True),
        'parts_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'parts_uom': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'maintenance_id': fields.many2one('mro.order', 'Maintenance Order', select=True),
    }
    
    _defaults = {
        'parts_qty': lambda *a: 1.0,
    }
    
    def onchange_parts(self, cr, uid, ids, parts_id):
        """
        onchange handler of parts_id.
        """
        parts = self.pool.get('product.product').browse(cr, uid, parts_id)
        return {'value': {'parts_uom': parts.uom_id.id}}
        
    def unlink(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'maintenance_id': False})
        return True
        
    def create(self, cr, uid, values, context=None):
        ids = self.search(cr, uid, [('maintenance_id','=',values['maintenance_id']),('parts_id','=',values['parts_id'])])
        if len(ids)>0:
            values['parts_qty'] = self.browse(cr, uid, ids[0]).parts_qty + values['parts_qty']
            self.write(cr, uid, ids[0], values, context=context)
            return ids[0]
        ids = self.search(cr, uid, [('maintenance_id','=',False)])
        if len(ids)>0:
            self.write(cr, uid, ids[0], values, context=context)
            return ids[0]
        return super(mro_order_parts_line, self).create(cr, uid, values, context=context)
        

class mro_task(osv.osv):
    """
    Maintenance Tasks (Template for order)
    """
    _name = 'mro.task'
    _description = 'Maintenance Task'
    
    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective')
    ]
    
    _columns = {
        'name': fields.char('Description', size=64, required=True, translate=True),
        'asset_id': fields.many2one('asset.asset', 'Asset', required=True),
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True),
        'parts_lines': fields.one2many('mro.task.parts.line', 'task_id', 'Parts'),
        'tools_description': fields.text('Tools Description',translate=True),
        'labor_description': fields.text('Labor Description',translate=True),
        'operations_description': fields.text('Operations Description',translate=True),
        'documentation_description': fields.text('Documentation Description',translate=True),
        'active': fields.boolean('Active'),
    }

    _defaults = {
        'active': True,
        'maintenance_type': 'cm',
    }
    
    
class mro_task_parts_line(osv.osv):
    _name = 'mro.task.parts.line'
    _description = 'Maintenance Planned Parts'
    _columns = {
        'name': fields.char('Description', size=64),
        'parts_id': fields.many2one('product.product', 'Parts', required=True),
        'parts_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'parts_uom': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'task_id': fields.many2one('mro.task', 'Maintenance Task', select=True),
    }
    
    _defaults = {
        'parts_qty': lambda *a: 1.0,
    }
    
    def onchange_parts(self, cr, uid, ids, parts_id):
        """
        onchange handler of parts_id.
        """
        parts = self.pool.get('product.product').browse(cr, uid, parts_id)
        return {'value': {'parts_uom': parts.uom_id.id}}
        
    def unlink(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'task_id': False})
        return True
        
    def create(self, cr, uid, values, context=None):
        ids = self.search(cr, uid, [('task_id','=',values['task_id']),('parts_id','=',values['parts_id'])])
        if len(ids)>0:
            values['parts_qty'] = self.browse(cr, uid, ids[0]).parts_qty + values['parts_qty']
            self.write(cr, uid, ids[0], values, context=context)
            return ids[0]
        ids = self.search(cr, uid, [('task_id','=',False)])
        if len(ids)>0:
            self.write(cr, uid, ids[0], values, context=context)
            return ids[0]
        return super(mro_task_parts_line, self).create(cr, uid, values, context=context)

        
class mro_request(osv.osv):
    """
    Maintenance Requests
    """
    _name = 'mro.request'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    STATE_SELECTION = [
        ('draft', 'Draft'),
        ('claim', 'Claim'),
        ('run', 'Execution'),
        ('done', 'Done'),
        ('reject', 'Rejected'),
        ('cancel', 'Canceled')
    ]
    _track = {
        'state': {
            'mro.mt_request_sent': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'claim',
            'mro.mt_request_confirmed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'run',
            'mro.mt_request_rejected': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'reject',
        },
    }
    _columns = {
        'name': fields.char('Reference', size=64),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True,
            help="When the maintenance request is created the status is set to 'Draft'.\n\
            If the request is sent the status is set to 'Claim'.\n\
            If the request is confirmed the status is set to 'Execution'.\n\
            If the request is rejected the status is set to 'Rejected'.\n\
            When the maintenance is over, the status is set to 'Done'."),
        'asset_id': fields.many2one('asset.asset', 'Asset', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'cause': fields.char('Cause', size=64, translate=True, required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'description': fields.text('Description', readonly=True, states={'draft': [('readonly', False)]}),
        'reject_reason': fields.text('Reject Reason', readonly=True),
        'requested_date': fields.datetime('Requested Date', required=True, select=1, readonly=True, states={'draft': [('readonly', False)]}, help="Date requested by the customer for maintenance."),
        'execution_date': fields.datetime('Execution Date', required=True, select=1, readonly=True, states={'draft':[('readonly',False)],'claim':[('readonly',False)]}),
        'breakdown': fields.boolean('Breakdown', readonly=True, states={'draft': [('readonly', False)]}),
        'create_uid': fields.many2one('res.users', 'Responsible'),
    }
    
    _defaults = {
        'state': 'draft',
        'requested_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'execution_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'breakdown': False,
    }
    
    def onchange_requested_date(self, cr, uid, ids, date):
        """
        onchange handler of requested_date.
        """
        return {'value': {
            'execution_date': date,
        }}
    
    def onchange_execution_date(self, cr, uid, ids, date, state, breakdown):
        """
        onchange handler of execution_date.
        """
        value = {}
        if state == 'draft' and not breakdown:
            value['value'] = {'requested_date': date}
        return value
        
    def action_send(self, cr, uid, ids, context=None):
        value = {'state': 'claim'}
        for request in self.browse(cr, uid, ids, context=context):
            if request.breakdown:
                value['requested_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            self.write(cr, uid, ids, value)
        return True
        
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms maintenance request.
        @return: Newly generated Maintenance Order Id.
        """
        order = self.pool.get('mro.order')
        order_id = False
        for request in self.browse(cr, uid, ids, context=context):
            order_id = order.create(cr, uid, {
                'date_planned':request.requested_date,
                'date_scheduled':request.requested_date,
                'date_execution':request.requested_date,
                'origin': request.name,
                'state': 'draft',
                'maintenance_type': 'bm',
                'asset_id': request.asset_id.id,
                'description': request.cause,
                'problem_description': request.description,
            })
        self.write(cr, uid, ids, {'state': 'run'})
        return order_id
        
    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
        
    def action_reject(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'reject', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
        
    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel', 'execution_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mro.request') or '/'
        return super(mro_request, self).create(cr, uid, vals, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: