import rdflib
from rdflib import  BNode
from rdflib.namespace import RDF
import csv

g = rdflib.Graph()
result = g.parse("dataset/restaurants.rdf")


ns_vcard = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#VCard")
ns_name = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#fn")
ns_address = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#adr")
ns_tel = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#tel")
ns_tel_value = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#value")
ns_geo = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#geo")
ns_vcard_geo = rdflib.URIRef("http://www.bcn.cat/data/v8y/xvcard#geo")
ns_district = rdflib.URIRef("http://www.bcn.cat/data/v8y/xvcard#district")
ns_neighborhood = rdflib.URIRef("http://www.bcn.cat/data/v8y/xvcard#neighborhood")
ns_street_address = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#street-address")

ns_longitude = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#longitude")
ns_latitude = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#latitude")
ns_postal_code = rdflib.URIRef("http://www.w3.org/2006/vcard/ns#postal-code")

with open('dataset/bcn_restaurant.csv', 'w') as csvfile:
    fieldnames = ['name', 'street_address', 'district', 'neighborhood', 'postal-code',
                  'telephone', 'latitude','longitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    for rdf_restaurant in result.subjects(RDF.type, ns_vcard):
        restaurant = { 'name': None, 'street_address': None, 'district': None,
                       'neighborhood': None, 'postal-code': None, 'latitude': None,
                       'longitude': None }

        restaurant['name'] = result.objects(rdf_restaurant,ns_name).next()

        address_bnode  = BNode(result.objects(rdf_restaurant, ns_address).next())
        restaurant['street_address'] = result.objects(address_bnode, ns_street_address).next()
        restaurant['postal-code']    = result.objects(address_bnode, ns_postal_code).next()
        restaurant['district']       = result.objects(address_bnode, ns_district).next()

        if len(list(result.objects(address_bnode, ns_neighborhood))) > 0:
            restaurant['neighborhood']   = result.objects(address_bnode, ns_neighborhood).next()

        if len(list(result.objects(rdf_restaurant, ns_tel))) > 0:
            tel_bnode  = BNode(result.objects(rdf_restaurant, ns_tel).next())
            restaurant['telephone'] = result.objects(tel_bnode, ns_tel_value).next()

        geo_subject = rdflib.URIRef(result.objects(address_bnode, ns_vcard_geo).next())
        restaurant['latitude']    = result.objects(geo_subject, ns_latitude).next()
        restaurant['longitude']   = result.objects(geo_subject, ns_longitude).next()

        writer.writerow(restaurant)
