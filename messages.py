#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessagesDE(object):

    def __init__(self):
        self.initial_message = {
            "msg": "Wählen Sie zunächst ihren tiefsten Messpunkt.",
            "step": "1"}
        self.add_probe_message = {
            "msg": "Fügen Sie, falls benötigt, weitere Messpunkte \
                    mithilfe der Dropdown-Auswahl hinzu. Wenn keine weiteren \
                    Messpunkte benötigt werden, klicken Sie auf Fertig.",
            "step": "2"}
        self.max_elements_message = {
            "msg": "Es können keine weiteren Elemente hinzugefügt werden. \
                    Schließen Sie die Konfiguration durch einen klick auf \
                    Fertig ab oder überarbeiten Sie die Konfiguration.",
            "step": "2"}
        self.finish = {
            "msg": "Wählen Sie nun Anschluss, Kabellänge und Stückzahl aus \
                    und schließen Sie die Konfiguration mit einem Klick auf \
                    OK ab. Ein PDF mit ihren Einstellungen wird erstellt, \
                    welches Sie uns per Email an info@imko.de senden.",
            "step": "3"}


class MessagesEN(object):

    def __init__(self):
        self.initial_message = {
            "msg": "Start with choosing your deepest measuring point.",
            "step": "1"}
        self.add_probe_message = {
            "msg": "If needed add additional measuring points, \
                    provided by the dropdown menu. If you dont need further \
                    measuring points, click Done.",
            "step": "2"}
        self.max_elements_message = {
            "msg": "You cannot add further measuring points. \
                    Complete the process by clicking Done or review your \
                    configuration.",
            "step": "2"}
        self.finish = {
            "msg": "Now select connector, cablelength and amount and complete \
                    the configuration by clicking OK. A PDF with your setup \
                    will be created. Send this PDF via email to info@imko.de",
            "step": "3"}
