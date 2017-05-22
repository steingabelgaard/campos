# -*- coding: utf-8 -*-
# Copyright 2017 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class CamposActivityInstanse(models.Model):

    _name = 'campos.activity.instanse'
    _description = 'Campos Activity Instanse' 
    _order = 'actins_date_begin'
    _inherit = 'mail.thread'
    
    name = fields.Char('Name', size=128, translate=True)
    seats_max = fields.Integer('Maximum Avalaible Seats')
    seats_hard = fields.Boolean('Hard limit')
    seats_reserved = fields.Integer('Reserved Seats', compute='_compute_seats')
    seats_available = fields.Integer('Available Seats', compute='_compute_seats')
    seats_used = fields.Integer('Number of Participations', compute='_compute_seats')
    ticket_ids = fields.One2many('campos.activity.ticket', 'act_ins_id', 'Tickets')
    
    #'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name', multi='seats_reserved'),
    activity_id = fields.Many2one('campos.activity.activity', 'Activity')
    period_id = fields.Many2one('campos.activity.period', 'Period')
    staff_ids = fields.Many2many('campos.event.participant','campos_activity_staff_rel', 'act_ins_id','par_id','Staff', domain=[('staff', '=', True)])
    #ticket_ids = fields.One2many('campos.activity.ticket', 'act_ins_id', 'Tickets')
    actins_date_begin = fields.Datetime(related='period_id.date_begin', string='Start Date/Time', store=True)
    actins_date_end = fields.Datetime(related='period_id.date_end', string='End Date/Time', store=True)
    location_id = fields.Many2one('campos.activity.location', 'Location')
    booking = fields.Selection([('dropin', 'Drop In'),
                                ('dropin_prebook', 'Drop In & Pre Booking'),
                                ('precamp', 'Pre Camp Booking Required'),
                                ('prebook', 'Booking required')], 'Booking')
    
    state = fields.Selection([('open', 'Open'),
                                ('cancelled', 'Cancelled'),
                                ('canc_weather', 'Cancelled due to weather'),
                                ('canc_risk', 'At risk of cancellation due to weather conditions')], 'State', default='open')
    
    
    @api.onchange('activity_id','period_id')
    def on_change_actper(self):
        if self.activity_id and self.period_id:
            self.name = '%s - %s' % (self.activity_id.display_name, self.period_id.display_name)

    @api.depends('ticket_ids')
    @api.multi
    def _compute_seats(self):
        res = {}
        for a in self.ids:
            res[a.id] = {'open': 0, 'done': 0}
        tables, where_clause, where_params = self.env['campos.activity.ticket']._query_get()
        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
        self._cr.execute("""SELECT act_ins_id, state, SUM(seats)
                      FROM campos_activity_ticket
                      WHERE act_ins_id IN %s
                      """ + where_clause + """
                      GROUP BY act_ins_id, state,
                      """, where_params)
        for aid, state, val in self._cr.fetchall():
            res[aid][state] = val
        
        for a in self.ids:    
            a.seats_reserved = res[a.id]['open']
            a.seats_used = res[a.id]['done']
            a.seats_available = a.seats_max - \
                (res[a.id]['open'] + res[a.id]['done']) \
                if a.seats_max > 0 else None
    
    