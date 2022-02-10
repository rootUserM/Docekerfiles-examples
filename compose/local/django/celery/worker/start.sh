#!/usr/bin/env bash

set -o errexit
set -o nounset


celery -A cride.taskapp worker -l INFO
