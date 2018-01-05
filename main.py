#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2

#           "GC_GET2/templates"
#       "GC_GET2"
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("NPU.html")

    def post(self):
        DNA_osumljenca = self.request.get("vnos")

        # splošni podatki - značilnosti, DNA
        DNA_zapis_lasje = ["CCAGCAATCGC", "GCCAGTGCCG", "TTAGCTATCGC"]
        DNA_zapis_obraz = ["GCCACGG", "ACCACAA", "AGGCCTCA"]
        DNA_zapis_oci = ["TTGTGGTGGC", "GGGAGGTGGC", "AAGTAGTGAC"]
        DNA_zapis_spol = ["TGAAGGACCTTC", "TGCAGGAACTTC"]
        DNA_zapis_rasa = ["AAAACCTCA", "CGACTACAG", "CGCGGGCCG"]

        opis_DNA_zapis_lasje = {"CCAGCAATCGC": "črni", "GCCAGTGCCG": "rjavi", "TTAGCTATCGC": "blond"}
        opis_DNA_zapis_obraz = {"GCCACGG": "kvadrat", "ACCACAA": "okrogel", "AGGCCTCA": "ovalen"}
        opis_DNA_zapis_oci = {"TTGTGGTGGC": "modre", "GGGAGGTGGC": "zelene", "AAGTAGTGAC": "rjave"}
        opis_DNA_zapis_spol = {"TGCAGGAACTTC": "moški", "TGAAGGACCTTC": "ženski"}
        opis_DNA_zapis_rasa = {"AAAACCTCA": "bela", "CGACTACAG": "črna", "CGCGGGCCG": "azijska"}

        # iskanje ujemanja DNA osumljencev
        DNA_ujemanja = []

        try:
            for item in DNA_zapis_spol:
                if item in DNA_osumljenca:
                    DNA_ujemanja.append(opis_DNA_zapis_spol[item])
            for item in DNA_zapis_rasa:
                if item in DNA_osumljenca:
                    DNA_ujemanja.append(opis_DNA_zapis_rasa[item])
            for item in DNA_zapis_lasje:
                if item in DNA_osumljenca:
                    DNA_ujemanja.append(opis_DNA_zapis_lasje[item])
            for item in DNA_zapis_oci:
                if item in DNA_osumljenca:
                    DNA_ujemanja.append(opis_DNA_zapis_oci[item])
            for item in DNA_zapis_obraz:
                if item in DNA_osumljenca:
                    DNA_ujemanja.append(opis_DNA_zapis_obraz[item])

            # izpis rezultatov DNK analize
            opisne_lastnosti = ["spol osebe", "rasa", "barva las", "barva oči", "oblika obraza"]

            return self.write("Analizirana DNA ustreza naslednjim lastnostim:<br />"
                              "{0}: {1}<br />"
                              "{2}: {3}<br />"
                              "{4}: {5}<br />"
                              "{6}: {7}<br />"
                              "{8}: {9}".format(opisne_lastnosti[0], DNA_ujemanja[0], opisne_lastnosti[1], DNA_ujemanja[1],
                                                opisne_lastnosti[2], DNA_ujemanja[2], opisne_lastnosti[3], DNA_ujemanja[3],
                                                opisne_lastnosti[4], DNA_ujemanja[4]))
        except IndexError:
            return self.write("Vnešeno DNA zaporedje se ne ujema z lastnostmi, ki so v naši podatkovni bazi")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
