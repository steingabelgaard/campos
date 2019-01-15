# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposCampDay(models.Model):

    _name = 'campos.camp.day'
    _description = 'Campos Camp Day'
    _rec_name = 'campday'
    _order = 'campday'

    campday = fields.Date('Camp Day')
    
    
