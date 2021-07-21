#!/bin/sh

# Generates a key for the server and client to use

dd if=/dev/urandom of=/dev/stdout bs=32 count=1 status=none | base64