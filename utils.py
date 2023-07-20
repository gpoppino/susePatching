import logging
from xmlrpc.client import Fault


class SystemPackageRefreshScheduler:

    def __init__(self, client, system, date):
        self.__client = client
        self.__system = system
        self.__date = date
        self.__logger = logging.getLogger(__name__)

    def schedule(self):
        action_ids = []
        try:
            action_ids.append(self.__client.system.schedulePackageRefresh(self.__system.get_id(self.__client), self.__date))
            self.__logger.debug(f"Successfully scheduled package refresh with action ID {action_ids}")
        except Fault as err:
            self.__logger.error(f"Failed to schedule package refresh for system {self.__system.name}")
            self.__logger.error("Fault code: %d" % err.faultCode)
            self.__logger.error("Fault string: %s" % err.faultString)
            return None
        return action_ids
