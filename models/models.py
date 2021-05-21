# -*- coding: utf-8 -*-
from odoo import models, fields, api
import xmlrpc.client

class method_correos_dte(models.Model):
    _name = 'method_correos_dte.correos_dte'

    name = fields.Char(string="Nombre del contribuyente")
    rut = fields.Char(string="Rut del contribuyente")
    nro_resolucion = fields.Char(string="Número Resolucion del SII")
    fecha_resolucion = fields.Date(string='Fecha Resolucion del SII')
    email_dte = fields.Char(string='Correo Electrónico de Intercambio')
    url = fields.Char(string="URL contribuyente")
    


class ModuleName(models.Model):
    _inherit = 'res.partner'

    @api.one
    def obtener_dte_email(self):
        url = 'http://170.239.87.131:8069'
        db = 'method'
        username = 'cesar@method.cl'
        password = '2010'
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        uid = common.authenticate(db, username, password, {})
        rut_partner=self.sii_document_number
        if rut_partner:
            dte_email=models.execute_kw(db, uid, password,
                'method_correos_dte.correos_dte', 'search_read',
                [[['rut', '=', rut_partner.replace('.','')]]],
                [])
            if dte_email:
                for i in dte_email:
                    self.dte_email=i['email_dte']

