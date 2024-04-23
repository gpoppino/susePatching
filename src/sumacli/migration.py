import logging
from xmlrpc.client import Fault

from sumacli.scheduler import SchedulerFactory, Scheduler


class SystemProductMigrationScheduler(Scheduler):
    def __init__(self, client, system, date, args):
        self.__client = client
        self.__system = system
        self.__date = date
        self.__logger = logging.getLogger(__name__)
        self.__dry_run = args.dry_run

    def schedule(self):
        action_ids = []
        try:
            action_ids.append(self.__client.system.scheduleProductMigration(self.__system.get_id(self.__client),
                                                                            self.__system.target, [], self.__dry_run,
                                                                            self.__date))
            self.__logger.debug(f"Successfully scheduled product migration with action ID {action_ids}")
            if self.__dry_run:
                self.__logger.info(f"Dry run mode: no action taken for system {self.__system.name}")
        except Fault as err:
            self.__logger.error(f"Failed to schedule product migration for system {self.__system.name}")
            self.__logger.error("Fault code: %d" % err.faultCode)
            self.__logger.error("Fault string: %s" % err.faultString)
            return None
        except ValueError as err:
            self.__logger.error(err)
            return None
        return action_ids


class ProductMigrationSchedulerFactory(SchedulerFactory):
    def get_scheduler(self, client, system, schedule_date, args):
        if system.target is None:
            raise ValueError(f"System {system.name} has no migration target")
        scheduler = SystemProductMigrationScheduler(client, system, schedule_date, args)
        return scheduler
