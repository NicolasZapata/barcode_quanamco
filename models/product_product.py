from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sequence_counter = fields.Integer(
        "Sequence Counter",
        default=1,
        help="Counter for generating unique sequences for products.",
    )

class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "sequency"

    product_reference_id = fields.Many2one(
        "product.reference",
        string="Product Reference",
        tracking=True,
    )
    product_reference_code = fields.Char(
        "Product Reference Code", related="product_reference_id.code"
    )
    sequency = fields.Integer(
        "Sequency",
        required=False,
    )

    barcode = fields.Char(
        "Barcode",
        compute="_auto_complete_barcode",
        readonly=False,
        store=True,
    )

    @api.model
    def create(self, vals):
        """
        Al guardarse:
            . . . . .  secuencia
            00000000022-> 02 <-
            00000000022-> 03 <-
            00000000022-> 04 <-
            . . . . . . . . . .
            00000000022-> n1n2 <-
        """
        # Incrementa el valor de la secuencia específica para la variante
        vals["sequency"] = self._get_next_sequency(vals.get("product_tmpl_id"))
        record = super(ProductProduct, self).create(vals)
        # Llama a la función para completar el código de barras solo si hay datos suficientes
        if record.categ_code and record.product_reference_code:
            record._auto_complete_barcode()
        return record

    def _get_next_sequency(self, template_id):
        template = self.env["product.template"].browse(template_id)
        return template.sequence_counter + 1

    @api.depends(
        "categ_code",
        "product_class_code",
        "product_brand_code",
        "product_material_code",
        "product_reference_code",
        "sequency",
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
        Auto-generates a barcode based on various fields.
        This method constructs a QR code by concatenating values from different fields
        (such as `categ_code`, `product_class_code`, etc.) and assigns the resulting
        barcode to the `barcode` field of the current record.
        :return: None
        """
        for record in self:
            if record.categ_code and record.product_reference_code:
                qr_code = []
                # Add category code or default "00"
                if record.categ_code:
                    qr_code.append(record.categ_code)
                elif not record.categ_code:
                    qr_code.append("00")
                # Add product class code or default "00"
                if record.product_class_code:
                    qr_code.append(record.product_class_code)
                elif not record.product_class_code:
                    qr_code.append("")
                # Add product material code or default "00"
                if record.product_material_id:
                    qr_code.append(record.product_material_code)
                elif not record.product_material_id:
                    qr_code.append("00")
                # Add product brand code or default "000"
                if record.product_brand_id:
                    qr_code.append(record.product_brand_code)
                elif not record.product_brand_id.code:
                    qr_code.append("000")
                # Add product reference code or default "00"
                if record.product_reference_code:
                    qr_code.append(record.product_reference_code)
                elif not record.product_reference_code:
                    qr_code.append("00")
                # Add custom sequence (if available)
                if record.sequency:
                    qr_code.append(str(record.sequency).zfill(2))
                else:
                    qr_code.append(str(record._get_next_sequency(record.product_tmpl_id.id)).zfill(2))
                # Join all components to form the final barcode
                record.barcode = "".join(qr_code)
