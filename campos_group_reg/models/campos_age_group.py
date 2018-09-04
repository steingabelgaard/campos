# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposAgeGroup(models.Model):

    _name = 'campos.age.group'
    _description = 'Campos Age Group'  # TODO
    _order = 'age_from'

    name = fields.Char()
    age_from = fields.Integer('Age From')
    age_to = fields.Integer('Age To')
