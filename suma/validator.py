import logging
import os
import time
import xmlrpc.client
from datetime import datetime


class ActionIDFileManager:
    def __init__(self, action_id_filename):
        self.__action_ids = []
        self.__logger = logging.getLogger(__name__)
        self.__action_id_filename = action_id_filename
        if action_id_filename is None:
            actions_directory = "actions/"
            if not os.path.exists(actions_directory):
                os.makedirs(actions_directory)
            self.__action_id_filename = (actions_directory +
                                         "action_ids." + datetime.fromtimestamp(time.time()).isoformat())

    def read(self):
        with open(self.__action_id_filename) as f:
            for line in f:
                if line.strip() == '':
                    continue
                self.__action_ids.append(int(line))
        return self.__action_ids

    def append(self, action_id):
        if isinstance(action_id, list):
            for x in action_id:
                self.__action_ids.append(x)
        else:
            self.__action_ids.append(action_id)

    def save(self):
        if not self.__action_ids:
            return False
        with open(self.__action_id_filename, "w") as f:
            data = [str(action_id) + "\n" for action_id in self.__action_ids]
            f.writelines(data)
            self.__logger.debug(f"Action IDs file created: {self.__action_id_filename}")
            return True

    def get_action_ids(self):
        return self.__action_ids

    def get_filename(self):
        return self.__action_id_filename


class ActionIDValidator:
    def __init__(self, client, action_id_file_manager):
        self.__client = client
        self.__action_id_file_manager = action_id_file_manager
        self.__logger = logging.getLogger(__name__)

    def validate(self):
        self.__action_id_file_manager.read()

        found = False
        systems = self.__list_systems(self.__client.schedule.listCompletedSystems)
        if systems:
            self.__logger.info(f"The following systems have completed successfully: {systems}")
            found = True

        systems = self.__list_systems(self.__client.schedule.listFailedSystems)
        if systems:
            self.__logger.error(f"The following systems have failed: {systems}")
            found = True

        systems = self.__list_systems(self.__client.schedule.listInProgressSystems)
        if systems:
            self.__logger.warning(f"The following systems have actions in progress: {systems}")
            found = True

        if not found:
            self.__logger.error(f"Action IDs not found.")

    def __list_systems(self, func):
        action_ids = self.__action_id_file_manager.get_action_ids()
        systems = set()
        for action_id in action_ids:
            s = None
            try:
                s = func(action_id)
            except xmlrpc.client.Fault as err:
                self.__logger.error(f"Fault string: {err.faultString}")
            if s:
                systems.add(s[0]['server_name'])
        return systems
