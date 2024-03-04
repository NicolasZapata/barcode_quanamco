from odoo import _, api, fields, models
import random


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_class_code = fields.Char(
        "Product Class Code",
        tracking=True,
        related="product_class_id.code",
    )
    default_code = fields.Char(
        "Internal Reference",
        index=True,
        default=lambda self: 45 + random.randint(00, 99),
    )
    categ_code = fields.Char(
        "Category Code",
        related="categ_id.code",
    )
    product_class_id = fields.Many2one(
        "product.class",
        string="Product Class",
    )
    brand_code = fields.Char(string="Brand", related="product_brand_id.code")
    material_code = fields.Char(string="Material", related="product_material_id.code")
    barcode = fields.Char(
        "Barcode",
        copy=False,
        store=True,
        index="btree_not_null",
        compute="_auto_complete_barcode",
        help="International Article Number used for product identification.",
    )

    # Conformación del código de barras
    def _auto_complete_barcode(self):
        """
        Código 1: Category Code
        Código 2: Class Code
        Código 3: La Marca
        Código 4: Material
        por ende
        | Categoría | Clase de Código | Marca | Material | Consecutivo |
        """
        for record in self:
            qr_code = []
            if record.categ_code:
                qr_code.append(record.categ_code)
            elif record.categ_code == '':
                qr_code.append('00')

            if record.product_class_code:
                qr_code.append(record.product_class_code)
            elif record.product_class_code == '':
                qr_code.append('00')

            if record.product_brand_id:
                qr_code.append(record.product_brand_id.code)
            elif not record.product_brand_id.code:
                qr_code.append('00')

            if record.product_material_id:
                qr_code.append(record.product_material_id.code)
            elif not record.product_material_id:
                qr_code.append('00')

            if record.default_code:
                qr_code.append(record.default_code)
            elif not record.default_code:
                qr_code.append('0000')
            record.barcode = "".join(qr_code)
