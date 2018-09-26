# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposScoutOrg(models.Model):

    _name = 'campos.scout.org'
    _description = 'Campos Scout Org'  # TODO

    name = fields.Char('Name', size=128)
    country_id = fields.Many2one('res.country', 'Country')
    sex = fields.Char('Sex', size=128)
    worldorg = fields.Selection([('wagggs', 'WAGGGS'),
                                 ('wosm', 'WOSM'),
                                 ('w/w', 'WAGGGS/WOSM'),
                                 ('other', 'Other')], string='World Organization')
