# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)


class CamposGroupReg(models.Model):

    _name = 'campos.group.reg'
    _description = 'Campos Group Reg'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _inherits = {'res.partner': 'partner_id',
                 }

    def _default_prereg_ids(self):
        # your list of project should come from the context, some selection
        # in a previous wizard or wherever else
        periods = self.env['campos.camp.period'].search([])

        age_groups = self.env['campos.age.group'].search([])
        return [
            (0, 0, {
                'period_id': p.id,
                'age_group_id': a.id,
                'value': 0,
            })
            for p in periods
            for a in age_groups
        ]

    partner_id = fields.Many2one('res.partner', 'Group', required=True,  ondelete="restrict")

    name = fields.Char(related='partner_id.name', required=True)
    street = fields.Char(related='partner_id.street')
    street2 = fields.Char(related='partner_id.street2')
    zip = fields.Char(related='partner_id.zip')
    city = fields.Char(related='partner_id.city')
    country_id = fields.Many2one(related='partner_id.country_id')
    municipality_id = fields.Many2one(related='partner_id.municipality_id')

    state = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('reg', 'Registred'),
        ('prereg', 'Pre Registered'),
        ('finalreg', 'Final Registration'),
        ('done', 'Attended'),
        ('cancel', 'Cancelled'),
        ], string='State', default='draft', track_visibility='onchange')

    # Contact

    contact_partner_id = fields.Many2one('res.partner', 'Contact')

    contact_name = fields.Char(related='contact_partner_id.name')
    contact_street = fields.Char(related='contact_partner_id.street')
    contact_street2 = fields.Char(related='contact_partner_id.street2')
    contact_zip = fields.Char(related='contact_partner_id.zip')
    contact_city = fields.Char(related='contact_partner_id.city')
    contact_country_id = fields.Many2one(related='partner_id.country_id')
    contact_email = fields.Char(related='contact_partner_id.email')
    contact_mobile = fields.Char(related='contact_partner_id.mobile')

    treasurer_partner_id = fields.Many2one('res.partner', 'Treasurer')

    treasurer_name = fields.Char(related='treasurer_partner_id.name')
    treasurer_street = fields.Char(related='treasurer_partner_id.street')
    treasurer_street2 = fields.Char(related='treasurer_partner_id.street2')
    treasurer_zip = fields.Char(related='treasurer_partner_id.zip')
    treasurer_city = fields.Char(related='treasurer_partner_id.city')
    treasurer_country_id = fields.Many2one(related='partner_id.country_id')
    treasurer_email = fields.Char(related='treasurer_partner_id.email')
    treasurer_mobile = fields.Char(related='treasurer_partner_id.mobile')

    prereg_ids = fields.One2many('campos.prereg.age.period',
                                 'group_reg_id',
                                 'Pre registrtations',
                                 default=_default_prereg_ids)
    scout_org_id = fields.Many2one('campos.scout.org', 'Scout organization')
    
    # Final registration
    cars = fields.Integer('# of cars', track_visibility='onchange')
    busses = fields.Integer('# of busses', track_visibility='onchange')
    large_tents = fields.Integer('# of large tents (>50 sqm)')
    large_constructions = fields.Text('Large construction')
    
    ckr_ok = fields.Boolean('CKR confirmed', track_visibility='onchange')
    
    participant_ids = fields.One2many('campos.participant', 'group_reg_id', 'Participants')
    participants_confirmed = fields.Integer('Participants', help="Confirmed participants", compute='_compute_participants')
    
    @api.model
    def create(self, vals):
        if 'name' in vals and not 'partner_id' in vals:
            group_partner = self.env['res.partner'].create(
                {'name': vals['name'],
                 'street': vals['street'],
                 'street2': vals['street2'],
                 'zip': vals['zip'],
                 'city': vals['city'],
                 'country_id': vals['country_id'],
                 'is_company': True})
            vals['partner_id'] = group_partner.id

        if 'contact_name' in vals and vals['contact_name']:
            _logger.info("Creating Contact")
            contact_partner = self.env['res.partner'].create(
                {'name': vals['contact_name'],
                 'street': vals['contact_street'],
                 'street2': vals['contact_street2'],
                 'zip': vals['contact_zip'],
                 'city': vals['contact_city'],
                 'country_id': vals['contact_country_id'],
                 'email': vals['contact_email'],
                 'mobile': vals['contact_mobile'],
                 'type': 'contact',
                 'parent_id': group_partner.id})
            vals['contact_partner_id'] = contact_partner.id
        if 'treasurer_name' in vals and vals['treasurer_name']:
            _logger.info("Creating Trasurer")
            treasurer_partner = self.env['res.partner'].create(
                {'name': vals['treasurer_name'],
                 'street': vals['treasurer_street'],
                 'street2': vals['treasurer_street2'],
                 'zip': vals['treasurer_zip'],
                 'city': vals['treasurer_city'],
                 'country_id': vals['treasurer_country_id'],
                 'email': vals['treasurer_email'],
                 'mobile': vals['treasurer_mobile'],
                 'type': 'invoice',
                 'parent_id': group_partner.id})
            vals['treasurer_partner_id'] = treasurer_partner.id
        _logger.info('BEFORE CReate')
        res = super(CamposGroupReg, self).create(vals)
        res._state_action(res.state)
        return res
    
    @api.multi
    def write(self, vals):
        ret = super(CamposGroupReg, self).write(vals)
        if 'state' in vals:
            self._state_action(vals['state'])
        return ret
    
    @api.multi    
    def _state_action(self, new_state):
        _logger.info('STATE ACTION: %s', new_state)
        method = getattr(self, '_state_action_%s' % new_state, False)
        if method:
            method()
            
    @api.multi
    def _state_action_cancel(self):        
        partners = self.mapped('partner_id') + self.mapped('contact_partner_id') + self.mapped('treasurer_partner_id')
        _logger.info('PARTNERS %s:', partners )
        if partners:
            users = self.env['res.users'].search([('partner_id', 'in', partners.ids)])
            for user in users:
                user.login += '-' + str(user.id) # Make disabled ogin uniq
                user.active = False
            partners.write({'active': False})
            
    @api.multi
    def _state_action_draft(self):
        _logger.info('STATE ACTION DRAFT %s', self)
        for grp in self:
            if grp.contact_partner_id and not grp.contact_partner_id.user_ids:
                grp.contact_partner_id.signup_and_mail('campos_group_reg.contact_welcome_mail') 
            # Administration notifications:
            template = self.env.ref('campos_group_reg.new_group_pre_reg_mail')
            _logger.info("ADMMAIL %s %d", template, grp.id)
            if template:
                template.send_mail(grp.id)
        
         
    def action_registrered(self):
        self.ensure_one()
        # TODO Send mails
        self.state = 'reg'
        
    def action_pre_reg(self):
        self.ensure_one()
        self.signup_contacts()
        self.state = 'prereg'
    
        
    @api.multi
    def signup_contacts(self):
        for grp in self:
            if not grp.contact_partner_id.user_ids:
                grp.contact_partner_id.signup_and_mail('campos_group_reg.contact_welcome_mail') 
            if not grp.treasurer_partner_id.user_ids:
                grp.treasurer_partner_id.signup_and_mail('campos_group_reg.treasurer_welcome_mail') 
                
    @api.multi
    @api.depends('participant_ids.state')
    def _compute_participants(self):
        """ Determine reserved, available, reserved but unconfirmed and used seats. """
        # initialize fields to 0
        for group_reg in self:
            group_reg.participants_confirmed =  0
        # aggregate registrations by group_reg and by state
        if self.ids:
            state_field = {
                #'draft': 'participants_unconfirmed',
                'confirmed': 'participants_confirmed',
                #'done': 'seats_used',
            }
            query = """ SELECT group_reg_id, state, count(group_reg_id)
                        FROM campos_participant
                        WHERE group_reg_id IN %s AND state IN ('confirmed')
                        GROUP BY group_reg_id, state
                    """
            self._cr.execute(query, (tuple(self.ids),))
            for group_reg_id, state, num in self._cr.fetchall():
                group_reg = self.browse(group_reg_id)
                group_reg[state_field[state]] += num
