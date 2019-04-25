# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposAccommodationType(models.Model):

    _name = 'campos.accommodation.type'
    _description = 'Campos Accommodation Type'  # TODO

    name = fields.Char()
