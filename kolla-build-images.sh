#!/bin/bash

# SPDX-License-Identifier: MIT

DISTRO=debian
TYPE=source
BUILD=
NAMESPACE=haerwu

if [ -n "$1" ]; then DISTRO=$1;fi
if [ -n "$2" ]; then TYPE=$2;fi
if [ -n "$3" ]; then BUILD=$3;fi
if [ -n "$4" ]; then NAMESPACE=$4;fi


echo "Build setup:"
echo "  - distros:    $DISTRO"
echo "  - build type: $TYPE"
echo "  - building:   $BUILD"
echo "  - namespace:  $NAMESPACE"
echo ""


for distro in $DISTRO
do
	for btype in $TYPE
	do
		LOGS=logs/$distro-$btype-$NAMESPACE
		mkdir -p $LOGS

		./tools/build.py --base $distro \
				 --format none \
				 --logs-dir $LOGS \
				 --pull \
				 --format none \
				 --retries 0 \
				 --type $btype \
				 --namespace $NAMESPACE \
				 $BUILD
	done
done
