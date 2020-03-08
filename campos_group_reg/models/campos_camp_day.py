# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

import locale
import contextlib

@contextlib.contextmanager
def setlocale(*args, **kw):
  saved = locale.setlocale(locale.LC_ALL)
  yield locale.setlocale(*args, **kw)
  locale.setlocale(locale.LC_ALL, saved)


class CamposCampDay(models.Model):

    _name = 'campos.camp.day'
    _description = 'Campos Camp Day'
    _rec_name = 'name'
    _order = 'campday'

    campday = fields.Date('Camp Day')
    name = fields.Char('Name')
    arrival_day = fields.Boolean('Arrival day')
    depature_day = fields.Boolean('Depature day')
    valid_dk = fields.Boolean('Arrival/Departure valid for DK Groups')
    valid_non_dk = fields.Boolean(
        'Arrival/Departure valid for foreign  Groups'
    )
    
    @api.onchange('campday')
    def onchange_campday(self):
        if not self.name and self.campday:
            with setlocale(locale.LC_ALL, 'da_DK.utf8'): 
                self.name = self.campday.strftime('%A %d/%m').capitalize()
