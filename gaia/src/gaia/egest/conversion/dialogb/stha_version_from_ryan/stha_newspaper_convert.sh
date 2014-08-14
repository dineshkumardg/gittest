#!/bin/sh
################################################################################
# Gale Group ESS Source Code
#
# Description: A shell script that calls a Perl program that converts data for most DVI Newspapers
#              and Periodicals: 19th Century UK Periodicals and 19th Century Empire (NCUKP/NCUP/NCEP)
#              and Slavery and Anti-Slavery Newspapers and Periodicals (SASN).
# File name:   dvi_newspaper_convert.sh
# Project:     NCUKP/NCUP/NCEP/SAS
# Source Control Path:
# Programmer:  Ryan Cartmill
#
# Input:     An option file, a delivery manifest, and a "split manifest" directory location.
# Output:    One-to-many dialog B files.
# Execution: Run the shell script with required parameters.
#
# Command line: 
# sh dvi_newspaper_convert.sh <option-file> <delivery-manifest | 'only_headnotes' | 'only_spotlight' | 'only_tables'> <split-manifest-location>
#
# Comments:
#     Platform: Unix/Linux
#
# Revision   History
# Date       Programmer        Description
################################################################################
# 04/27/2009 Ryan Cartmill.....New code, based off of ncup_convert.sh. Added code to pass named LOG
#                              file when processing "only_headnotes".
# 10/14/2009 Ryan Cartmill.....Altered split command to make chunks of 250 files, instead of 1000.
# 09/29/2010 Ryan Cartmill.....Added ECON and PPNP to usage message.
# 10/26/2010 Ryan Cartmill.....Added NCEP to usage message.
# 12/07/2010 Ryan Cartmill.....Added 'only_spotlight' to usage message.
# 12/07/2010 Ryan Cartmill.....Added necessary code to support 'only_tables' option for ECON; added LSNR to usage message.
# 09/13/2011 Ryan Cartmill.....Added TDA to usage message.
# 09/14/2011 Ryan Cartmill.....Switched argument order, to place split manifest directory as 2nd argument; allowed for one-to-many manifest
#                              files to be passed in.
# 09/15/2011 Ryan Cartmill.....Implemented code to auto-create Issue Report.
# 09/22/2011 Ryan Cartmill.....Added code to rename delivery manifest after successful completion of conversion.
# 10/06/2011 Ryan Cartmill.....Updated date code to include hours and minutes.
# 12/14/2011 Mark Hefner.......Added STHA to usage message.
################################################################################

prog_path=`dirname $0`
SCRIPT=`basename $0 | cut -d'.' -f1`

echo "prog_path = $prog_path"

# To Do:
# After processing an original delivery manifest, move it to another name (or location?)
# Create a report that lists the following 4 fields of information:
#   .7zip/zip filename (or delivery manifest name?)
#   Output filename
#   Issue XML Filename
#   Issue RN
# Auto-call the prep_and_send_output.sh script?

