#!/usr/bin/bash






sudo docker run --publish 8080:9392 -e PASSWORD="porcodio" --volume openvas:/data --name openvas immauss/openvas
