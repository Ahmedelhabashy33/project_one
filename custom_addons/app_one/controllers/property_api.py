from odoo import http
from odoo.http import request
import json


class PropertyApi(http.Controller):
    @http.route(['/v1/property'],methods=["POST"], type='http', auth='none', csrf=False)
    def posy_property(self):
        args = request.httprequest.data.decode()
        vals =  json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "name is required !!",
            },status=404)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "Property created successfully",
                    "name": res.name,
                    "id": res.id,
                },status=201)
        except Exception as e:
            return request.make_json_response({
                "message": str(e),
            },status=400)


    @http.route("/v1/property/<int:property_id>" , methods=["PUT"], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try :
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Property does not exist !!",
                },status=404)
            print(property_id)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            print(vals)
            property_id.write(vals)
            print(property_id.garden_area)
            return request.make_json_response({
                "message": "Property updated successfully",
            },status=200)
        except Exception as e:
            return request.make_json_response({
                "message": str(e),
            },status=400)
    @http.route("/v1/property/<int:property_id>" , methods=["GET"], type='http', auth='none', csrf=False)
    def read_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message" : "Property does not exist !!",
                },status=404)
            return request.make_json_response({
                "message": "Property read successfully",
                "data": {
                    "id": property_id.id,
                    "name": property_id.name,
                    "postcode": property_id.postcode,
                },
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "message": str(e),
            },status=404)

    @http.route("/v1/property/<int:property_id>" , methods=["DELETE"], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        if not property_id:
            return request.make_json_response({
                "message": "Property does not exist !!",
            },status=404)
        else:
            try:
                property_id.unlink()
                return request.make_json_response({
                "message": "Property deleted successfully",

                },status=200)
            except Exception as e:
                return request.make_json_response({
                "message": str(e),
                },status=404)


