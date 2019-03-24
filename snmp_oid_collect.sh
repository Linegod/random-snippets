#!/bin/bash
#J.P. Pasnak, CD - 14/02/2014
#This script does a bulkwalk of a snmp table
#and turns the output into a key-value pair, suitable for ingestion into Splunk
COMMUNITY="......."
DIR_PATH="/"
PARSE="table.awk"
HOSTS="host1 host2"
OIDS="ifTable"
for HOST_ID in ${HOSTS}
	do
		mkdir -p ${DIR_PATH}/${HOST_ID}
		for OID in ${OIDS}
			do
				DATE=`date +%Y-%m-%dT%T%:z`;DPATH=`date +%Y%m%d`;STAMP="${DATE} ${HOST_ID} ${OID}"
				snmpbulkwalk -m ALL -v2c -c${COMMUNITY} ${HOST_ID} -OUQs ${OID} | 
				sed 's/\.0//g'|
				sed 's/ = /=/g'|
				xargs echo ${DATE} ${HOST_ID} ${OI}D >> ${DIR_PATH}/${HOST_ID}/${OID}-${DPATH}.log
			done
	done
