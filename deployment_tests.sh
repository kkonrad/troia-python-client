#!/bin/bash
PROJECT=../troia_server/Troia-Server/troia-server
TOMCAT=/var/lib/tomcat6
for i in {1..500}
do
    sudo service tomcat6 stop
    sudo rm -rf $TOMCAT/webapps/troia-server-1.0*
    sudo cp $PROJECT/target/*.war $TOMCAT/webapps/
    sudo service tomcat6 start
    python load_sample_job.py
done
