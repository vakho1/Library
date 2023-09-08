from odoo import fields, models


class Librarytag(models.Model):
    _name = 'library.tag'
    _description = 'library tag'

    name = fields.Char(string='Title')
    color = fields.Integer(string="Tag Color")