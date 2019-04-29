# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)

class CamposSnapshot(models.Model):

    _name = 'campos.snapshot'
    _description = 'Campos Snapshot'  # TODO

    name = fields.Char()
    code = fields.Char(size=16)
    state = fields.Selection([('draft', 'Draft'),
                              ('inprogress', 'In Progress'),
                              ('completed', 'Completed')], default='draft', string='State', track_visibility='onchange')

    ssreg_ids = fields.One2many('campos.ss.group.reg', 'snapshot_id', 'Registration Snapshot')
    ss_date = fields.Datetime('Snapshot Date')
    
    @api.multi
    def action_do_snapshot(self):
    
        
        for ss in self:
            ss.state = 'inprogress'
            ss.ss_date = fields.Datetime.now()
            for reg in self.env['campos.group.reg'].search([]):
                _logger.info('SS: %s %d Reg %s', ss, ss.id, reg)
                reg.do_snapshot(ss)
            ss.state = 'completed'