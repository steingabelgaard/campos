
from odoo import http
# from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin
from odoo.addons.cms_form.controllers.main import FormControllerMixin
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin

class GroupRegForm(http.Controller, FormControllerMixin):
    """Partner form w/ tabs."""

    @http.route([
        '/group_reg/<model("campos.group.reg"):main_object>/edit',
    ], type='http', auth='user', website=True)
    def cms_form(self, main_object=None, **kw):
        model = 'campos.group.reg'
        return self.make_response(
            model, model_id=main_object and main_object.id, **kw)

    def form_model_key(self, model, **kw):
        """Return a valid form model."""
        return 'cms.form.campos.group.reg'

class ParticipantForm(http.Controller, FormControllerMixin):
    """Partner form w/ tabs."""

    @http.route([
        '/participant/add',
        '/participant/<model("campos.participant"):main_object>/edit',
    ], type='http', auth='user', website=True)
    def cms_form(self, main_object=None, **kw):
        model = 'campos.participant'
        return self.make_response(
            model, model_id=main_object and main_object.id, **kw)

    def form_model_key(self, model, **kw):
        """Return a valid form model."""
        return 'cms.form.campos.participant'


class ParticipantListing(http.Controller, SearchFormControllerMixin):
    """Partner search form controller."""

    @http.route([
        '/participants',
        '/participants/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'campos.participant'
        return self.make_response(model, **kw)

    def form_model_key(self, model, **kw):
         """Return a valid form model."""
         return 'cms.search.campos.participant'
