from odoo import models, fields, _


class cmsParticipantForm(models.AbstractModel):
    """A test model form."""

    _name = 'cms.form.campos.participant'
    _inherit = 'cms.form'
    _form_model = 'campos.participant'
    _form_model_fields = (
        'name',
        #  'street', 'street2', 'zip', 'city',
        # 'country_id',
        #'gender',
        'age_group_id',
        'arrival_date_id',
        'depature_date_id',
        'participant_state',
    )
    _form_required_fields = (
        'name',
        #'gender',
        'age_group_id',
        'arrival_date_id',
        'depature_date_id',
    )
    _form_fields_order = (
        'name',
        #'street', 'street2', 'zip', 'city',
        #'country_id',
        #'gender',
        'age_group_id',
        'arrival_date_id',
        'depature_date_id',
        'participant_state',
    )

    participant_state = fields.Selection(
        [('confirmed', 'Participate'), ('cancelled', 'Cancelled')],
        string="State",
        default='confirmed',
    )

    def form_before_create_or_update(self, values, extra_values):
        if extra_values.get('participant_state'):
            values['state'] = extra_values.get('participant_state')

    @property
    def form_msg_success_updated(self):
        return _('Participant updated.')

    @property
    def form_msg_success_created(self):
        # TODO: include form model name if any
        msg = _('Participant added.')
        return msg

    def form_next_url(self, main_object=None):
        if self.request.args.get('redirect'):
            # redirect overridden
            return self.request.args.get('redirect')
        return '/participants'


class cmsParticipantSearchForm(models.AbstractModel):
    """A test model form."""

    _name = 'cms.search.campos.participant'
    _inherit = 'cms.form.search'
    _form_model = 'campos.participant'

    _form_model_fields = 'name'

    form_buttons_template = 'campos_group_reg.participant_search_form_buttons'
    form_search_results_template = (
        'campos_group_reg.participant_search_results'
    )
