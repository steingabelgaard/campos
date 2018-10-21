
from odoo import http
# from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin
from odoo.addons.cms_form.controllers.main import FormControllerMixin


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
