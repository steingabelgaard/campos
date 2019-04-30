# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class HrEmployee(models.Model):

    _inherit = 'hr.employee'
    
    participate = fields.Boolean('Participate in Camp')
    
    participant_id = fields.Many2one('campos.participant', 'Paticipant record')
    
    # Related participant fields:
    
    camp_day_ids = fields.Many2many(related='participant_id.camp_day_ids')
    arrival_date_id = fields.Many2one(related='participant_id.arrival_date_id')     
    depature_date_id = fields.Many2one(related='participant_id.depature_date_id')
    
    first_meal = fields.Selection(related='participant_id.first_meal')
    last_meal = fields.Selection(related='participant_id.last_meal')
    
    camp_age = fields.Integer(related='participant_id.camp_age')
    camp_age18plus = fields.Char(related='participant_id.camp_age18plus')
    scout_org_id = fields.Many2one(related='participant_id.scout_org_id')
    accommodation_id = fields.Many2one(related='participant_id.accommodation_id')
    
    ckr_ok = fields.Boolean('CKR', track_visibility='onchange')
    
    @api.multi
    def toggle_participate(self):
        self.ensure_one()
        self.participate = not self.participate
        if self.participate:
            if not self.participant_id:
                self.participant_id = self.env['campos.participant'].create({'partner_id': self.address_home_id.id,
                                                                             'employee_id': self.id,
                                                                             'state': 'confirmed',
                                                                             'group_reg_id': False})
                self.address_home_id.participant = True
        else:
            if self.participant_id:
                self.participant_id.state = 'cancelled'
            
    
