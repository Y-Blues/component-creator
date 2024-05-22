# app="all"
from ycappuccino.api.component_creator import IMail, IComponentServiceFactory
from ycappuccino.api.core import IActivityLogger
from ycappuccino.api.proxy import YCappuccinoRemote
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import (
    ComponentFactory,
    Requires,
    Validate,
    Invalidate,
    Property,
    Provides,
    Instantiate,
    BindField,
    UnbindField,
)


import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

_logger = logging.getLogger(__name__)


@ComponentFactory("Mail")
@Provides(
    specifications=[
        YCappuccinoRemote.__name__,
        IMail.__name__,
        IComponentServiceFactory.__name__,
    ]
)
@Requires("_log", IActivityLogger.__name__, spec_filter="'(name=main)'")
@App(name="ycappuccino.component_creator")
class ComponentMail(IMail):
    def __init__(self):
        super(IMail, self).__init__()
        self._host = None
        self._port = None

    def send(self, a_subject, a_from, a_to, a_mail):

        msg = EmailMessage()
        msg.set_content(a_mail)

        # me == the sender's email address
        # you == the recipient's email address
        msg["Subject"] = a_subject
        msg["From"] = a_from
        msg["To"] = a_to
        # TODO test with TLS etc...
        with smtplib.SMTP("{}:{}".format(self.host, self.port)) as s:
            s.send_message(msg)

    @Validate
    def validate(self, context):
        self._log.info("ComponentMail validating")
        self._log.info("ComponentMail validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentMail invalidating")
        self._log.info("ComponentMail invalidated")
