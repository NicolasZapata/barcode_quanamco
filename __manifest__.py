{
  'name': 'Barcode module by Grupo Quanam Colombia',
  'version': '1.0',
  'description': 'This is a module that generates barcodes for storage products from product categories.',
  'summary': '',
  'author': 'Grupo Quanam Colombia SAS',
  'website': 'https://grupoquanam.com.co',
  'license': 'LGPL-3',
  'category': 'barcode',
  'depends': [
    'product',
    'mail',
    'sale',
  ],
  'data': [
    'security/ir.model.access.csv',
    'views/product_category.xml',
    'views/product_template.xml',
    'views/product_class_view.xml',
    'views/product_product_view.xml',
  ],
  'demo': [
    ''
  ],
  'auto_install': False,
  'application': False,
  'assets': {
    
  }
}