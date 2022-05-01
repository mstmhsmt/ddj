#!/usr/bin/env python3

from .conf import VAR_DIR, FACT_DIR, DD_DIR, LOG_DIR, FB_DIR
from .conf import ONT_DIR, WORK_DIR, REFACT_DIR
from .conf import VIRTUOSO_PW, VIRTUOSO_PORT, DEPENDENCIES_INSTALLER

try:
    from conf import *
    print('local conf imported')
except Exception:
    pass

if __name__ == '__main__':
    print(f'VAR_DIR: {VAR_DIR}')
    print(f'fACT_DIR: {FACT_DIR}')
    print(f'DD_DIR: {DD_DIR}')
    print(f'LOG_DIR: {LOG_DIR}')
    print(f'FB_DIR: {FB_DIR}')
    print(f'ONT_DIR: {ONT_DIR}')
    print(f'WORK_DIR: {WORK_DIR}')
    print(f'REFACT_DIR: {REFACT_DIR}')
    print(f'VIRTUOSO_PW: {VIRTUOSO_PW}')
    print(f'VIRTUOSO_PORT: {VIRTUOSO_PORT}')
    print(f'DEPENDENCIES_INSTALLER: {DEPENDENCIES_INSTALLER}')
