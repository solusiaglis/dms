import base64
import hashlib
import json
import logging
from collections import defaultdict

from PIL import Image

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import consteq, human_size
from odoo.tools.mimetypes import guess_mimetype

import requests

class File(models.Model):
    _inherit = "dms.file"

    entitiy_id = fields.Char(string="Entitiy Id")
    send_response_json = fields.Char(string="Send Response JSON")
    send_ocr = fields.Boolean(string="Send OCR", compute='_send_ocr') 
    receive_ocr = fields.Boolean(string="Receive OCR", compute='_receive_ocr') 
    receive_response_json = fields.Char(string="Receive Response JSON")

    @api.depends('send_response_json')
    def _send_ocr(self):
        for rec in self:
            rec.send_ocr = False
            if not rec.send_response_json:
                rec.send_ocr = True

    @api.depends('send_response_json','receive_response_json')
    def _receive_ocr(self):
        for rec in self:
            rec.receive_ocr = False
            if rec.send_response_json and not rec.receive_response_json:
                rec.receive_ocr = True

    def action_send_ocr(self):
        # workspace_id = '018fba0e-36a5-7bc9-b3e5-05855a03a910'
        # project_id = '018fbae8-dd71-7601-bab4-2104233323e3'
        # api_key = 'UpLaoOe.896DWGDLRO2P8f5eGklZ8oQ1tuRXDQs-'

        xuser = self.env.user.company_id

        workspace_id = xuser.sai_workspace_id
        project_id = xuser.sai_invoice_project_id
        api_key = xuser.sai_api_key

        url = f"https://go.v7labs.com/api/workspaces/{workspace_id}/projects/{project_id}/entities"

        headers = { "X-API-KEY": api_key }

        for rec in self:
            payload = {
                        "fields": {
                            "invoice": {
                                    "file_name": rec.name,
                                    "file_url": "https://docs.swissuplabs.com/images/m2/pdf-invoices/frontend/invoice-stripes.png"
                                    }
                                }
                    }
            response = requests.post(url, json=payload, headers=headers)
            rec.send_response_json = response.json()
            rec.entitiy_id = response.json()['id']


    def action_receive_ocr(self):
        print(self)
