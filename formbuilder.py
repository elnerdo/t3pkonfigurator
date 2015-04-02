#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FormBuilder(object):

    def __init__(self):
        
        self.submit_form = '<form action="/t3pkonfigurator" method="post" id="t3psubmitform"> \
                    <input type="hidden" name="tube" value="{self.tube}"> \
                    <input type="hidden" name="offset" value="{self.offset}"> \
                    <input type="hidden" name="configuration" value="{self.configuration}"> \
                    <input type="hidden" name="summary" value="{self.summary}"> \
                    <div class="form-group"> \
                    <label for="first_name">Vorname</label> \
                    <input type="text" id="first_name" name="first_name" required> \
                    </div> \
                    <div class="form-group"> \
                    <label for="last_name">Nachname</label> \
                    <input type="text" id="last_name" name="last_name" required> \
                    </div> \
                    <div class="form-group"> \
                    <label for="company">Firma</label> \
                    <input type="text" id="company" name="company" required> \
                    </div> \
                    <div class="form-group"> \
                    <label for="company">Email</label> \
                    <input type="text" id="email" name="email" required> \
                    </div> \
                    <div class="form-group"> \
                    <label for="connector">Anschluss</label> \
                    <select id="connector" name="connector" required> \
                    <option value="">Bitte auswählen</option> \
                    <option value="IMP-BUS">IMP-BUS</option> \
                    <option value="SDI-12">SDI-12</option> \
                    <option value="RS-485">RS-485</option> \
                    </select> \
                    <input class="btn btn-primary"type="submit" value="Absenden"> \
                    </form>'

        self.form_deepest = '\
<form class="form-horizontal" action="/t3pkonfigurator" \
method="post" name="maxdepth">\
<div class="form-group">\
<label class="col-md-3" for="deepest">Tiefster Messpunkt in cm</label>\
<select class="col-md-3" id="deepest" name="deepest">\
{0}\
</select>\
<div class="col-md-2">\
<button id="deepest-btn" class="btn btn-primary">OK</button>\
</div>\
</div>\
</form>'

        self.test123 = '<a href="/t3pkonfigurator/static/t3p-config-22.347929.pdf" download>Download!</a>'

        self.deepest_option = '<option value={0}>{0}cm</option>'

        self.info_div = '\
<div>\
Ihre Messpunkte:<br>\
<ol>{0}</ol>\
</div>'

        self.info_div_element = '<li>{0}</li>'

        self.form_add_option = '<option value="{0}">{0}cm</option>'

        self.form_add_possible = '\
<form action="/t3pkonfigurator" method="post" name="additional_probe" \
id="additional_probe">\
<div class="form-group">\
<label class="col-md-3" for="add_probe">Weiterer Messpunkt:</label>\
<select class="col-md-3" name="add_probe" id="add_probe">\
{options}\
</select>\
</div>\
<input type="hidden" value="{depths}" name="depths" id="depths">\
<button class="btn btn-primary" id="add-btn">Add</button>\
</form>'

        self.form_add_impossible = '\
<form action="/t3pkonfigurator" method="post" name="additional_probe" \
id="additional_probe">\
<input type="hidden" value="{depths}" name="depths" id="depths">\
</form>'

        self.form_conf_done = '\
<form method="post" action="/t3pkonfigurator">\
<div id="summary">Ihre Messpunkte mit dem Tiefsten beginnend:<br>\
<ol>{depthlist}</ol>\
</div>\
<div id="tube">Sie brauchen ein {tube}cm Rohr</div>\
<div id="offset">Bodenabstand: {offset}cm</div><br>\
<p>Verbaute Teile:</p>{parts}\
<div class="form-group">\
<label for="connector">Anschluss: </label>\
<select id="connector" name="connector" required>\
<option value="">Bitte auswählen</option>\
<option value="IMP-BUS">IMP-BUS</option>\
<option value="SDI-12">SDI-12</option>\
<option value="RS-485">RS-485</option>\
</select>\
</div>\
<div class="form-group">\
<label for="cable">Kabellänge: </label>\
<select id="cable" name="cable" required>\
<option value="">Bitte auswählen</option>\
<option value="2m">2m</option>\
<option value="5m">5m</option>\
<option value="10m">10m</option>\
<option value="Spezial">Andere (auf Anfrage)</option>\
</select>\
</div>\
<div class="form-group">\
<label for="amount">Stückzahl: </label>\
<input id="amount" name="amount" type="number" required>\
</div>\
<div style="visibility:hidden;height:0;"id="config">{config}</div>\
<div id="control-btns">\
<input type="hidden" name="prepare_submit" value="1">\
<input type="hidden" name="tube" value="{tube}">\
<input type="hidden" name="offset" value="{offset}">\
<input type="hidden" name="summary" value="{depthlist}">\
<input type="hidden" name="configuration" value="{config}">\
<input type="submit" value="Weiter">\
</div>\
</form>'

    def build_deepest(self):
        options = '<option value="">Bitte auswählen</option>'
        for x in range(265,5,-5):
            options += self.deepest_option.format(x)
        return self.form_deepest.format(options)

    def build_add(self, possible_depths, depths):
        info_items = ''
        for i in depths:
            info_items += self.info_div_element.format(i)
        html = self.info_div.format(info_items)
        if not possible_depths:
            html += self.form_add_impossible.format(depths=depths) 
        else:
            options = ''
            for pd in possible_depths:
                options += self.form_add_option.format(pd)
            html += self.form_add_possible.format(options=options, depths=depths)
        btn = '<form method="post" action="/t3pkonfigurator">\
              <input type="hidden" name="conf_done" value="{0}">\
              <input type="submit" class="btn btn-success" value="Finish">\
              </form>'
        return html + btn.format(depths)

    def build_conf_done(self, conf):
        depthlist_item = '<li>{0}cm</li>'
        depthlist = ''
        for i in conf['depths']:
            depthlist += depthlist_item.format(i)
        partlist_item = '<p>{0} x {1}</p>'
        parts = ''
        for i in conf['parts']:
            parts += partlist_item.format(conf['parts'][i], i)
        html = self.form_conf_done.format(depthlist=depthlist,tube=conf['tube'],
            offset=conf['offset'], config=conf['order'], parts=parts)
        return html

    def build_prepare_submit(self, formdata):
        self.tube = formdata['tube']
        self.offset = formdata['offset']
        self.configuration = formdata['configuration']
        self.summary = formdata['summary']
        return self.submit_form.format(self=self)
