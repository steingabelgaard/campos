# -*- coding: utf-8 -*-
# Copyright 2017 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, SUPERUSER_ID, _


from openerp.addons.connector.queue.job import job, related_action
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.exception import FailedJobError

import logging
_logger = logging.getLogger(__name__)

def related_action_generic(session, job):
            model = job.args[0]
            res_id = job.args[1]
            model_obj = session.env['ir.model'].search([('model', '=', model)])
            action = {
                'name': model_obj.name,
                'type': 'ir.actions.act_window',
                'res_model': model,
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': res_id,
            }
            return action

@job(default_channel='root.inv')
@related_action(action=related_action_generic)
def do_delayed_snapshot(session, model, ssreg_id):
    _logger.info("DO SSREG: %d", ssreg_id)
    ssreg = session.env['campos.fee.ss.registration'].browse(ssreg_id)
    if ssreg.exists():
        ssreg.do_delayed_snapshot()


class EventRegistration(models.Model):

    _inherit = 'event.registration'

    number_participants = fields.Integer('Number of participants', compute='_compute_fees')
    number_participants_stored = fields.Integer('# of participants', compute='_compute_fees', store=True)
    number_accomondations = fields.Integer('# accomdation', compute='_compute_fees', store=True)
    fee_participants = fields.Float('Participants Fees', compute='_compute_fees')
    fee_transport = fields.Float('Transport Fee/Refusion', compute='_compute_fees')
    material_cost = fields.Float('Material orders', compute='_compute_fees')
    fee_total = fields.Float('Total Fee', compute='_compute_fees')
    ssreg_ids = fields.One2many('campos.fee.ss.registration', 'registration_id', 'Snapshot')

    @api.multi
    @api.depends('participant_ids', 'participant_ids.state', 'jobber_accommondation_ids')
    def _compute_fees(self):
        for reg in self.sudo():
            fee_participants = 0.0
            fee_transport = 0.0
            number_participants = 0
            number_accomondations = 0
            for par in reg.participant_ids.filtered(lambda r: r.state not in ['cancel', 'deregistered']):
                fee_participants += par.camp_price
                fee_transport += par.transport_price_total
                number_participants += 1
                if not par.staff:
                    number_accomondations += 1
            number_accomondations += len(reg.jobber_accomodation_ids)
            reg.fee_participants = fee_participants
            reg.fee_transport = fee_transport
            reg.number_participants = number_participants
            reg.number_participants_stored = number_participants
            reg.number_accomondations = number_accomondations
            so_cost = 0.0
            if self.env.uid == SUPERUSER_ID:
                for so in self.env['sale.order.line'].search([('order_partner_id', '=', reg.partner_id.id),('order_id.state', '!=', 'cancel')]):
                    so_cost += so.price_subtotal
            else:
                for so in self.env['sale.order.line'].suspend_security().search([('order_partner_id', '=', reg.partner_id.id),('order_id.state', '!=', 'cancel')]):
                    so_cost += so.price_subtotal
            reg.material_cost = so_cost
            reg.fee_total = fee_participants + fee_transport + so_cost
            
    @api.multi
    def do_snapshot(self, snapshot):
        _logger.info('SS: %s %d', snapshot, snapshot.id)
        for reg in self:
            ssreg = self.env['campos.fee.ss.registration'].create({'snapshot_id': snapshot.id,
                                                                   'registration_id': reg.id})
            
            session = ConnectorSession.from_env(self.env)
            do_delayed_snapshot.delay(session, 'campos.fee.ss.registration', ssreg.id)
            
#             for par in reg.participant_ids:
#                 par.do_snapshot(ssreg)
#             
#             ssreg.write({'number_participants': reg.number_participants,
#                          'fee_participants': reg.fee_participants,
#                          'fee_transport': reg.fee_transport,
#                          'material_cost': reg.material_cost,
#                          'fee_total': reg.fee_total,
#                          'state': reg.state,
#                          'name': reg.name})
#             if snapshot.execute_func:
#                 func = getattr(ssreg, snapshot.execute_func)
#                 func()

    @api.multi
    def assign_group_number(self):
        for reg in self:
            if not reg.partner_id.ref:
                reg.partner_id.ref = self.env['ir.sequence'].next_by_code('group.number')
