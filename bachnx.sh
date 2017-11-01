#!/bin/bash

service postgresql start
cmsInitDB
cmsImporter /contest
cmsAdminWebServer > /dev/null 2>&1 & 
cmsRankingWebServer > /dev/null 2>&1 & 
cmsLogService 0 > /dev/null 2>&1 &
echo 1 | cmsResourceService -a