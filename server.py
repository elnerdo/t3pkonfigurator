#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, time
import logging
import tornado.ioloop
import tornado.web
import tornado.options
from t3pkonfigurator import MainHandler

__version__ = '0.1.0'

if __name__ == "__main__":

    settings = {
        "debug": True,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "."),
        "static_url_prefix": "/t3pkonfigurator/static/",
    }

    application = tornado.web.Application([
        (r"/t3pkonfigurator/de", MainHandler, dict(lang="de")),
        (r"/t3pkonfigurator/en", MainHandler, dict(lang="en"))
    ], **settings)

    tornado.options.parse_command_line()
    logging.info("Starting Server at: http://127.0.0.1:80/t3pkonfigurator/de")
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
