import re
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char()
    image = fields.Image(max_width=290, max_height=290)
    author_ids = fields.Many2one('res.partner', string='Author')
    qty_in_stock = fields.Integer(string='Quantity in Stock')
    num_of_pages = fields.Integer(string='Number of Pages')
    tag_ids = fields.Many2many('library.tag', string='Tags')
    reader_ids = fields.Many2one('library.reader')
    isbn_10 = fields.Char(string='ISBN 10')
    description = fields.Text(string='Description')
    category_ids = fields.Many2many('library.book.category')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Title must be unique'),
    ]

    @api.constrains('isbn_10')
    def _check_isbn_10_format(self):
        for book in self:
            if book.isbn_10:
                pattern = r'^\d{9}(\d|X)$'
                if not re.match(pattern, book.isbn_10):
                    raise ValidationError("ISBN-10 format is invalid. It should be 10 digits or 9 digits followed by 'X'. Example: 007462542X")
                else:
                    if not self._is_valid_isbn_10(book.isbn_10):
                        raise ValidationError("ISBN-10 is not valid.")

    def _is_valid_isbn_10(self, isbn_10):
        if isbn_10:
            isbn_digits = [int(digit) if digit != 'X' else 10 for digit in isbn_10]
            weighted_sum = sum((10 - i) * digit for i, digit in enumerate(isbn_digits[:9]))
            return (weighted_sum + isbn_digits[9]) % 11 == 0
        return False

    @api.constrains('qty_in_stock')
    def _check_qty_in_stock(self):
        for book in self:
            if book.qty_in_stock < 0:
                raise ValidationError("Quantity in stock cannot be negative.")
            

    @api.constrains('num_of_pages')
    def _check_num_of_pages(self):
        for book in self:
            if book.num_of_pages < 0:
                raise ValidationError("Numbers of pages cannot be negative.")