# If we don't have 3 command line arguments, print message and exit...
if [ $# -lt 3 ]
then

  echo
  echo "**********************************************************************"
  echo "Possible Missing Attributes:"
  echo 
  #echo "sh $0 <option-file> <delivery-manifest | 'only_headnotes' | 'only_spotlight' | 'only_tables'> <split-manifest-location>"
  echo "sh $0 <option-file> <split-manifest-location> <delivery-manifest | 'only_headnotes' | 'only_spotlight' | 'only_tables'> [<delivery-manifest | 'only_headnotes' | 'only_spotlight' | 'only_tables'> ...]"
  echo
  echo "This program converts NCEP, NCUP, SASN, FTIM, ILN, TLS, ECON, PPNP, LSNR, TDA (1986+), STHA XML data to the Gale B format"
  echo
  echo "**********************************************************************"
   
  exit
fi

OPT_FILE=`pwd`/$1
SPLIT_MANIFEST_DIR=`pwd`/$2
shift 2

DATE=`date +%Y%m%d_\%H\%M`
#echo "Date: ${DATE}"

# Read-in/set options from OPT file...
DVI_NAME=`grep 'dvi_name' ${OPT_FILE} | cut -d ':' -f2- | sed 's:^ *::' | tr '[:lower:]' '[:upper:]'`
OUTPUT_DIR=`grep 'output_dir' ${OPT_FILE} | cut -d ':' -f2- | sed 's:^[ 	]*::'`
REPORT_DIR=${OUTPUT_DIR}../reports

if [ ! -d ${REPORT_DIR} ]
then
   echo
   echo "Creating report dir: ${REPORT_DIR}"
   echo
   
   mkdir -p ${REPORT_DIR}
fi

ISSUE_REPORT=${REPORT_DIR}/${DVI_NAME}_${DATE}_issue_report.txt

echo "Delivery Manifest|Output File|Issue RN|Input File" > ${ISSUE_REPORT}


for ARGUMENT in $@
do 
   case ${ARGUMENT} in
   
   only_headnotes|only_spotlight|only_tables)
   
      LOG=${ARGUMENT}_${DATE}.log
   
      perl ${prog_path}/${SCRIPT}.pl ${OPT_FILE} ${ARGUMENT} ${LOG}
   
      ;;
   
   *.[tT][xX][tT])
   
      DELIVERY_MANIFEST=`pwd`/${ARGUMENT}
   
      START_DIR=`pwd`
   
      cd ${SPLIT_MANIFEST_DIR}
   
      # Split the main manifest into multiple 250-line manifests, to make processing easier...
      split -l 250 -d -a 3 ${DELIVERY_MANIFEST} `basename $DELIVERY_MANIFEST | sed 's:\.[^.]*::'`_
   
      cd ${START_DIR}
   
      for SPLIT_MANIFEST in ${SPLIT_MANIFEST_DIR}/*
      do
         #echo Processing $SPLIT_MANIFEST...
         LOG=`basename $SPLIT_MANIFEST`.log
   
         perl ${prog_path}/${SCRIPT}.pl ${OPT_FILE} ${SPLIT_MANIFEST} ${LOG}
   
         if [ $? -eq 0 ]
         then
		    echo
            echo -e "Conversion complete for: ${SPLIT_MANIFEST}!\n"
         else
            echo -e "\n*******************************************************"
            echo    "*** Conversion failure for: ${SPLIT_MANIFEST}!  Exiting..."
            echo -e "*******************************************************\n"
            exit 1
         fi

		 # Create a report that lists the following 4 fields of information:
         #   Delivery manifest name
         #   Output filename
		 #   Issue RN
         #   Issue XML Filename
		 
         OUTPUT_FILE=${OUTPUT_DIR}/`basename $SPLIT_MANIFEST | sed 's:_[xX][mM][lL]::' | sed 's:_[mM][aA][nN][iI][fF][eE][sS][tT]::' | tr '[:lower:]' '[:upper:]'`.02
		 
		 # Get the Issue RNs and Input filenames (minus XML extension)...
		 grep -C1 '^RT  I' ${OUTPUT_FILE} | sed 's:^[A-Z]\{2,3\} \{1,2\}::' | sed 's: ::g' | tr '\n' '|' | sed 's:|--|:~:'g | sed 's:|$:~:' | tr '~' '\n' | cut -d '|' -f1,3 |
		 while read ISSUE
		 do
			echo "`basename ${ARGUMENT}`|`basename ${OUTPUT_FILE}`|${ISSUE}.xml" >> ${ISSUE_REPORT}
		 done
      done

      # Conversion was successful, so rename manifest file to signify that it was processed...
      mv ${DELIVERY_MANIFEST} ${DELIVERY_MANIFEST}_PROCESSED
   
      ;;
   
   *)
       echo -e "\n***Argument not valid:  ${ARGUMENT}\n"
       exit
   
       ;;
   esac
done

echo
echo "Your Issue Report is located here: ${ISSUE_REPORT}"
echo