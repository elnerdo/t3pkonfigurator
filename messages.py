#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MessagesDE(object):

    def __init__(self):
        self.initial_message = "Wählen Sie zunächst ihren tiefsten Messpunkt."
        self.add_probe_message = "Fügen Sie, falls benötigt, weitere Messpunkte \
            mithilfe der Dropdown-Auswahl hinzu. Wenn keine weiteren Messpunkte \
            benötigt werden, klicken Sie auf Fertig."
        self.max_elements_message = "Es können keine weiteren Elemente hinzugefügt werden. \
            Schließen Sie die Konfiguration durch einen klick auf Fertig ab oder \
            überarbeiten Sie die Konfiguration."
        self.finish = "Wählen Sie nun Anschluss, Kabellänge und Stückzahl aus \
            und schließen Sie die Konfiguration mit einem Klick auf OK ab.\
            Ein PDF mit ihren Einstellungen wird erstellt, welches Sie uns \
            per Email an info@imko.de senden."


class MessagesEN(object):

    def __init__(self):
        self.initial_message = "Start with choosing your deepest measuring point."
        self.add_probe_message = "If needed add additional measuring points, \
            provided by the dropdown menu. If you dont need further measuring \
            points, click Done."
        self.max_elements_message = "You cannot add further measuring points. \
            Complete the process by clicking Done or review your configuration."
        self.finish = "Now select connector, cablelength and amount and complete \
            the configuration by clicking OK. A PDF with your setup will be \
            created. Send this PDF via email to info@imko.de"
