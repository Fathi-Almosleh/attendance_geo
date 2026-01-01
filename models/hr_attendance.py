# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import math

def _haversine_m(lat1, lon1, lat2, lon2):
    """Returns distance in meters between two WGS84 points."""
    r = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    checkin_latitude = fields.Float(string="Check-in Latitude", digits=(16, 8), readonly=True, copy=False)
    checkin_longitude = fields.Float(string="Check-in Longitude", digits=(16, 8), readonly=True, copy=False)
    checkin_url = fields.Char(string="Check-in Location URL", readonly=True, copy=False)
    checkin_note = fields.Char(string="Check-in Note", readonly=True, copy=False)

    checkout_latitude = fields.Float(string="Check-out Latitude", digits=(16, 8), readonly=True, copy=False)
    checkout_longitude = fields.Float(string="Check-out Longitude", digits=(16, 8), readonly=True, copy=False)
    checkout_url = fields.Char(string="Check-out Location URL", readonly=True, copy=False)
    checkout_note = fields.Char(string="Check-out Note", readonly=True, copy=False)

    def _check_within_allowed_locations(self, employee, lat, lon, action_label):
        """Validate (lat, lon) is within at least one configured location radius for the employee's user.
        If the user has no configured locations, do nothing (no restriction).
        """
        user = employee.user_id
        if not user:
            return

        locations = user.work_location_ids.filtered(lambda l: l.active)
        if not locations:
            return  # no restriction configured

        for loc in locations:
            if loc.latitude is None or loc.longitude is None or not loc.radius_m:
                continue
            dist = _haversine_m(lat, lon, loc.latitude, loc.longitude)
            if dist <= loc.radius_m:
                return

        raise UserError(_(
            "%(action)s is not allowed from your current location. "
            "Please move داخل دائرة أحد مواقع العمل المسموحة ثم أعد المحاولة."
        ) % {"action": action_label})

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Validate check-in when coordinates are provided
        for rec, vals in zip(records, vals_list):
            if vals.get("check_in") and vals.get("checkin_latitude") is not None and vals.get("checkin_longitude") is not None:
                try:
                    rec._check_within_allowed_locations(
                        rec.employee_id,
                        float(vals["checkin_latitude"]),
                        float(vals["checkin_longitude"]),
                        _("Check-in"),
                    )
                except (ValueError, TypeError):
                    # If parsing fails, don't block
                    pass
        return records

    def write(self, vals):
        # Validate check-out when coordinates are provided
        if "check_out" in vals and vals.get("checkout_latitude") is not None and vals.get("checkout_longitude") is not None:
            for rec in self:
                try:
                    rec._check_within_allowed_locations(
                        rec.employee_id,
                        float(vals["checkout_latitude"]),
                        float(vals["checkout_longitude"]),
                        _("Check-out"),
                    )
                except (ValueError, TypeError):
                    pass
        return super().write(vals)
