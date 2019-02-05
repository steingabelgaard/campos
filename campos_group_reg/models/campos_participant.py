# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class CamposParticipant(models.Model):

    _name = 'campos.participant'
    _description = 'CampOS Participant'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    __inherits = {'res.partner': 'partner_id'}
    _order = 'name'
    _mail_post_access = 'read'

    def _get_group_reg_id(self):
        if self.env.user.partner_id.parent_id.scoutgroup:
            group_reg = self.env['campos.group.reg'].sudo().search([('partner_id', '=', self.env.user.partner_id.parent_id.id)])
            return group_reg.id
        return False
    
    partner_id = fields.Many2one('res.partner', 'Member', delegate=True, required=True, ondelete='restrict', index=True, auto_join=True)
    group_reg_id = fields.Many2one('campos.group.reg', string='Group', default=_get_group_reg_id)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('cancelled', 'Cancelled'),
                              ], default='draft', string='State', track_visibility='onchange')
    
    camp_day_ids = fields.Many2many('campos.camp.day', string='Camp Days')
    
    arrival_date_id = fields.Many2one('campos.camp.day', 'Arrival date', domain=[('arrival_day', '=', True)], track_visibility='onchange')
    depature_date_id = fields.Many2one('campos.camp.day', 'Depature date', domain=[('depature_day', '=', True)], track_visibility='onchange')
    
    
    def _update_camp_days(self):
        days = self.env['campos.camp.day'].search([('campday', '>=', self.arrival_date_id.campday), ('campday', '<=', self.depature_date_id.campday)])
        if days:
            self.suspend_security().camp_day_ids = days
                                                    
    @api.model
    def create(self, vals):
        if 'group_reg_id' not in vals:
            vals['group_reg_id'] = self._get_group_reg_id()
        vals['parent_id'] = self.env['campos.group.reg'].browse(vals['group_reg_id']).partner_id.id
        vals['participant'] = True
        vals['type'] = 'other'
        _logger.info('CREATE: %s', vals)    
        res = super(CamposParticipant, self.sudo()).create(vals)
        if 'arrival_date_id' in vals and 'depature_day_id' in vals:
            self._update_camp_days()
        return res
    
    @api.multi
    def write(self, vals):
        res = super(CamposParticipant, self).write(vals)
        if 'arrival_date_id' in vals or 'depature_day_id' in vals:
            for par in self:
                par._update_camp_days()
        return res