# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CamposPreregAgePeriod(models.Model):

    _name = 'campos.prereg.age.period'
    _description = 'Campos Prereg Age Period'  # TODO

    name = fields.Char()
    group_reg_id = fields.Many2one('campos.group.reg', 'Group registration')
    period_id = fields.Many2one('campos.camp.period', 'Camp Period')
    age_group_id = fields.Many2one('campos.age.group', 'Age Group')
    value = fields.Integer('Value')
