# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.fields import One2many
from openerp.osv.fields import reference
class Preregistration(models.Model):
    '''
    Pre-registration for a scout group to an event
    '''
    _inherit = 'event.registration'
    group_name = fields.Char('Group Name')
    group_association = fields.Many2one('campos.scout.org','Scout Organization')
    group_world_association = fields.Selection(related='group_association.worldorg', string='World Organisation', readonly=True)
    group_entrypoint = fields.Char('Point of entry into Denmark')
    group_municipality = fields.Many2one('campos.municipality','Municipallity for DK groups / Place of arrival for non DK groups')
    group_country = fields.Many2one('res.country', 'Country')
    association_groupid = fields.Char('Groups id (number) at local association')
    participant_ids = fields.One2many('event.registration.participants','registration_id','Participants')
    pionering_poles_3m_total = fields.Integer('Number of pionering poles - 3 meters')
    pionering_poles_6m_total = fields.Integer('Number of pionering poles - 6 meters')
    pionering_poles_9m_total = fields.Integer('Number of pionering poles - 9 meters')
    handicap = fields.Boolean('Participant(s) with handicap or other special considerations?')
    handicap_description = fields.Text('Description of handicap / special considerations')
    handicap_needs = fields.Text('Special needs due to handicap / special considerations')
    friendship_group = fields.Boolean('Request placement with friendship group?')
    friendship_group_name = fields.Char('Friendship group name, association, country')
    friendship_group_info = fields.Text('Friendship group other info')
    group_camp_agreements = fields.Text('Official agreements')
    internal_information = fields.Text('Internal information',  groups="campos_event.group_campos_staff,campos_event.group_campos_admin")


class PreregistrationAgegroup(models.Model):
    _name = 'event.registration.agegroup'
    name = fields.Char('Age Group name', required=True)
    age_from = fields.Integer('From age', required=True)
    age_to = fields.Integer('To age', required=True)
    
class PreregistrationParticipants(models.Model):
    _name = 'event.registration.participants'
    registration_id = fields.Many2one('event.registration', 'Registration')
    participant_age_group_id = fields.Many2one('event.registration.agegroup','Age Group')
    participant_total  = fields.Integer('Number of participants', required=True)
    participant_from_date = fields.Date('Date of arrival', required=True)
    participant_to_date = fields.Date('Date of departure', required=True)
    participant_transport_to_camp_total  = fields.Integer('Number of transport to camp', required=True)
    participant_transport_from_camp_total  = fields.Integer('Number of transport from camp', required=True)
    participant_transport_note = fields.Char(compute = '_calculate_note', string='Not all participants with transport')
    
    @api.depends ('participant_total','participant_transport_to_camp_total','participant_transport_from_camp_total')
    @api.multi
    def _calculate_note (self):
        for record in self:
            if record.participant_transport_to_camp_total!=record.participant_total or record.participant_transport_from_camp_total!=record.participant_total:
                record.participant_transport_note = 'NB!'
    
