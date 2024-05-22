# app="all"


from ycappuccino.api.component_creator import IComponentServiceList
from ycappuccino.api.core import IActivityLogger
from ycappuccino.api.endpoints import IRightManager
from ycappuccino.api.proxy import YCappuccinoRemote
from ycappuccino.api.storage import ITrigger
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import (
    ComponentFactory,
    Requires,
    Validate,
    Invalidate,
    Provides,
    Instantiate,
)


_logger = logging.getLogger(__name__)


@ComponentFactory("ComponentServiceTrigger-Factory")
@Provides(specifications=[YCappuccinoRemote.__name__, ITrigger.__name__])
@Requires("_log", IActivityLogger.__name__, spec_filter="'(name=main)'")
@Requires("_component_services_list", IComponentServiceList.__name__)
@Requires("_jwt", IRightManager.__name__)
@Instantiate("ComponentServiceTrigger")
@App(name="ycappuccino.component_creator")
class ComponentServiceTrigger(ITrigger):
    def __init__(self):
        super(ComponentServiceTrigger, self).__init__(
            "ComponentServiceTrigger",
            "component",
            ["upsert", "delete"],
            a_synchronous=True,
            a_post=True,
        )
        self._component_services = {}
        self._component_services_list = None

    def execute(self, a_action, a_component_service):
        w_factory_id = a_component_service.get_factory_id()
        w_name = a_component_service.get_name()

        w_active = False

        if a_action == "post" or a_action == "put":
            w_active = a_component_service.get_active()
        elif a_action == "get":
            return a_component_service
        if w_factory_id is not None:
            if w_name in self._component_services.keys():
                # TDOO detroy
                w_component = self._component_services_list.delete_component(
                    a_component_service
                )
                del self._component_services[w_name]
            if w_active:
                w_component = self._component_services_list.create_component(
                    a_component_service
                )
                self._component_services[w_name] = w_component
            return a_component_service

    @Validate
    def validate(self, context):
        self._log.info("ComponentServiceTrigger validating")

        self._log.info("ComponentServiceTrigger validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentServiceTrigger invalidating")

        self._log.info("ComponentServiceTrigger invalidated")
