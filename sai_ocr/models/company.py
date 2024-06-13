# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta, datetime, date
import calendar

from odoo import fields, models, api, _, Command
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from odoo.tools.mail import is_html_empty
from odoo.tools.misc import format_date
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.addons.account.models.account_move import MAX_HASH_VERSION


MONTH_SELECTION = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]

ONBOARDING_STEP_STATES = [
    ('not_done', "Not done"),
    ('just_done', "Just done"),
    ('done', "Done"),
]
DASHBOARD_ONBOARDING_STATES = ONBOARDING_STEP_STATES + [('closed', 'Closed')]


class ResCompany(models.Model):
    _inherit = "res.company"

    sai_api_key = fields.Char(string="API Key")
    sai_workspace_id = fields.Char(string="Workspace Id")
    sai_journal_project_id = fields.Char(string="Journal Project Id")
    sai_bill_project_id = fields.Char(string="Bill Project Id")
    sai_invoice_project_id = fields.Char(string="Invoice Project Id")

