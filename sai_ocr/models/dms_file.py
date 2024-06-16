import requests

from odoo import api, fields, models


class File(models.Model):
    _inherit = "dms.file"

    entitiy_id = fields.Char("Entitiy Id")
    send_response_json = fields.Char("Send Response JSON")
    send_ocr = fields.Boolean("Send OCR", compute="_compute_send_ocr")
    receive_ocr = fields.Boolean("Receive OCR", compute="_compute_receive_ocr")
    receive_response_json = fields.Char("Receive Response JSON")

    @api.depends("send_response_json")
    def _compute_send_ocr(self):
        for rec in self:
            rec.send_ocr = False
            if not rec.send_response_json:
                rec.send_ocr = True

    @api.depends("send_response_json", "receive_response_json")
    def _compute_receive_ocr(self):
        for rec in self:
            rec.receive_ocr = False
            if rec.send_response_json and not rec.receive_response_json:
                rec.receive_ocr = True

    def action_send_ocr(self):
        xuser = self.env.user.company_id

        workspace_id = xuser.sai_workspace_id
        project_id = xuser.sai_invoice_project_id
        api_url = xuser.sai_api_url
        api_key = xuser.sai_api_key

        # url = f"https://go.v7labs.com/api/workspaces/{workspace_id}"
        #       /projects/{project_id}/entities"

        url = f"{api_url}/workspaces/{workspace_id}/projects/{project_id}/entities"

        headers = {"X-API-KEY": api_key}

        xfile = "https://docs.swissuplabs.com/images/m2/pdf-invoices/\
                frontend/invoice-stripes.png"

        for rec in self:
            payload = {
                "fields": {
                    "invoice": {
                        "file_name": rec.name,
                        "file_url": xfile,
                    }
                }
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            rec.send_response_json = response.json()
            rec.entitiy_id = response.json()["id"]

    def action_receive_ocr(self):
        # print(self)
        return
