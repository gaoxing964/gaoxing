import sae
#sae.add_vendor_dir('myBlog/models')
from myapp import app

application = sae.create_wsgi_app(app)