# -*- coding: utf-8 -*-
{
    "name": "Attendance GPS + Notes + Work Location Radius",
    "version": "16.0.1.0.0",
    "category": "Human Resources/Attendances",
    "summary": "Store GPS/URL/notes for check in/out and optionally restrict by configured work locations & radius.",
    "depends": ["hr_attendance", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/hr_attendance_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "odoo_attendance_user_location_note/static/src/js/attendance_note_gps_hook.js",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
