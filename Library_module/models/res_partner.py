from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    library_ids = fields.One2many('library.book', 'author_ids')
    is_author = fields.Boolean()
    