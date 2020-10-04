
from odoo import models, fields, api,exceptions
from odoo.tools.translate import _
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
class JobPosition(models.Model):
    _inherit = 'hr.job'
    default_groub_crm = fields.Boolean(string='Default Groub Crm')
    default_esc_crm = fields.Boolean(string='Default Escalation Crm')
    is_presales_eng = fields.Boolean(string='Is Presales Engineer')