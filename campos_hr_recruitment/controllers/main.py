
from odoo import http, _
from odoo.http import request
from addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment 


class CamposHrRecruitment(WebsiteHrRecruitment):

    @http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):
        error = {}
        default = {}
        countries = request.env['res.country'].search([])
        country_da_id = request.env.ref('base.dk').id
        
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("campos_hr_recruitment.apply", {
            'job': job,
            'error': error,
            'default': default,
            'countries': countries,
            'country_da_id': country_da_id,
        })