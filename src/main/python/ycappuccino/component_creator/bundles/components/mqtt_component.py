# app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt

from ycappuccino.api.component_creator import IComponentServiceFactory, IMqtt
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import (
    ComponentFactory,
    Requires,
    Validate,
    Invalidate,
    Provides,
)


_logger = logging.getLogger(__name__)


@ComponentFactory("Mqtt")
@Provides(
    specifications=[
        YCappuccino.__name__,
        IMqtt.__name__,
        IComponentServiceFactory.__name__,
    ]
)
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@App(name="ycappuccino.component_creator")
class ComponentMqtt(IMqtt):
    def __init__(self):
        super(IMqtt, self).__init__()
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
