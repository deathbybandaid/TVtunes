import os
import argparse
import time
import pathlib

from TVtunes import TVtunes_VERSION, TVtunes_OBJ
import TVtunes.exceptions
import TVtunes.config
import TVtunes.logger
import TVtunes.versions
import TVtunes.scheduler
import TVtunes.web
from TVtunes.db import TVtunesdb

ERR_CODE = 1
ERR_CODE_NO_RESTART = 2


def build_args_parser(script_dir):
    """
    Build argument parser for TVtunes.
    """

    parser = argparse.ArgumentParser(description='TVtunes')
    parser.add_argument('-c', '--config', dest='cfg', type=str, default=pathlib.Path(script_dir).joinpath('config.ini'), required=False, help='configuration file to load.')
    parser.add_argument('--setup', dest='setup', type=str, required=False, nargs='?', const=True, default=False, help='Setup Configuration file.')
    parser.add_argument('--iliketobreakthings', dest='iliketobreakthings', type=str, nargs='?', const=True, required=False, default=False, help='Override Config Settings not meant to be overridden.')
    return parser.parse_args()


def run(settings, logger, db, script_dir, TVtunes_web, versions, web, scheduler, deps):
    """
    Create TVtunes and fHDHH_web objects, and run threads.
    """

    tvtunes = TVtunes_OBJ(settings, logger, db, versions, web, scheduler, deps)
    tvtunesweb = TVtunes_web.TVtunes_HTTP_Server(tvtunes)

    versions.sched_init(tvtunes)

    try:

        # Start Flask Thread
        tvtunesweb.start()

        # Perform some actions now that HTTP Server is running
        tvtunes.api.get("/api/startup_tasks")

        # Run Scheduled Jobs thread
        tvtunes.scheduler.run()

        logger.noob("TVtunes and TVtunes_web should now be running and accessible via the web interface at %s" % tvtunes.api.base)
        if settings.dict["logging"]["level"].upper() == "NOOB":
            logger.noob("Set your [logging]level to INFO if you wish to see more logging output.")

        # wait forever
        restart_code = "restart"
        while tvtunes.threads["flask"].is_alive():
            time.sleep(1)

        if restart_code in ["restart"]:
            logger.noob("TVtunes has been signaled to restart.")

        return restart_code

    except KeyboardInterrupt:
        return ERR_CODE_NO_RESTART

    return ERR_CODE


def start(args, script_dir, TVtunes_web, deps):
    """
    Get Configuration for TVtunes and start.
    """

    try:
        settings = TVtunes.config.Config(args, script_dir)
    except TVtunes.exceptions.ConfigurationError as e:
        print(e)
        return ERR_CODE_NO_RESTART

    # Setup Logging
    logger = TVtunes.logger.Logger(settings)
    settings.logger = logger

    logger.noob("Loading TVtunes %s with TVtunes_web %s" % (TVtunes_VERSION, TVtunes_web.TVtunes_web_VERSION))
    logger.info("Importing Core config values from Configuration File: %s" % settings.config_file)

    logger.debug("Logging to File: %s" % os.path.join(settings.internal["paths"]["logs_dir"], '.TVtunes.log'))

    # Continue non-core settings setup
    settings.secondary_setup()

    scheduler = TVtunes.scheduler.Scheduler()

    # Setup Database
    db = TVtunesdb(settings, logger)

    logger.debug("Setting Up shared Web Requests system.")
    web = TVtunes.web.WebReq()

    # Setup Version System
    versions = TVtunes.versions.Versions(settings, TVtunes_web, logger, web, db, scheduler)

    return run(settings, logger, db, script_dir, TVtunes_web, versions, web, scheduler, deps)


def config_setup(args, script_dir, TVtunes_web):
    """
    Setup Config file.
    """

    settings = TVtunes.config.Config(args, script_dir, TVtunes_web)
    settings.setup_user_config()
    return ERR_CODE


def main(script_dir, TVtunes_web, deps):
    """
    TVtunes run script entry point.
    """

    try:
        args = build_args_parser(script_dir)

        if args.setup:
            return config_setup(args, script_dir, TVtunes_web)

        while True:

            returned_code = start(args, script_dir, TVtunes_web, deps)
            if returned_code not in ["restart"]:
                return returned_code

    except KeyboardInterrupt:
        print("\n\nInterrupted")
        return ERR_CODE


if __name__ == '__main__':
    """
    Trigger main function.
    """
    main()
