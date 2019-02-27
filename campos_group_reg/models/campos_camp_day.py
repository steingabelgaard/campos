# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposCampDay(models.Model):

    _name = 'campos.camp.day'
    _description = 'Campos Camp Day'
    _rec_name = 'campday'
    _order = 'campday'

    campday = fields.Date('Camp Day')
    name = fields.Date(related='campday')  # For CMS Form support
    arrival_day = fields.Boolean('Arrival day')
    depature_day = fields.Boolean('Depature day')
    valid_dk = fields.Boolean('Arrival/Departure valid for DK Groups')
    valid_non_dk = fields.Boolean(
        'Arrival/Departure valid for foreign  Groups'
    )
