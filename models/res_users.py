# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    work_location_ids = fields.Many2many(
        comodel_name="hr.attendance.work.location",
        relation="res_users_hr_attendance_work_location_rel",
        column1="user_id",
        column2="location_id",
        string="Work Locations (Attendance)",
        help="If you add locations here, check-in/check-out will be allowed only داخل دائرة أحد هذه المواقع.",
    )
