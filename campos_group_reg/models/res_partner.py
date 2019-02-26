# -*- coding: utf-8 -*-
# Copyright 2018 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from psycopg2 import IntegrityError

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):

    _inherit = 'res.partner'
    
    scoutgroup = fields.Boolean('Scout Troop')
    participant = fields.Boolean('Participant')
    is_dk = fields.Boolean('Is DK', compute='_compute_dk', store=True)
    is_non_dk = fields.Boolean('Is Non DK', compute='_compute_dk', store=True)

    @api.multi
    @api.depends('country_id')
    def _compute_dk(self):
        dk_id = self.env.ref('base.dk')
        for partner in self:
            if partner.country_id == dk_id:
                partner.update({'is_dk': True,
                                'is_non_dk': False})
            else:
                partner.update({'is_dk': False,
                                'is_non_dk': True})


    def ensure_portal_user(self):
        '''
        Extracted from ensure_member_number() to use in server action/Lab work
        '''
        if self.env['res.users'].sudo().search_count([('partner_id', '=', self.id)]) == 0:
            try:
                company_id = self.env.ref('base.main_company').id
                data = {} # self.env['ir.default'].get_defaults_dict('res.users')
                data.update({
                        'login': self.email,
                        'partner_id': self.id,
                        'company_id' : company_id,
                        'company_ids' : [(4, company_id,)],
                        'groups_id': [(4, self.env.ref('base.group_portal').id)],
                        })
                user = self.env['res.users'].sudo().with_context(no_reset_password=True).create(data)

            except IntegrityError:
                # Ignore error if user exists
                if self.env['res.users'].sudo().search_count([('partner_id', '=', self.id)]) > 0:
                    pass
                else:
                    raise
                
    def signup_and_mail(self, template_ref):
        _logger.info('SIGNUP AND MAIL: %s %s', self, template_ref)
        template = self.env.ref(template_ref)
        self.ensure_portal_user()
        lang = self.lang
        portal_url = self.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[self.id]
        self.signup_prepare()
        _logger.info('PORTAL %s', portal_url)
        if template:
            template.with_context(dbname=self._cr.dbname, portal_url=portal_url, lang=lang).send_mail(self.id, force_send=True)
        else:
            _logger.warning("No email template found for sending email to the portal user")


        
