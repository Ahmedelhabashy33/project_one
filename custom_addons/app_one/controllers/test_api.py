from odoo import http

print(">>>>>> test_api.py loaded")
class TestApi(http.Controller):
    @http.route(['/api/test'],methods=["GET"], type='http', auth='none' ,csrf=False)
    def  test_endpoint(self):
        print("inside test_endpoint method")