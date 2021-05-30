#!/usr/bin/env python3

from .conf import VAR_DIR, FACT_DIR, DD_DIR, LOG_DIR, FB_DIR
from .conf import ONT_DIR, WORK_DIR, REFACT_DIR
from .conf import VIRTUOSO_PW, VIRTUOSO_PORT, DEPENDENCIES_INSTALLER

try:
    from conf import *
    print('local conf imported')
except:
    pass
