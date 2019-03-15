import logging
import sys
import datetime
import certstream
import json

# This is an example of a long-running service/process which will monitor for
# CT Logs in real-time and as soon as a certificat_update action is triggered
# for a domain pattern we care about, we will immediately take action to task
# those scans via our public REST API endpoints

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_callback(message, context):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        domain_patterns = [
            ".mozilla.com",
            ".mozilla.org",
            ".firefox.com",
            ".com",  # for testing purposes only, remove before setting live
        ]

        for fqdn in all_domains:
            for domain_pattern in domain_patterns:
                # We want all legit FDQNs, but we can't scan wild-cards
                if fqdn.endswith(domain_pattern) and ('*' not in fqdn):
                    # TODO: add relevant tasking call here to /ondemand/portscan, /ondemand/observatory, etc.
                    logger.info("Triggered a vulnerability scan of: {}".format(fqdn))


logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')