from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date, datetime

class LibraryReader(models.Model):
    _name = 'library.reader'
    _description = 'Library Reader'
    _rec_name = 'name'

    name = fields.Char()
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    book_ids = fields.One2many('library.book', 'reader_ids', string='Books')

    @api.depends('dob')
    def _compute_age(self):
        today = datetime.today().date()
        for reader in self:
            if reader.dob:
                delta = today - reader.dob
                age_years = delta.days // 365
                if age_years < 12:
                    raise ValidationError('Age must be greater than 12 for a reader.')
                else:
                    reader.age = age_years

    _sql_constraints = [
        ('unique_name_date_of_birth', 'UNIQUE(name, dob)', 'A reader with the same name and date of birth already exists.')
    ]