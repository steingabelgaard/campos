# -*- coding: utf-8 -*-
# Copyright 2017 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class CamposEventParticipant(models.Model):

    _inherit = 'campos.event.participant'

    checkin_info_html = fields.Html('Check In Notes', compute='compute_checkin')
    checkin_ok = fields.Boolean('Check In possible', compute='compute_checkin')
    arrive_time = fields.Datetime('Arrival')
    checkin_completed = fields.Datetime('Check In Time')
    checkin_subcamp_id = fields.Many2one('campos.subcamp', 'Sub Camp', compute='_compute_checkin_subcamp_id')

    @api.multi
    #@api.depends()
    def compute_checkin(self):
        for par in self:
            ckr_clc = False
            checkin_ok = True
            infotext = []
            if par.clc_state:
                if par.clc_state != 'passed' and par.camp_age >= 18:
                    infotext.append(_('CLC not passed!'))
                    checkin_ok = False
            elif par.ckr_state != 'approved' and par.camp_age >= 15:
                infotext.append(_('CKR not yet approved!'))
                checkin_ok = False
            #Economy
            if par.registration_id.partner_id != par.partner_id:
                infotext.append(_('Paid by: %s') % (par.registration_id.partner_id.name))
            elif par.registration_id.partner_id.credit > 0:
                infotext.append(_('Unpaid invoices. Total due: DKK %.2f') % (par.registration_id.partner_id.credit))
                checkin_ok = False
            else:
                infotext.append(_('Payment recived'))
            if len(par.jobber_pay_for_ids) > 1:
                infotext.append(_('Paying for: %s' % ', '.join(par.jobber_pay_for_ids.mapped('name'))))

            if len(par.jobber_child_ids) > 1:
                infotext.append(_('Children: %s' % ', '.join(par.jobber_child_ids.mapped('name'))))

            if not par.accomodation_ids:
                infotext.append(_('No accomonodation specified'))
                checkin_ok = False
            else:
                infotext.append(_('Check accomodation'))
                
            if not par.canteen_ids:
                infotext.append(_('No Catering specified'))
                checkin_ok = False
            else:
                infotext.append(_('Check catering'))
                    
            #Infolines:
            if par.wristband_date:
                infotext.append(_(u'Skejser armbånd er udsendt/uddelt'))
                
            if checkin_ok:
                par.checkin_info_html = '<div class="campos_info_box">%s</div>' % '<br />'.join(infotext) if infotext else False
            else:
                par.checkin_info_html = '<div class="campos_warning_box">%s</div>' % '<br />'.join(infotext) if infotext else False
            par.checkin_ok = checkin_ok
    
    @api.multi
    #@api.depends()
    def _compute_checkin_subcamp_id(self):
        pass
            
    @api.multi
    def action_checkin(self):
        self.ensure_one()
        self.state = 'arrived'
        self.arrive_time = fields.Datetime.now()

        if not self.checkin_ok and not self.env.user.has_group('campos_checkin.group_campos_checkin_mgr'):
            return self.env['warning_box'].info(title=_('Checkin'), message=_(u'Checkin for %s is not possible here\nGo to Løkkegård for Checkin.\n\nPlease show the location on the map for the ITS') %  (self.name))

        action = {
            'name': _("Checkin for %s") % (self.name),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'campos.checkin.wiz',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': {
                'default_participant_id': self.id,
                },
        }
        _logger.info('ACTION: %s', action)
        return action

    @api.multi
    def action_cancel_checkin(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window.message',
            'title': _('Cancel Checkin'),
            'message': _("Change to 'Arrived' or 'Not yet arrived'"),
            'buttons': [
                {
                    'type': 'method',
                    'name': _('Arrived'),
                    'model': self._name,
                    'method': 'action_execute_cancel_checkin',
                    # list of arguments to pass positionally
                    'args': [self.ids],
                    # dictionary of keyword arguments
                    'kwargs': {'force_state': 'arrived'},
                },
                {
                    'type': 'method',
                    'name': _('Not yet arrived'),
                    'model': self._name,
                    'method': 'action_execute_cancel_checkin',
                    # list of arguments to pass positionally
                    'args': [self.ids],
                    # dictionary of keyword arguments
                    'kwargs': {'force_state': 'approved'},
                }
            ]
        }
        
    @api.multi
    def action_execute_cancel_checkin(self, force_state=None):
        self.ensure_one()
        if force_state:
            self.state = force_state
            if force_state == 'approved':
                self.arrive_time = False