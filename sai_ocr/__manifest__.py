# -*- coding: utf-8 -*-
# Part of HG Custom Modules.
{
    "name": "Odoo 16 OCR",
    "author": "HERRY GOUW",
    "category": "Extra Tools",
    "license": "OPL-1",
    "website": "https://github.com/OCA/dms",
    "summary": "OCR",
    "description": """This module is useful for DMS integration to OCR.""",
    "version": "16.0.1.0.0",
    "depends": ["base", "base_setup", "dms"],
    "application": True,
    "assets": {
        "web.assets_backend": [
        ],
        "web.assets_qweb": [
        ],
    },
    "data": [
        'views/res_config_settings_views.xml',
        'views/dms_file.xml',
    ],
    "images": ["static/description/icon.jpg", ],
    "auto_install": False,
    "installable": True,
}
