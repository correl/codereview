#!/bin/bash
CODEREVIEW_PATH=/path/to/codereview

cd $CODEREVIEW_PATH \
    && python manage.py updaterepos $* >/dev/null \
    && python manage.py update_index >/dev/null
