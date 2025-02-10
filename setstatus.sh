#!/bin/bash
  # perl-rename "s/_[a-z]_/_$2_/" $1
  pa=$1
  pp=${1/_[a-z]_/_$2_}
  if [ $1 != $pp ]; then
  mv $1 $pp

    fi
  echo $pp
