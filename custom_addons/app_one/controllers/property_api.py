import math
from urllib.parse import parse_qs

from PIL.ImageChops import offset

from odoo import http
from odoo.http import request
import json

def valid_response(data , status ,pagination_info):
    response_body={
        'data' : data
        }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error , status):
    response_body={
        'error' : error
        }
    return request.make_json_response(response_body, status=status)

# class PropertyApi(http.Controller):
#     @http.route(['/v1/property'],methods=["POST"], type='http', auth='none', csrf=False)
#     def posy_property(self):
#         args = request.httprequest.data.decode()
#         vals =  json.loads(args)
#         if not vals.get('name'):
#             return request.make_json_response({
#                 "message": "name is required !!",
#             },status=404)
#         try:
#             res = request.env['property'].sudo().create(vals)
#             if res:
#                 return valid_response({
#                     "name": res.name,
#                     "id": res.id,
#                 },status=201)
#         except Exception as e:
#             return invalid_response(str(e),status=400)

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
            # res = request.env['property'].sudo().create(vals)
            cr = request.env.cr
            columns = ','.join(vals.keys())
            values = ','.join(['%s'] * len(vals))
            query = f"""INSERT INTO property ({columns}) VALUES ({values}) RETURNING id,name ,postcode"""
            cr.execute(query, tuple(vals.values()))
            res = cr.fetchone()
            if res:
                return request.make_json_response({
                    "id": res[0],
                    "name": res[1],
                    "postcode" : res[2],
                },status=201)
        except Exception as e:
            return invalid_response(str(e),status=400)


    @http.route("/v1/property/<int:property_id>" , methods=["PUT"], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try :
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Property does not exist !!",
                },status=404)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
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

    @http.route("/v1/properties", methods=["GET"], type='http', auth='none', csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain=[]
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                property_domain += (('state' , '=' , params.get('state')[0]))
            property_ids = request.env['property'].sudo().search(property_domain, offset=offset,limit=limit , order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)
            print(page)
            print(limit)

            if not property_ids:
                return invalid_response("There are not records !!", status=404)
            return valid_response([{
                    "id": property_id.id,
                    "name": property_id.name,
                    "postcode": property_id.postcode,
            }for property_id in property_ids], pagination_info={
                  'page' : page if page else 0,
                  'limit' : limit ,
                  'pages' :math.ceil (property_count / limit) if limit else 1,
                   'count' :property_count
                     } , status=200)
        except Exception as e:
            return invalid_response( str(e), status=404)