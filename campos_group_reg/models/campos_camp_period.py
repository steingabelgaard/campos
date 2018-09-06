# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CamposCampPeriod(models.Model):

    _name = 'campos.camp.period'
    _description = 'Campos Camp Period'  # TODO
    _order = 'date_from'

    name = fields.Char()
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
