# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CamposParticipantDay(models.Model):

    _name = 'campos.participant.day'
    _description = 'Campos Participant Day'  # TODO

    name = fields.Char()
    participant_id = fields.Many2one('campos.participant', 'Participant')
    day_id = fields.Many2one('campos.camp.day', 'Day')
    
