# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposSsGroupReg(models.Model):

    _name = 'campos.ss.group.reg'
    _description = 'Campos Ss Group Reg'  # TODO

    name = fields.Char()
    snapshot_id = fields.Many2one('campos.snapshot', 'Snapshot')
    registration_id = fields.Many2one('campos.group.reg', 'Registration')
    sspar_ids = fields.One2many('campos.ss.participant', 'ssreg_id', 'Participants')
    
    state = fields.Selection(
        [
            ('draft', 'Unconfirmed'),
            ('reg', 'Registred'),
            ('prereg', 'Pre Registered'),
            ('finalreg', 'Final Registration'),
            ('done', 'Attended'),
            ('cancel', 'Cancelled'),
        ],
        string='State',
        default='draft',
        track_visibility='onchange',
    )
