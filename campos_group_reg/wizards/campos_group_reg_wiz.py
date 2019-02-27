# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class CamposGroupRegWiz(models.TransientModel):

    _name = 'campos.group.reg.wiz'

    name = fields.Char(required=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one('res.country')
    municipality_id = fields.Many2one('partner.municipality')

    contact_name = fields.Char()
    contact_street = fields.Char()
    contact_street2 = fields.Char()
    contact_zip = fields.Char()
    contact_city = fields.Char()
    contact_country_id = fields.Many2one('res.country')
    contact_email = fields.Char()
    contact_mobile = fields.Char()

    treasurer_name = fields.Char()
    treasurer_street = fields.Char()
    treasurer_street2 = fields.Char()
    treasurer_zip = fields.Char()
    treasurer_city = fields.Char()
    treasurer_country_id = fields.Many2one('res.country')
    treasurer_email = fields.Char()
    treasurer_mobile = fields.Char()

    def form_after_create_or_update(self, values, extra_values):
        _logger.info('IN FORM AFTER', values)
        self.env['campos.group.reg'].sudo().create(values)

    @api.multi
    def doit(self):
        for wizard in self:
            # TODO
            pass
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Action Name',  # TODO
            'res_model': 'result.model',  # TODO
            'domain': [('id', '=', result_ids)],  # TODO
            'view_mode': 'form,tree',
        }
        return action
