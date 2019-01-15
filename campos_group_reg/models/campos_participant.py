# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposParticipant(models.Model):

    _name = 'campos.participant'
    _description = 'CampOS Participant'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    __inherits = {'res.partner': 'partner_id'}
    _order = 'name'
    _mail_post_access = 'read'

    partner_id = fields.Many2one('res.partner', 'Member', delegate=True, required=True, ondelete='restrict', index=True, auto_join=True)
    group_reg_id = fields.Many2one('campos.group.reg', string='Group')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('cancelled', 'Cancelled'),
                              ], default='draft', string='State', track_visibility='onchange')
    
    camp_day_ids = fields.Many2many('campos.camp.day', string='Camp Days')