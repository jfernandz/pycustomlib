"""
Some docstring
"""

import logging
import os

from .local import Local
from .remote import Remote

logging.basicConfig(
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
    )

logger = logging.getLogger(__package__)

if __name__ == "__main__":
    sys1 = Local()
    print(sys1.free())

    user_name = os.environ.get('UNAME', None)
    user_pwd = os.environ.get("UPASS", None)
    host_ip = os.environ.get("HIP", None)
    logger.info("User: %s, Pass: %s and Host IP: %s", user_name, user_pwd, host_ip)

    if user_name is not None and user_pwd is not None and host_ip is not None:
        sys2 = Remote(ip_addr=host_ip)
        sys2.connect(username=user_name, password=user_pwd)

    if sys2 is not None:
        print(sys2.free())
