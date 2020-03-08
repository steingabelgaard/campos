# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)


class CamposParticipant(models.Model):

    _name = 'campos.participant'
    _description = 'Participant'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    __inherits = {'res.partner': 'partner_id'}
    _order = 'name'
    _mail_post_access = 'read'

    def _get_group_reg_id(self):
        if self.env.user.partner_id.parent_id.scoutgroup:
            group_reg = (
                self.env['campos.group.reg']
                .sudo()
                .search(
                    [
                        (
                            'partner_id',
                            '=',
                            self.env.user.partner_id.parent_id.id,
                        )
                    ]
                )
            )
            return group_reg.id
        return False

    partner_id = fields.Many2one(
        'res.partner',
        'Member',
        delegate=True,
        required=True,
        ondelete='restrict',
        index=True,
        auto_join=True,
    )
    group_reg_id = fields.Many2one(
        'campos.group.reg', string='Group', default=_get_group_reg_id
    )
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

    camp_day_ids = fields.Many2many('campos.camp.day', string='Camp Days')

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
    
    first_meal = fields.Selection([('breakfast', 'Breakfast'),
                                   ('lunch', 'Lunch'),
                                   ('dinner', 'Dinner')], string='First meal on arrival date')
    last_meal = fields.Selection([('breakfast', 'Breakfast'),
                                  ('lunch', 'Lunch'),
                                  ('dinner', 'Dinner')], string='Last meal on departure date')

    age_group_id = fields.Many2one('campos.age.group', 'Age Group')

    camp_age = fields.Integer('Age (on camp)', compute='_compute_camp_age', store=True)
    camp_age18plus = fields.Char('18+ (on camp)', compute='_compute_camp_age', store=True)
    
    camp_days = fields.Char('Camp Days text', compute='_compute_camp_days')
    camp_day_co = fields.Integer('# Camp Days')
    
    scout_org_id = fields.Many2one('campos.scout.org', 'Scout organization')
    accommodation_id = fields.Many2one('campos.accommodation.type', 'Accomodation')
    
    sspar_ids = fields.One2many('campos.ss.participant', 'participant_id', 'Snapshot')

    @api.multi
    def action_sync(self):
        self._update_camp_days()
        
    def _update_camp_days(self):
        days = self.env['campos.camp.day'].sudo().search(
            [
                ('campday', '>=', self.arrival_date_id.campday),
                ('campday', '<=', self.depature_date_id.campday),
            ]
        )
        if days:
            self.suspend_security().camp_day_ids = days
            self.suspend_security().camp_day_co = len(days)
            
    @api.multi
    @api.depends('birthdate_date')
    def _compute_camp_age(self):
        for part in self:
            camp_age18plus = ''
            camp_age = relativedelta(fields.Date.from_string(part.arrival_date_id.campday), fields.Date.from_string(part.birthdate_date)).years if part.birthdate_date and part.arrival_date_id else False
            if camp_age > 18:
                camp_age18plus = '18+'
            part.update({'camp_age': camp_age,
                         'camp_age18plus': camp_age18plus})

    @api.multi
    @api.depends('arrival_date_id', 'depature_date_id' )
    def _compute_camp_days(self):
        for part in self:
            camp_days = []
            for day in part.camp_day_ids:
                camp_days.append(day.campday[-2:])
            part.camp_days = ','.join(camp_days)
            
    
    @api.model
    def create(self, vals):
        if 'group_reg_id' not in vals:
            vals['group_reg_id'] = self._get_group_reg_id()
        vals['parent_id'] = (
            self.env['campos.group.reg']
            .browse(vals['group_reg_id'])
            .partner_id.id
        )
        vals['participant'] = True
        vals['type'] = 'other'
        _logger.info('CREATE: %s', vals)
        res = super(CamposParticipant, self.sudo()).create(vals)
        if 'arrival_date_id' in vals and 'depature_date_id' in vals:
            res._update_camp_days()
        return res

    @api.multi
    def write(self, vals):
        res = super(CamposParticipant, self).write(vals)
        if 'arrival_date_id' in vals or 'depature_date_id' in vals:
            for par in self:
                par._update_camp_days()
        return res

    @api.multi
    def do_snapshot(self, ssreg):
        for par in self:
            days = fields.Date.from_string(par.arrival_date_id.campday) - fields.Date.from_string(par.arrival_date_id.campday)
            sspar = self.env['campos.ss.participant'].create({'ssreg_id': ssreg.id,
                                                              'participant_id': par.id,
                                                              'name': par.name,
                                                              'arrival_date_id': par.arrival_date_id.id,
                                                              'depature_date_id': par.depature_date_id.id,
                                                              'employee_id': par.employee_id.id if par.employee_id else False,
                                                              'camp_age': par.camp_age,
                                                              'state': par.state,
                                                              'camp_day_count': days.days + 2,
                                                              'nights': days.days + 1,
                                                              }
            )
                                                              
               