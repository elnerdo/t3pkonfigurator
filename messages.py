#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Messages(object):

    def __init__(self):
        self.initial_message = "Wählen Sie zunächst ihren tiefsten Messpunkt."
        self.too_deep_message = "Ihr gewünschter Messpunkt liegt zu tief. \
            Sie benötigen eine Spezialanfertigung. Bitte setzen Sie sich mit \
            uns in Verbindung. LINK"
        self.add_probe_message = "Fügen Sie, falls benötigt, weitere Messpunkte \
            mithilfe der Dropdown-Auswahl hinzu. Wenn keine weiteren Messpunkte \
            benötigt werden, klicken Sie auf Finish."
        self.max_elements_message = "Es können keine weiteren Elemente hinzugefügt werden. \
            Schließen Sie die Konfiguration durch einen klick auf Finish ab oder \
            überarbeiten Sie die Konfiguration."
        self.email_success = "Vielen Dank. Wir werden uns in kürze mit ihnen in \
            Verbindung setzen."
        self.email_error = "Es ist ein Fehler aufgetreten. Bitte wiederholen Sie \
            den Vorgang."
        self.print_or_next = "Sie haben die Möglichkeit ihre Konfiguration zu \
            drucken. Schicken Sie das Konfigurations-PDF an info@imko.de."
