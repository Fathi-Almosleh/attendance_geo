# -*- coding: utf-8 -*-
from odoo import fields, models


class HrAttendanceWorkLocation(models.Model):
    _name = "hr.attendance.work.location"
    _description = "Attendance Work Location"
    _order = "name"

    name = fields.Char(required=True)
    latitude = fields.Float(string="Latitude", digits=(16, 8), required=True)
    longitude = fields.Float(string="Longitude", digits=(16, 8), required=True)
    radius_m = fields.Integer(string="Allowed Radius (m)", default=100, required=True)
    active = fields.Boolean(default=True)
