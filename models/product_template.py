from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "mail.thread", "mail.activity.mixin"]
    _description = "Product Template"

    category_code = fields.Char("Category Code", related="categ_id.code", tracking=True)
    product_class_id = fields.Many2one(
        "product.class",
        string="Product Class",
        tracking=True,
    )
    product_class_code = fields.Char(
        "Product CLass Code",
        related="product_class_id.code",
        tracking=True,
    )
