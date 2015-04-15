#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Messages(object):

    def __init__(self):
        self.initial_message = "Wählen Sie zunächst ihren tiefsten Messpunkt."
        self.add_probe_message = "Fügen Sie, falls benötigt, weitere Messpunkte \
            mithilfe der Dropdown-Auswahl hinzu. Wenn keine weiteren Messpunkte \
            benötigt werden, klicken Sie auf Finish."
        self.max_elements_message = "Es können keine weiteren Elemente hinzugefügt werden. \
            Schließen Sie die Konfiguration durch einen klick auf Finish ab oder \
            überarbeiten Sie die Konfiguration."
        self.finish = "Wählen Sie nun Anschluss, Kabellänge und Stückzahl aus \
            und schließen Sie die Konfiguration mit einem Klick auf OK ab."
