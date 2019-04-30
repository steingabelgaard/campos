# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposSsParticipant(models.Model):

    _name = 'campos.ss.participant'
    _description = 'Campos Ss Participant'  # TODO

    name = fields.Char()

    ssreg_id = fields.Many2one('campos.ss.group.reg', 'Snapshot Reg')
    participant_id = fields.Many2one('campos.participant', 'Participant')
    
    nights = fields.Integer('Nights')
    camp_day_count = fields.Integer('Days')
    camp_product_id = fields.Many2one('product.product', 'Camp Fee Product')
    extra_camp_days = fields.Integer('Extra Camp dayes')
    extra_camp_days_product_id = fields.Many2one('product.product', 'Camp Fee Product Extra Days')
    extra_pre_camp_days = fields.Integer('Extra Pre Camp dayes')
    extra_pre_camp_days_product_id = fields.Many2one('product.product', 'Camp Fee Product Extra Pre Camp Days')
    extra_post_camp_days = fields.Integer('Extra Post Camp dayes')
    extra_post_camp_days_product_id = fields.Many2one('product.product', 'Camp Fee Product Extra Post Camp Days')
    
    arrival_date_id = fields.Many2one(
        'campos.camp.day',
        'Arrival date',
        domain=[('arrival_day', '=', True)],
        track_visibility='onchange',
    )
    depature_date_id = fields.Many2one(
        'campos.camp.day',
        'Depature date',
        domain=[('depature_day', '=', True)],
        track_visibility='onchange',
    )
    
    employee_id = fields.Many2one('hr.employee', 'Staff')
    camp_age = fields.Integer('Age (on Camp)')
    
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        string='State',
        track_visibility='onchange',
    )
    
    
    
    