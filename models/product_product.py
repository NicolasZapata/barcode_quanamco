from odoo import _, api, fields, models
import random


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "barcode desc"

    product_reference_id = fields.Many2one(
        "product.reference",
        string="Product Reference",
        tracking=True,
    )
    product_class_code = fields.Char(
        "Product Class Code",
        tracking=True,
        related="product_class_id.code",
    )
    default_code = fields.Char(
        "Internal Reference",
        index=True,
        # default=lambda self: 45,
        default=45,
        store=True,
    )
    sequency = fields.Char("Sequency", default=lambda self: random.randint(00, 99))
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
        # copy=False,
        compute="_auto_complete_barcode",
        # index="btree_not_null",
        help="International Article Number used for product identification.",
        store=True,
    )

    # Conformación del código de barras
    @api.depends(
        "categ_code",
        "product_class_code",
        "product_brand_id",
        "product_material_id",
        "default_code",
        "sequency",
        "barcode",
    )
    def _auto_complete_barcode(self):
        """
        Categoria(2) + Clase(2) + material(2) + Marca(3) + Referencia de producto(2) + secuencia(2)

             99      +  99      +     99      +    999   +             99            +     99

        Ejemplo:
        45+02+02+123+01+01
        45+02+00+000+01+02
        45+02+01+045+00+03
        45+02+01+045+12+04
        """
        for record in self:
            qr_code = []
            if record.categ_code:
                qr_code.append(record.categ_code)
            elif not record.categ_code:
                qr_code.append("00")

            if record.product_class_code:
                qr_code.append(record.product_class_code)
            elif not record.product_class_code:
                qr_code.append("00")

            if record.product_brand_id:
                qr_code.append(record.product_brand_id.code)
            elif not record.product_brand_id.code:
                qr_code.append("00")

            if record.product_material_id:
                qr_code.append(record.product_material_id.code)
            elif not record.product_material_id:
                qr_code.append("00")

            if record.default_code:
                qr_code.append(record.default_code)
            elif not record.default_code:
                qr_code.append("00")

            if record.sequency:
                qr_code.append(record.sequency)

            record.barcode = "".join(qr_code)
