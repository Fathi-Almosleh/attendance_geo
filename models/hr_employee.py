# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def attendance_manual(self, next_action, entered_pin=None, location=False, note=False):
        # Pass extra data through context so we can write it on the created/updated attendance record.
        ctx = dict(self.env.context)
        if location:
            ctx["attendance_location"] = location
        if note:
            ctx["attendance_note"] = note
        return super(HrEmployee, self.with_context(ctx)).attendance_manual(next_action, entered_pin)

    def _attendance_action_change(self):
        attendance = super()._attendance_action_change()

        location = self.env.context.get("attendance_location")
        note = self.env.context.get("attendance_note")

        if not location:
            return attendance

        try:
            lat = float(location[0])
            lon = float(location[1])
        except Exception:
            return attendance

        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        vals = {}
        if self.attendance_state == "checked_in":
            vals.update({
                "checkin_latitude": lat,
                "checkin_longitude": lon,
                "checkin_url": maps_url,
            })
            if note:
                vals["checkin_note"] = note
        else:
            vals.update({
                "checkout_latitude": lat,
                "checkout_longitude": lon,
                "checkout_url": maps_url,
            })
            if note:
                vals["checkout_note"] = note

        attendance.write(vals)
        return attendance
