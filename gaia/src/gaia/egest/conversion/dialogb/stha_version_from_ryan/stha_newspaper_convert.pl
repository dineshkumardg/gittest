#!/usr/bin/perl
# ------------------------------------------------------------------------------
# Gale Group ESS Source Code
# Description: A program that reads in DVI Newspaper & Periodical XML Issue files, and outputs the data in Dialog B format.
# File name: dvi_newspaper_convert.pl
# Project: NCUKP/NCUP/NCEP/SASN
# Source Control Path:
# Programmer: Ryan Cartmill
#
# Input: 1) An OPT file (containing path information), 2) a manifest file, containing XML files to
#        be processed and 3) an optional log filename.
# Output: A Format B file, named after the manifest file, but with a ".02" extension, containing Issue, Page,
#         Article, MARC and MATP records.
#
# Shell script/batch: None
# Execution:
#    Command line: perl dvi_newspaper_convert.pl <OPT-file> <manifest-of-XML-files> [<log-file>]
#
# Comments:
#    Perl Version: 5.8.8
#
#    Products Supported: NCUP, SASN, FTIM, ILN, TLS, ECON, PPNP, LSNR, TDA (1986+) and STHA
#
# ClearQuest Request Number: None
#
################################################################################
# Revision History
# ==============================================================================
# Date	      Programmer          Description
# ==============================================================================
# 04/20/2006  Ryan Cartmill.......New code, based off London Times, as well as ECCO, SABC, SUPC, etc.
#
# 05/17/2006  Mark Hefner.........Removed the CY and CP tags from the article and issue (CY)
#                                 and from the article, issue, and page records (CP).
#                                 Added the IN tag to the article, issue and page records and
#                                 updated the PI tag in the article and page records to omit
#                                 the associated text and punctuation when <pa> or <is> is not
#                                 present, per updated spec.
#
# 05/18/2006  Mark Hefner.........Added $nak and $syn around < and > in the subroutine
#                                 create_AIF_PIF.  Also changed the assignment of the CI tag
#                                 (Clipped Article Image), it now goes through a while loop
#                                 to call the prep_XML subroutine to put in the nak and syn
#                                 characters around < and >.
#
# 06/01/2006  Ryan Cartmill.......Fixed Trailer record, so it contains correct line counts and record counts.
#                                 Commented out FL tag from MARC records (temporarily).
# 06/02/2006  Ryan Cartmill.......Reinstated the FL tag in the MARC Metadata records.
# 06/26/2006  Ryan Cartmill.......Fixed issue so that '/>' of '<pg ...' is now output; <p> and </p> tags are
#                                 now being properly output around clip rectangle text; NAK and SYN are now
#                                 being properly placed around "inserted" <p>...</p> tags (when para is >
#                                 8000 characters); updated sub create_AIF_PIF to call sub prep_XML, to
#                                 standardize code.
# 06/27/2006  Ryan Cartmill.......Moved sub ftp_files call so it's *after* sub load_opt call, so that all opt
#                                 parameters are processed; altered sub ftp_files, so it now will properly
#                                 get all the headnote files; changed use autouse statement, so that the
#                                 vmsopen function is called only when needed (i.e. only on VMS, not Unix);
#                                 added code for when batch processing is disabled -- all output goes into a
#                                 single NCNP_MMDD.02 file.
# 06/29/2006  Ryan Cartmill.......Moved location of sub prep_XML and sub clean calls to sub make_B_format.
#                                 Only TX, << and >> Format B tags aren't passed through these calls (TX data
#                                 is cleaned and prepped earlier). Now, all fields are being cleaned and
#                                 prepped properly.
# 06/30/2006  Ryan Cartmill.......Split sub prep_XML into sub prep_XML_tags() and sub prep_XML_entities();
#                                 now, not passing AIF, CI and PIF through sub prep_XML_tags, to be "in
#                                 synch" with LTO/TDA processing; Updated code to not output MATP more than
#                                 one time (flag is "turned off" when MATP is first output); created new sub
#                                 add_tag_namespace(), that can be called for AIF, CI and PIF, and is also
#                                 automatically called by sub prep_XML_tags(); Added code to email if there
#                                 are any LCCNs missing from the ncnp_lookup.txt file.
# 07/20/2006  Ryan Cartmill.......Updated Article record with JJ, PC, PS and ST tags; Changed code to accept
#                                 an input manifest file, and process the XML files listed inside that
#                                 manifest file; slightly changed code to output MARC records.
# 07/21/2006  Ryan Cartmill.......Uncommented code that prints to log file.
# 08/11/2006  Ryan Cartmill.......Updated program to accept both PSM-formatted manifest files, or OCM-created
#                                 manifest files (with .xml extension); Added ZI tag to all records (except
#                                 MATP); Added (commented) code to truncate article titles at 150 characters,
#                                 for both TI and AIF tag contents.
# 08/21/2006  Ryan Cartmill.......Updated code to fix issue where entities were being "double escaped" during
#                                 conversion.
# 08/23/2006  Ryan Cartmill.......Added TE tag to Page, Article, and Issue records; implemented code to
#                                 truncate article titles at 375 characters, plus added ellipsis (affects TI
#                                 and AIF contents); now removing period from PD tag (MARC record); added
#                                 code to convert all entities with an ASCII value of 160-255 to their actual
#                                 characters, so that the data will be similar to LTO/TDA (allows users to
#                                 type the actual characters in when entering search terms); removed
#                                 decode_entities call, and HTML::Entities module; removed enable/disable
#                                 switches for batch-processing, as program is now driven by what's in the
#                                 manifest file.
# 09/13/2006  Ryan Cartmill.......Removed 'use Date::Calc;' and the %day and %mth hashes, as they're not
#                                 needed for NCNP.
# 09/22/2006  Ryan Cartmill.......Added code to allow for processing of only headnotes, using command-line
#                                 option 'only_headnotes' in lieu of a manifest filename; fixed bug where
#                                 <headnote> and </headnote> tags weren't being escaped with NAK/SYN.
# 10/01/2007  Ryan Cartmill.......Updated code to fix output issue pertaining to multi-page articles.
# 10/02/2007  Ryan Cartmill.......Updated code to read $dvi_name from OPT file, rather than OPT filename, 
#                                 which was proving problematic when using fullpath to OPT file.
# 10/03/2007  Ryan Cartmill.......Shifted code around to properly set $dvi_name before setting $bncn/$bbcn/etc.
#                                 flags.
# 10/16/2007  Ryan Cartmill.......Updated code to comment out $matp_hash{ID}; updated code to only remove
#                                 *leading* zeros from page numbers in sub create_AIF_PIF; updated code to
#                                 only move input files to completed dir when on VMS; updated code to only
#                                 print messages to STDERR when on VMS.
# 10/31/2007  Ryan Cartmill.......Updated code to handle continuation pages (including AIF, PI, PID and RN);
#                                 changed code that creates $issue_hash{PI}, so it's built again, instead of
#                                 using the $article_hash{PI} (which was sometimes blank when needed);
#                                 changed BNCNPageIDList to just PageIDList, so it's more generic; added sub
#                                 to read in and store the PageIDList (for quick referencing) instead of opening
#                                 and closing the file each time.
# 11/01/2007  Ryan Cartmill.......Added code to clear out @aif_multiple between files (was causing code to loop);
#                                 added additional checks to make sure $prev_page_number isn't > $article_hash{PID}.
# 09/30/2008  Cholan Photon.......Added code to auther name composed and reversed by using <detailed_au> tag.
#								  Also have been changed article start page number provided PI tag.
# 11/11/2008  Cholan Photon.......Added code to checking empty pages by using <page> tag.
#								  Also have been changed correct page number in PI content.
# 04/27/2009 Ryan Cartmill........Updated code, to handle Slavery and Antislavery Newspapers.  Removed code that adds ".opt" to first argument;
#                                 Updated UZ value from NCUP to SASN; Updated RN values for Page and MARC Metadata Records.
# 06/15/2009 Ryan Cartmill........Updated code to ignore field names from sap_lookup.txt file.
#
# 09/30/2009 Ryan Cartmill........Merged code from ncup_convert.pl and sasn_convert.pl into this new program, dvi_newspaper_convert.pl.
#                                 Values that differ (like RN prefixes and UZ values) are set via the use of the dvi_name variable, which is
#                                 present in each unique, passed-in OPT file.
# 09/30/2009 Ryan Cartmill........UNcommented code to populate $article_hash{PA} -- not sure why this was commented out in the first place.
#                                 UNcommented code to populate $article_hash{PG} -- not sure why this was commented out in the first place.
#                                 Added code specific to FTIM.
# 10/01/2009 Ryan Cartmill........Updated code to allow attributes on <article> paragraphs.  Fixed a NASTY bug, where an if statement was
#                                 searching
# 11/06/2009 Ryan Cartmill........Updated code (specific to Financial Times) to transform UTF-8 to ISO-Latin; output "Edition" instead of "Issue"
#                                 in PI; and output <da> value to DA, for Issue, Page, and Article records.
# 11/19/2009 Ryan Cartmill........Updated code to split by <page>, then by </article>, in order to properly assign <pa> values to necessary
#                                 Format B tags (PA, PG, PI, PIF).
# 12/11/2009 Ryan Cartmill........Updated code for ILN (Illustrated London News), per specs.  Still have outstanding questions on 1) input filename
#                                 pattern and 2) $marc_hash{RN}.  Also assuming files using UTF-8 encoding.  Will need to testing whether using
#                                 utf8::valid and/or utf8::is_utf8 functions will increase conversion speed.
# 12/30/2009 Ryan Cartmill........Updated code to switch output of SH and UZ tags in Page records, to prevent tag segmentation when a
#                                 backwards page continuation occurs.
# 03/16/2010 Ryan Cartmill........Added code to output page 1 records that don't contain article content.
# mm/dd/yyyy Joe Programmer.......Description of Change.
#
# 03/25/2010 Ryan Cartmill........Updated code to read page ID from page records, instead of from article <pi> tags; Updated
#                                 code to store TS information for all necessary page records (using <pi> for reference);
#                                 added code to sub continuation_page_backwards to add missing TS information to page recs
#                                 that were already output.  Result is a better, more-reliable conversion, that is 9x faster
#                                 than before.
# 04/09/2010 Ryan Cartmill........Added code to prevent output of SC tag for TLS records.
# 04/12/2010 Ryan Cartmill........Altered code to output <placepub> to PW tag, instead of PR tag.
# 04/13/2010 Ryan Cartmill........Updated code to: 1) open output files as ISO-8859-1, 2) open input files as regular, non-UTF-8 files, 3) add AE tag
#                                 to appropriate page and article records and 4) NOT output LB tag to TLS records.
# 04/14/2010 Ryan Cartmill........Updated code to NOT output LB tag to TLS records for ALL record types.
# 04/20/2010 Ryan Cartmill........Updated code that outputs FW tag, to: 1) only output <nwtitle> value when <nwauthor> is not present and 2) Not output FW
#                                 when <nwtitle> is not present.
# 04/21/2010 Ryan Cartmill........Updated code to dedupe contributor names (authors, editors, illustrators and translators).
# 04/30/2010 Ryan Cartmill........Updated code to limit OI tag output to ILN conversions only; Added code to create page records for pages missing at the
#                                 end of an issue, by examining $issue_hash{IP};
# 09/10/2010 Ryan Cartmill........Added code to prevent output of AS, IC and OI tags in FTIM, and code to prevent output of AE, TB and TS tags in FTIM Page
#                                 content.  Basically, conversions for FTIM, ILN and TLS are now merged into one massive program.
# 09/13/2010 Ryan Cartmill........Updated code per ECON spec, and added ECON rules for encoding of output file, reopen of output file, and parsing of
#                                 filename (to grab year, month and day).  Also updated code to be a little tighter, in terms of rules for FTIM, ILN and
#                                 TLS.
# 09/14/2010 Ryan Cartmill........Fixed a couple mistakes in the code that were causing errors.  Added extra space after '<<' line (it was missing).
# 09/29/2010 Ryan Cartmill........Updated code (without specs!) for PPNP (Picture Post) conversion -- PPNP was modelled after ILN, except that the input
#                                 data isn't truly in UTF-8.  Added code to support new metadata file structure (with 27 columns instead of 32) -- code now
#                                 counts number of metadata fields, and acts accordingly.  Updated Issue record RN prefix to "04", per Kathy.
# 10/07/2010 Ryan Cartmill........Updated code/logic for AE, TS and TB.  Added new code/logic for SI. Added "failover" code
#                                 for AE population, so that older-format ILN records still get AE populated properly.
# 10/20/2010 Ryan Cartmill........Updated code for TLS, to save article's AE value for later output in page record.
# 10/28/2010 Ryan Cartmill........Updated code to remove faulty "my" occurrences from read_metadata_file subroutine, that
#                                 was preventing assignment of $source_library, which was preventing output of LB tag.
# 11/30/2010 Ryan Cartmill........Updated code for PPNP, to prevent output of NE tag (per specs).
# 12/07/2010 Ryan Cartmill........Updated code to handle a new Spotlight record; updated read_metadata subroutine to accommodate new values in lookup file;
#                                 updated load_opts subroutine to read in optional spotlight_file parameter.
# 12/13/2010 Ryan Cartmill........Update code for spotlight record, to place open and close wrapper element in their own RM
#                                 element, and to put each spotlight entry in its own RM tag (at request of CIM and DA).
# 12/20/2010 Ryan Cartmill........Updated code to create XT tag when <calsTableInfo> tag is encountered.  Added code to handle Excel dates prior to
#                                 1/1/1901.  Updated code for Listener (LSNR) too.
# 01/24/2011 Ryan Cartmill........Updated code to check for length of current TX content + new TX content *before* combining them together. This should fix
#                                 tag overruns.
# 01/27/2011 Ryan Cartmill........Updated code to handle output of Table Records (for Economist).
# 01/28/2011 Ryan Cartmill........Added code for tables, to remove pos attribute, add border, and cleanup TID output.
# 02/02/2011 Ryan Cartmill........Fixed a comment line.
# 03/10/2011 Ryan Cartmill........Remapped some high-end hexadecimal entities that the LSNR application can't handle.
# 05/25/2011 Ryan Cartmill........Added code to help diagnose metadata file problem (with too many columns).
# 06/06/2011 Ryan Cartmill........Updated code to read in marc_rn from metadata file for newer DVI Newspaper products.
# 09/13/2011 Ryan Cartmill........Added in code for LSNR high-end replacement characters.  Began coding for TDA 1986+ data. Updated code for following source tags, to be
#                                 more XML-compliant: <il>, <ocr>, <pi> and <wd>.
# 09/14/2011 Ryan Cartmill........Added code for <au_composed> (goes to AU tag); added code to strip S# occurrences from <pa>...</pa>; upgraded <pg>...</pg> code to
#                                 attributes to appear in any order.
# 09/15/2011 Ryan Cartmill........Commented-out code to remove S# occurrences from <pa>...</pa>.
# 10/05/2011 Ryan Cartmill........Updated code to fix bug with <LTO.pg> output in <LTO.text.cr> sections.
# 10/06/2011 Ryan Cartmill........Updated code to remove leading zeros from AIF tag's XXRN="..." value (to resolve
#                                 application error).
# 12/14/2011 Mark Hefner..........Updated code to process the STHA (Sunday Times) newspaper. The record prefixes and base
#                                 numbers changed from 2 and 8 digits to 5 and 5 digits.  Search for
#                                 "first_article_rn_base" for STHA code change.
# 03/02/2012 Mark Hefner..........Updated code to process the STHA (Sunday Times) newspaper issue record numbers.
#                                 The record numbers for STHA are now the record prefix "04002" plus a 5 digit
#                                 counter starting with 00001.  The issue record numbers are now kept in a pipe-delimited
#                                 control file that has the isssue id as the key and the issue number as the value.
#                                 Here is an example line:  STHA-1822-1020|0400200001
#                                 This change made for Altiris Request #289931.
################################################################################
# To Do:
#
# - Do dummy (page) records need to be created, like in London Times?
#


use Cwd;
use Net::FTP;
use File::Copy;
use File::Basename;
use Data::Dumper;
#use VMS::Stdio qw(:FUNCTIONS);
#use autouse 'VMS::Stdio' => qw(vmsopen);
#use vmsish;
use Spreadsheet::ParseExcel;
use Spreadsheet::ParseExcel::Utility qw(ExcelFmt ExcelLocaltime);

# SET UP MAIN VARIABLES
####################
# Characters that are wrapped around every XML tag and every entity...
my $nak = "\x15";
my $syn = "\x16";

#General:
my $file_no = 1;
my $first_article_found = 0;
my $hard_ret = '';
my $linecount = 0;
my $namespace = 'LTO';
my $output_count = 0;
my $page_rn_base = 0;
my $platform = '';
my $prev_page_number = 0;
my $read_count = 0;
my $recnum = '';
my $record_for_marc = '';
my $send_mail = 0;
my $start = '$$';
my $write_count = 0;
my $dvi_name;
my @aif_multiple = ();
my @get_pa = ();
my %hash_pid_pa = ();
my $spotlight_file;
my $table_dir;
my @table_files = ();

my $pPG;
my @AIF_array = ();
my %AE_hash = ();
my %SI_hash = ();
my %TB_hash = ();
my %TS_hash = ();
#my %TS_written_hash = ();
my @temp_PA = ();
my $author_count=0;

my %mcode_hash = ();
my %missing_lccn = ();
my %new_id = ();

my @text_cr       = ();
my @text_preamble = ();
my @text_title    = ();
my %pi_pgref_hash = ();
my @ocr_values    = ();
my %page_id_hash  = ();
my %table_id_hash = ();

####################
%issue_hash     = ();
%page_hash      = ();
%article_hash   = ();
%matp_hash      = ();
%marc_hash      = ();
%spotlight_hash = ();
%table_hash     = ();
%xml_mcode      = ();


######## New Variables for the DVI issue number assignment, starting with the STHA project ########
my $DVI_last_issue_num         = sprintf("%05d", (0));
my $DVI_last_issue_num_new     = sprintf("%05d", (0));
my $DVI_last_issue_num_saved   = sprintf("%05d", (0));
my $DVI_issue_num_ctr          = 0;
my $DVI_issue_new_num_ctr      = 0;
my $DVI_issue_existing_num_ctr = 0;

my %DVI_issue_num_hash         = ();




# Populating this array with Roman Numerals; values 1-50 (I - L)...
my @roman_array = ('i','ii','iii','iv','v','vi','vii','viii','ix','x',
                'xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx',
                'xxi','xxii','xxiii','xxiv','xxv','xxvi','xxvii','xxviii','xxix','xxx',
                'xxxi','xxxii','xxxiii','xxxiv','xxxv','xxxvi','xxxvii','xxxviii','xxxix','xl',
	        'xli','xlii','xliii','xliv','xlv','xlvi','xlvii','xlviii','xlix','l');

my %roman_hash = ();

# Populate the hash with the array cell content as a key, and the array index
# as the value...
for (my $j=0; $j<scalar(@roman_array); $j++)
{
    $roman_hash{$roman_array[$j]}=$j;
}

# Determine the current Operating System/Platform
if ($^O eq 'VMS')
{
  $platform = 'VMS';
}
else
{
  $platform = 'Unix';
}

if ($platform eq 'Unix')
{
   $hard_ret = "\n";
}
elsif ($platform eq 'VMS')
{
   $hard_ret = '';
}

# Get the current date information...
&get_date();

  
### Check the command line parameters, to make sure they're correct

&program_setup();


mprint ("Operating System:    $platform");


# Setup/Open the Regular Output files...
if ($platform eq "Unix")
{
   fileparse_set_fstype("MSDOS");
}
elsif ($platform eq "VMS")
{
   fileparse_set_fstype("VMS");
}


# Setup display:
#mprint("\n");
#
#mprint ('Records Read   Records Written   Current File');
#mprint ('------------   ---------------   ------------');


########################
# Main processing loop #
########################
(my $fname, my $dir, my $type) = fileparse("\U$manifest_file",'\..*');
$fname =~s:_manifest::i;
$fname =~s:_xml::i;
my $output_file = $output_dir.$fname.'.02';

if ($platform eq "Unix")
{
   if ($dvi_name eq 'FTIM' || $dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
   {
      open($NCNPOUT, '+>:encoding(ISO-8859-1)', $output_file) || die "\n\nError opening output file $output_file: $!.\n\n";
   }
   else
   {
	  open($NCNPOUT,"+>$output_file") || die "\n\nError opening output file $output_file: $!.\n\n";
   }
}
elsif ($platform eq "VMS")
{
   $NCNPOUT = vmsopen(">$output_file","rfm=fix","mrs=80") or die "*** can't open output b-file";
}

mprint("\nOpened output file: $output_file");

&write_header_rec();


while (my $input_file = shift(@inputfiles))
{
   %pgnum_hash=@pgnum_array=@pgnum_counted=%page_id = ();
   @AIF_array = ();
   @aif_multiple = ();

   # Open input XML file...
   if ($dvi_name eq 'FTIM' || $dvi_name eq 'ILN')
   {
      open(NCNPIN,'<:utf8', $input_file) || die "\nError opening input file $input_file: $!.\n";
   }
   else
   {
      open(NCNPIN,"<$input_file") || die "\nError opening input file $input_file: $!.\n";
   }

   mprint("\nOpened input file: $input_file");
   
   # Grab the current month and day from the input filename...
   (my $curr_year, my $curr_month, my $curr_day) = $input_file =~ /\w{4}-(\d{4})-(\w{3})(\d{2})/i;
   (my $curr_year, my $curr_month, my $curr_day) = $input_file =~ /\w{4}-(\d{4})-(\d{2})(\d{2})/i if ($dvi_name eq "FTIM" || $dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA');

   mprint (sprintf("Processing issue %s%02d%s%4d",$curr_month.' ',$curr_day,', ',$curr_year));

   $record=$record_for_marc = '';
   $true_page_id=$true_page_num = '';
   local $/ = '<page>';
   
   while (local $page=<NCNPIN>)
   {
      ($true_page_id) = $page=~m:<pageid[^>]*>(.*?)</pageid>:;
      ($true_page_num) = $true_page_id =~m:.*-(\d+)$:;


      # Store all non-empty AE, SI, TS and TB values for later use in Page and Article records...
      if ($dvi_name eq 'ILN' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
      {
         # Article Series Title
         if ((my $temp_AE) = $page =~m:<pageid.*pageType\s*=\s*"([^"]*)":)
         {
            $AE_hash{$true_page_id} = $temp_AE;
         }
         elsif ((my $temp_AE) = $page =~m:<sectiontype>(.*?)</sectiontype>:)
         {
            $AE_hash{$true_page_id} = $temp_AE;
         }

         # Supplement/Special Issue Indicator
         if ((my $temp_SI) = $page =~m:<pageid.*isPartOf\s*=\s*"([^"]*)":)
         {
            $SI_hash{$true_page_id} = $temp_SI;
         }

         # Supplement Title
         if ((my $temp_TS) = $page =~m:<supptitle>(.*?)</supptitle>:)
         {
	      $TS_hash{$true_page_id} = $temp_TS;
         }

         # Supplement Subtitle
         if ((my $temp_TB) = $page =~m:<suppsubtitle>(.*?)</suppsubtitle>:)
         {
            $TB_hash{$true_page_id} = $temp_TB;
         }
      }

      #print STDERR "4: The AE_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_hash ), "\n";
      #print STDERR "4: The SI_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_hash ), "\n";
      #print STDERR "4: The TS_hash contents are as follows: ", Data::Dumper::Dumper( \%TS_hash ), "\n";
      #print STDERR "4: The TS_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TS_written_hash ), "\n";
      #print STDERR "4: The TB_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_hash ), "\n";




#   local $/ = '<article';
   #print "PAGE: +++$page---\n";
#   while ($record=<NCNPIN>)
   foreach $record (split(/<\/article>/, $page))
   {

     #print "REC: +++$record---\n";
     
	 ## Updated by photon 11-11-2008 [dd-mm-yyyy]
	 (@get_pa) = $record =~ m:<pageid[^>]*>(.*?)(</pa>|</page>):sgi;
	 foreach my $get_pa (@get_pa) {
		if($get_pa =~ /<pa>/i){
			$get_pa =~ s/\n+//gi;
			$get_pa =~ s/\s*|\t*|<\/pageid>//gi;
			#$get_pa =~ s/\[|\]//gi;
			(my $key, my $value) = $get_pa =~ m:^(.*)<pa>(.*):i;
			
			# Cleanup "supplement" values from PA (page label) value...
			# Globally remove S and any digits that immediately follow...
			# BEFORE
            # <pa>1</pa>
            # <pa>1S</pa>
            # <pa>1S1</pa>
            # <pa>1S2 – 2S2</pa>

            # AFTER
            # <pa>1</pa>
            # <pa>1</pa>
            # <pa>1</pa>
            # <pa>1-2</pa>

			#$value =~s:S\d*::g;
			
			$hash_pid_pa{$key} = $value;
			#print STDERR "KEY: $key\nVALUE: $value\n";
		}
	 }
	 @get_pa = ();

	  if ($record =~m:<issue>:s)
      {
         #######################################################################
         # MAH 05/12/06, added $record_for_marc because the record separator   #
         # is set to <article> by the time the create_marc_record subroutine   #
         # is called.                                                          #
         #######################################################################
         $record_for_marc = $record;
         $record_for_page = $record;
         @ocr_values = ();
         &read_issue_record();
         $first_article_found = 0;
         $prev_page_number = 0;
         next;
      }
      elsif ($record =~m:</page>:)
      {
         #print "SKIP REC: +++$record---\n";
         next;
      }
      elsif(length($record)>5)
      {
		 &read_article_record();
         $read_count++;
         &add_format_b_tags('article_hash');
         &write_article_record();
         %article_hash = ();
      }

      # Create, populate and output the MARC Metadata record if we're processing the correct file...
      
#      if ( exists ($mcode_hash{$issue_hash{BA}}{ZJ}{$issue_hash{ZJ}}) && exists ($marc_hash{RN}) &&
 #         ($input_file =~m:$mcode_hash{$issue_hash{BA}}{ZJ}{$issue_hash{ZJ}}{XML_FILE}:) )
       if ( exists ($mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}) && exists ($marc_hash{RN}) &&
            ($input_file =~m:$mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}{XML_FILE}:) )
      {

         mprint ("Creating MARC record...");
         &create_marc_record();
         &add_format_b_tags('marc_hash');
         &write_marc_record();
         %marc_hash = ();
      }
      elsif (! exists ($mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}) )
      {
         $missing_lccn{$issue_hash{ID_dummy}} = "\n*** MISSING LCCN from ncnp_lookup.txt: MCODE=$issue_hash{BA}," .
                                          " LCCN=$issue_hash{ID}\n";
      }

      # Suppressed output to the screen to increase NCNP conversion speed
      #mprint(sprintf("\n   %9d         %9d   %s                 ",$read_count,$write_count,$input_file));
   }#foreach $record (split/<\/article>/, $page)

   }# while (my $page=<NCNPIN>)
   
   # Write out any remaining page record(s) in the issue, up to (but not including) the last page record...
   # Separate the ID from the page number...
   (my $prev_id, my $prev_num) = $prev_page_number =~m:^(.*)-(\d+)$:;

   # Using the $issue_hash{IP}, create the largest PID, in case there are multiple page records yet to be output...
   $article_hash{PID} = $prev_id ."-".sprintf("%04d", $issue_hash{IP});

   my $prev_num = 0;
   if ($prev_page_number)
   {
      ($prev_num) = $prev_page_number =~m:.*-(\d+)$:;
   }

#   (my $article_num) = $article_hash{PID} =~m:.*-(\d+)$:;
   my $article_num = $true_page_num;

   #mprint ("prev_num: $prev_num\narticle_num: $article_num\n");
   #print STDERR "^prev_num: $prev_num\narticle_num: $article_num\n\n";

   if ($prev_num > $article_num)
   {
      mprint ("***I. Non-sequential page ID encountered: prev_PID=$prev_page_number, curr_PID=$article_hash{PID} ***\n");
   }
   # Updated by photon 12-11-2008 [dd-mm-yyyy]
   my $get_temp_pi = $page_hash{PI};

#   while ($prev_page_number ne $article_hash{PID} && $prev_num <= $article_num)
   # Added code to create page records for pages missing at the end of an issue, by examining $issue_hash{IP}...
   while (($prev_page_number ne $true_page_id && $prev_num <= $article_num) || $prev_num < $issue_hash{IP})
   {
#		print STDERR "\n article hash:$article_hash{PID} and prev page number:$prev_page_number and prev_num is $prev_num and article num is $article_num";
#      print STDERR "\n?article_num:$true_page_id and prev page number:$prev_page_number" .
#                   "\n?prev_num is $prev_num and article num is $article_num" .
#                   "\n?prev_num is $prev_num and IP value is $issue_hash{IP}\n";
#      my $curr_page_number = $article_hash{PID};
      my $curr_page_number = $true_page_id;

      # Write out a page record if the page number changes, but only if it's not the first page...
      if ($prev_page_number)
      {
         # Populate the AE, SI, TS and TB tags from the stored values at the page-level, if present...
         # Need to know current page (use $prev_num or $curr_num)
         # Delete value from hash once done

         #print STDERR "1: The AE_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_hash ), "\n";

         if (exists($AE_hash{$prev_page_number}))# && !(exists($AE_written_hash{$prev_page_number})))
         {
            ($page_hash{AE}) = $AE_hash{$prev_page_number};
            delete $AE_hash{$prev_page_number};
#            $AE_written_hash{$prev_page_number} = '';
         }
         #print STDERR "1: The AE_written_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_written_hash ), "\n";

         #print STDERR "1: The SI_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_hash ), "\n";

         if (exists($SI_hash{$prev_page_number}))# && !(exists($SI_written_hash{$prev_page_number})))
         {
            ($page_hash{SI}) = $SI_hash{$prev_page_number};
            delete $SI_hash{$prev_page_number};
#            $SI_written_hash{$prev_page_number} = '';
         }
         #print STDERR "1: The SI_written_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_written_hash ), "\n";

         #print STDERR "1: The TB_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_hash ), "\n";

         if (exists($TB_hash{$prev_page_number}))# && !(exists($TB_written_hash{$prev_page_number})))
         {
            ($page_hash{TB}) = $TB_hash{$prev_page_number};
            delete $TB_hash{$prev_page_number};
#            $TB_written_hash{$prev_page_number} = '';
         }
         #print STDERR "1: The TB_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_written_hash ), "\n";

         if (exists($TS_hash{$prev_page_number}))# && !(exists($TS_written_hash{$prev_page_number})))
         {
            ($page_hash{TS}) = $TS_hash{$prev_page_number};
            delete $TS_hash{$prev_page_number};
#            $TS_written_hash{$prev_page_number} = '';
         }
         #print STDERR "1: The TS_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TS_written_hash ), "\n";
     
         mprint ('+++Writing record for page: '.$prev_page_number."\n");
       #  print STDERR '+++Writing record for page: '.$prev_page_number."\n";
         &add_format_b_tags('page_hash');
         &write_page_record();
         %page_hash = ();

		
         # Increment the prev_page_number, by incrementing just the page ID at the end of the value...
         (my $prev_id, $prev_num) = $prev_page_number =~m:^(.*)-(\d+)$:;
         $prev_num++;
#         $next_num = $prev_num + 1;
         $next_num = $prev_num;
         $prev_page_number = $prev_id ."-".sprintf("%04d", $next_num);
             
         # If the page numbers still aren't equal, we need to populate the AIF information...
         #mprint ("NEW prev_page_number: $prev_page_number\narticle_hash{PID}: $article_hash{PID}\n");
         #print STDERR "NEW prev_page_number: $prev_page_number\narticle_hash{PID}: $article_hash{PID}\n\n";

         #mprint ("next_num: $next_num\n");

         if (@AIF_array)
         {
            for (my $i=0; $i<=$#AIF_array; $i++)
            {
               if ($AIF_array[$i] =~ m:pgref="$next_num":ms)
               {
                   #mprint ("Found AIF data: $AIF_array[$i]\n");

                   push (@{$page_hash{AIF}}, $AIF_array[$i]);
                   #splice(@AIF_array, $i, 1);
                   $AIF_array[$i] = undef;
               }
            }
         }

         # Fake out the converter, so that continuation page records get the proper PID...
         $article_hash{PID} = $prev_page_number;
      }

      ($page_rn_base) = $article_hash{RN} =~m:^\d{2}(\d{8})$:;
      &create_page_record();

	  # Updated by photon 12-11-2008 [dd-mm-yyyy]	   
	  $page_hash{PI} = $get_temp_pi;

      if ($prev_page_number)
      {
         # Assign the actual Page ID back to $article_hash{PID}...
         $article_hash{PID} = $curr_page_number;
      }
      else
      {
         #$prev_page_number = $article_hash{PID};
         $prev_page_number = $true_page_id;

         # If there wasn't a previous page, there's no reason to print out any pages yet, so skip to the end...
         last;
      }
   }#while loop

   # Write out the last page record in the issue...
   
   # Populate the AE, SI, TS and TB tags from the stored values at the page-level, if present...
   # Need to know current page (use $prev_num or $curr_num)


   #print STDERR "2: The AE_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_hash ), "\n";

   if (exists($AE_hash{$prev_page_number}))# && !(exists($AE_written_hash{$prev_page_number})))
   {
      ($page_hash{AE}) = $AE_hash{$prev_page_number};
      delete $AE_hash{$prev_page_number};
#      $AE_written_hash{$prev_page_number} = '';
   }
   #print STDERR "2: The AE_written_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_written_hash ), "\n";

   #print STDERR "2: The SI_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_hash ), "\n";

   if (exists($SI_hash{$prev_page_number}))# && !(exists($SI_written_hash{$prev_page_number})))
   {
      ($page_hash{SI}) = $SI_hash{$prev_page_number};
      delete $SI_hash{$prev_page_number};
#      $SI_written_hash{$prev_page_number} = '';
   }
   #print STDERR "2: The SI_written_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_written_hash ), "\n";

   #print STDERR "2: The TB_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_hash ), "\n";

   if (exists($TB_hash{$prev_page_number}))# && !(exists($TB_written_hash{$prev_page_number})))
   {
      ($page_hash{TB}) = $TB_hash{$prev_page_number};
      delete $TB_hash{$prev_page_number};
#      $TB_written_hash{$prev_page_number} = '';
   }
   #print STDERR "2: The TB_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_written_hash ), "\n";

   if (exists($TS_hash{$prev_page_number}))# && !(exists($TS_written_hash{$prev_page_number})))
   {
      ($page_hash{TS}) = $TS_hash{$prev_page_number};
      delete $TS_hash{$prev_page_number};
#      $TS_written_hash{$prev_page_number} = '';
   }
   #print STDERR "2: The TS_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TS_written_hash ), "\n";
     

   #print STDERR "\n!article_num:$true_page_id and prev page number:$prev_page_number" .
   #             "\n!prev_num is $prev_num and article num is $article_num" .
   #             "\n!prev_num is $prev_num and IP value is $issue_hash{IP}\n";

	     	     
   mprint ('+++Writing record for page: '.$prev_page_number."\n");
   #print STDERR '+++Writing record for page: '.$prev_page_number."\n";
   &add_format_b_tags('page_hash');
   &write_page_record();
   %page_hash = ();
   %article_hash=();
   
   # If the MATP record hasn't yet been written, output it, then turn the flag off...
   if ($mcode_hash{$issue_hash{BA}}{OUTPUT})
   {
      mprint ('Creating MATP record...');
      &create_matp_record();
      &add_format_b_tags('matp_hash');
      &write_matp_record();
      %matp_hash = ();
      $mcode_hash{$issue_hash{BA}}{OUTPUT} = 0;
   }

   unless ($dvi_name eq 'TLS' || $dvi_name eq 'ECON')
   {
      # Calculate the average OCR for the entire newspaper issue...
      foreach my $article_ocr (@ocr_values)
      {
         $issue_hash{OCR} += $article_ocr;
      }
      $issue_hash{OCR} = $issue_hash{OCR} / scalar(@ocr_values);
      $issue_hash{OCR} =~s:^(\d+\.\d{2}).*$:$1:;
      $issue_hash{OCR} =~ s/^0$//;    ################# Updated by Photon
   }

   mprint ("Writing record for issue: $issue_hash{IID}");
   &add_format_b_tags('issue_hash');
   &write_issue_record();
   %issue_hash = ();


   close (NCNPIN);
   
   &continuation_page_backward();

   %AE_hash = ();
   %SI_hash = ();
   %TB_hash = ();
   %TS_hash = ();
#   %TS_written_hash = ();

   if ($platform eq 'VMS')
   {
      move($input_file,$completed_dir);
   }

}# end of while (my $file = shift(@inputfiles))

print STDERR "\n total authors : $author_count\n";


# If this is a "process headnotes only" run, create all of the MATP records...
if ($only_headnotes)
{
   &process_only_headnotes();
}
elsif ($only_spotlight)
{
  process_only_spotlight();
}
elsif ($only_tables)
{
  process_only_tables();
}

&write_trailer_rec;


# Close the output file...
close ($NCNPOUT);

# Lastly, move the manifest file to the completed directory...
move($manifest_file,$completed_dir);


# Two new subroutines to update DVI Issue numbers
if ( $dvi_name eq 'STHA' )
{
   # Write out the Issue Last Number Used file... MAH 03/02/2012
   &write_issue_last_num_file();

   # Write out the Issue ID RN MAP file... MAH 03/02/2012
   &write_issue_id_rn_map_file();
}

#==============================
# End of main processing loop #
#==============================

mprint ("\nProgram reached completion");
print STDERR "\nProgram reached completion\n";

mprint ("\nRECORD COUNTS\nPage Records Read: $read_count\nTotal Records Written: $write_count");
print STDERR "\nRECORD COUNTS\nPage Records Read: $read_count\nTotal Records Written: $write_count\n";

mprint( "End time:  ".scalar (localtime)) ;
print STDERR "End time:  ".scalar (localtime) ."\n";

$endtime=time;
mprint ( sprintf "\nElapsed actual time to run this script: %.2f seconds\n",$endtime-$starttime);
print STDERR sprintf "\nElapsed actual time to run this script: %.2f seconds\n",$endtime-$starttime . "\n";

if ($write_count < 1)
{
   mprint ("\nWarning: There were no records in the input file $file\n");
   print STDERR "\nWarning: There were no records in the input file $file\n\n";
}
else
{
   mprint( sprintf "Average speed per record: %.2f seconds\n",($endtime-$starttime)/$write_count);
   print STDERR sprintf "Average speed per record: %.2f seconds\n",($endtime-$starttime)/$write_count . "\n";
}

$complete=1;

# Set return status:
# Unix: 0 for success, 1 for failure
# VMS:  0 for failure, 1 for success
if ($platform eq 'Unix')
{
   exit(0);
}
elsif ($platform eq 'VMS')
{
   exit(1);
}

#END=========================================================


#=================================================================
sub program_setup
{
  if((@ARGV < 2) || (@ARGV > 3))
  {
     print "\nCommand line incorrect!\n\nUsage: perl $0 " .
           ' <option-file> <manifest-of-XML-files | only_headnotes | only_spotlight | only_tables> [<logfile>]' .
           "\n\nThis program converts NCUP, SASN, FTIM, ILN, TLS, ECON, PPNP, LSNR, TDA (1986+) and STHA XML data to the Gale B format\n\n";
     exit(44);
  }


  ####################################

  # Open and process the OPT file...
  $opt_file=$ARGV[0];
  open(OPTFILE,"<$opt_file") || die "\n\nError opening option file $opt_file: $!.\n\n";
  mprint("Opened option file:  $opt_file");

  &load_opt;

  ####################################

  # Process only headnote records/create only MATP records....
  if ($ARGV[1] =~m:^only_headnotes$:i)
  {
     mprint("\nPROCESSING HEADNOTES ONLY...\n");
     $only_headnotes = 1;
     $manifest_file=$dvi_name . '_only_headnotes_' . $datestamp;
  }
  elsif ($ARGV[1] =~m:^only_spotlight$:i)
  {
     mprint("\nPROCESSING SPOTLIGHT ONLY...\n");
     $only_spotlight = 1;
     $manifest_file=$dvi_name . '_only_spotlight_' . $datestamp;
  }
  elsif ($ARGV[1] =~m:^only_tables$:i)
  {
      mprint("\nPROCESSING TABLES ONLY...\n");
      $only_tables = 1;
      $manifest_file=$dvi_name . '_only_tables_' . $datestamp;
  }
  else  #READ MANIFEST OF XML FILES..
  {
     $manifest_file=$ARGV[1];
     open(MANIFEST,"<$manifest_file") || die "\n\nError opening manifest file $manifest_file: $!.\n\n";
     mprint("\nOpened Manifest file: $manifest_file");

     &read_manifest;
  }
  ####################################

  if ($platform eq "VMS")
  {
     $headnote_dir        = $headnote_dir_vms;
     $metadata_file       = $metadata_file_vms;
	 $dvi_ng_map          = $dvi_ng_map_vms;
     $dvi_il_map          = $dvi_il_map_vms;
     $dvi_issue_lastnum   = $dvi_issue_lastnum_vms;
     $dvi_issue_id_rn_map = $dvi_issue_id_rn_map_vms;
     $PageIDList          = $PageIDList_vms;
  }
  else
  {
     $headnote_dir        = $headnote_dir_unix;
     $metadata_file       = $metadata_file_unix;
     $dvi_ng_map          = $dvi_ng_map_unix;
     $dvi_il_map          = $dvi_il_map_unix;
     $dvi_issue_lastnum   = $dvi_issue_lastnum_unix;
     $dvi_issue_id_rn_map = $dvi_issue_id_rn_map_unix;
     $PageIDList          = $PageIDList_unix;

  }

  ###############################################################################
  # Get the NCNP metadata file from srvr99, as well as all the headnote records #
  ###############################################################################
  if ($platform eq "VMS")
  {
     &ftp_files;

     # Remove old headnote and metadata files from VMS...
     system "purge $metadata_file_vms";
     system "purge $headnote_dir_vms";
	 system "purge $dvi_ng_map_vms";
     system "purge $dvi_il_map_vms";
     system "purge $dvi_issue_lastnum_vms";
     system "purge $dvi_issue_id_rn_map_vms";
  }

  foreach my $datafile (@datafiles)
  {
     if( $datafile =~ /.*?\.xml/i)
     {
        push(@inputfiles, "$datafile");
     }
  }

  if (!(scalar(@inputfiles)) && !($only_headnotes) && !($only_spotlight) && !($only_tables))
  {
     mprint("\n***There were no XML files listed inside the manifest file: $manifest_file\n");
     die;
  }


  # Read in the metadata file...
  &read_metadata_file();

  # Read in the metadata file...
  &read_dvi_ng_map_file(); ###Updated by Photon

  # Read in the metadata file...
  &read_dvi_il_map_file(); ###Updated by Photon

  # Read in the Page ID list...
  &read_page_id_list();

  # Read in the Issue Last Number Used file... MAH 03/02/2012
  &read_issue_last_num_file();

  # Read in the Issue ID RN MAP file... MAH 03/02/2012
  &read_issue_id_rn_map_file();


  # Read in the Table ID list, if necessary...
  if (defined($TableIDList))
  {
     &read_table_id_list();
  }


  # Open the log file...
  if(@ARGV == 3)
  {
     $logfile = $log_dir.$ARGV[2];
  }
  else
  {
     $logfile = $log_dir."dvi_newspaper_convert_".$yearstamp.$monthstamp.$mday.$min.$sec.".log";
  }

  open(LOGFP, "+>$logfile") || die "\n\nError opening log file $logfile: $!.\n\n";

  mprint("Opened logfile: $logfile");
  $mess .= "Log file: $logfile\n";


  # Output some messages to the screen...
  mprint("\nPerl program name: " . $0);
  mprint('Copyright 2006, Thomson Gale, all rights reserved.');
  mprint('Program to convert 19th Century Newspaper XML data into Gale B format.');
  mprint('v1.0 July 2006 Ryan Cartmill');

  $progstart = (times)[0];
  $starttime = time;

  mprint("\n". 'Start time:  ' . scalar(localtime));
  ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

  return;
}# end of sub program_setup
#==================================================================================
sub load_opt ()
{
   %valid_options = (completed_dir            => '',
                     email                    => '',
                     headnote_dir_unix        => '',
                     headnote_dir_vms         => '',
                     input_dir                => '',
                     log_dir                  => '',
                     metadata_file_unix       => '',
                     metadata_file_vms        => '',
        			 output_dir               => '',
                     PageIDList_unix          => '',
                     PageIDList_vms           => '',
                     dvi_ng_map_unix          => '',
                     dvi_ng_map_vms	          => '',
                     dvi_il_map_unix          => '',
                     dvi_il_map_vms	          => '',
                     dvi_issue_lastnum_unix   => '',
                     dvi_issue_lastnum_vms    => '',
                     dvi_issue_id_rn_map_unix => '',
                     dvi_issue_id_rn_map_vms  => '',
                     dvi_name                 => '',
                     xxrn                     => ''
   );

   while (my $optline = <OPTFILE>)
   {
      if ($optline =~m:^!:)
      {
         next;
      }

      $optline =~s:[\n\r]*::g;
      ($option, $value) = ($optline =~m/(.*?):\s*(.*?)$/);

      if($option ne "")
      {
         $opt{$option} = $value;
      }
   }

   while((my $key, my $value) = each %opt)
   {
      if($key =~m:^$:)
      {
         next;
      }
      elsif ($key =~m:^completed_dir$:i)
      {
         $valid_options{completed_dir} = $value;
         mprint("Completed directory: $value");
         $completed_dir = $value;
      }
      elsif ($key =~m:^email$:i)
      {
         $valid_options{email} = $value;

         if($value ne "")
         {
            mprint("Email:               $value");
            $email_address = $value;
         }
         else
         {
            mprint("\n+++ Email address missing.  No email will be sent.\n");
         }
      }
      elsif ($key =~m:^headnote_dir_unix$:i)
      {
         $valid_options{headnote_dir_unix} = $value;
         mprint("Headnote directory (Unix):  $value");
         $headnote_dir_unix = $value;
      }
      elsif ($key =~m:^headnote_dir_vms$:i)
      {
         $valid_options{headnote_dir_vms} = $value;
         mprint("Headnote directory (VMS):  $value");
         $headnote_dir_vms = $value;
      }
      elsif ($key =~m:^input_dir$:i)
      {
         $valid_options{input_dir} = $value;
         mprint("Input directory:     $value");
         $input_dir = $value;
      }
      elsif ($key =~m:^log_dir$:i)
      {
         $valid_options{log_dir} = $value;
         mprint("Log Directory:       $value");
         $log_dir = $value;
      }
      elsif ($key =~m:^metadata_file_unix$:i)
      {
         $valid_options{metadata_file_unix} = $value;
         mprint("Metadata file (Unix):       $value");
         $metadata_file_unix = $value;
      }
      elsif ($key =~m:^metadata_file_vms$:i)
      {
         $valid_options{metadata_file_vms} = $value;
         mprint("Metadata file (VMS):       $value");
         $metadata_file_vms = $value;
      }
      elsif ($key =~m:^output_dir$:i)
      {
         $valid_options{output_dir} = $value;
         mprint("Output directory:    $value");
         $output_dir = $value;
      }
      elsif ($key =~m:^PageIDList_unix$:i) ###Updated by Photon
      {
         $valid_options{PageIDList_unix} = $value;
         mprint("PageIDList_unix file:    $value");
         $PageIDList_unix = $value;
      }
      elsif ($key =~m:^PageIDList_vms$:i)  ###Updated by Photon
      {
         $valid_options{PageIDList_vms} = $value;
         mprint("PageIDList_vms file:    $value");
         $PageIDList_vms = $value;
      }
      elsif ($key =~m:^dvi_ng_map_unix$:i) ###Updated by Photon
      {
         $valid_options{dvi_ng_map_unix} = $value;
         mprint("DVI_NG_map_unix file:    $value");
         $dvi_ng_map_unix = $value;
      }
      elsif ($key =~m:^dvi_ng_map_vms$:i)  ###Updated by Photon
      {
         $valid_options{dvi_ng_map_vms} = $value;
         mprint("DVI_NG_map_vms file:    $value");
         $dvi_ng_map_vms = $value;
      }
      elsif ($key =~m:^dvi_il_map_unix$:i) ###Updated by Photon
      {
         $valid_options{dvi_il_map_unix} = $value;
         mprint("DVI_IL_map_unix file:    $value");
         $dvi_il_map_unix = $value;
      }
      elsif ($key =~m:^dvi_il_map_vms$:i)  ###Updated by Photon
      {
         $valid_options{dvi_il_map_vms} = $value;
         mprint("DVI_IL_map_vms file:    $value");
         $dvi_il_map_vms = $value;
      }
      elsif ($key =~m:^dvi_issue_lastnum_unix$:i)   ###Updated by MAH 03/02/2012
      {
         $valid_options{dvi_issue_lastnum_unix}   = $value;
         mprint("dvi_issue_lastnum_unix file:       $value");
         $dvi_issue_lastnum_unix = $value;
      }
      elsif ($key =~m:^dvi_issue_lastnum_vms$:i)    ###Updated by MAH 03/02/2012
      {
         $valid_options{dvi_issue_lastnum_vms}    = $value;
         mprint("dvi_issue_lastnum_vms file:        $value");
         $dvi_issue_lastnum_vms = $value;
      }
      elsif ($key =~m:^dvi_issue_id_rn_map_unix$:i) ###Updated by MAH 03/02/2012
      {
         $valid_options{dvi_issue_id_rn_map_unix} = $value;
         mprint("dvi_issue_id_rn_map_unix file:     $value");
         $dvi_issue_id_rn_map_unix = $value;
      }
      elsif ($key =~m:^dvi_issue_id_rn_map_vms$:i)  ###Updated by MAH 03/02/2012
      {
         $valid_options{dvi_issue_id_rn_map_vms}  = $value;
         mprint("dvi_issue_id_rn_map_vms file:      $value");
         $dvi_issue_id_rn_map_vms  = $value;
      }
      elsif ($key =~m:^dvi_name$:i)        ###Updated by Ryan
      {
         # Lowercase the DVI Name value, just in case...
         $value = lc($value);
         $valid_options{dvi_name} = $value;
         mprint("DVI Name:    $value");
         # Automatically uppercase this value, for standardization...
         $dvi_name = "\U$value";
      }
      elsif ($key =~m:^xxrn$:i)
      {
         $valid_options{xxrn} = $value;
         mprint("XXRN:                $value");
         $xxrn_value = $value;
      }
      elsif ($key =~m:^spotlight_file$:i)
      {
         $valid_options{spotlight_file} = $value;
         mprint("Spotlight File:                $value");
         $spotlight_file = $value;
      }
      elsif ($key =~m:^table_dir$:i)
      {
         $valid_options{table_dir} = $value;
         mprint("Table Directory:                $value");
         $table_dir = $value;
      }
      elsif ($key =~m:^TableIDList$:i)
      {
         $valid_options{TableIDList} = $value;
         mprint("TableIDList file:    $value");
         $TableIDList = $value;
      }
      else # Skip all unknown options...
      {
         next;
      }
   } #while each %opt

   # Do a final check, and make sure all valid options are populated; if not, exit program...
   while ((my $key, my $value) = each %valid_options)
   {
      if ($value !~m:\S:)
      {
         mprint ("Fatal error in control file - value for [$key] is missing.");
         $mess = "Program failure: Fatal error in control file - value for [$key] is missing\n\n";
         exit(44);
      }
   }

   close(OPTFILE);
   return;
}
#==================================================================================
sub ftp_files
{
   mprint ("\nFTPing fresh NCNP Metadata and Headnote files from srvr99 ...");

   $hostname = 'srvr99.gale.com';

   $ftp = Net::FTP->new($hostname);
   $ftp->login("essocm","03esstemp");

   $ftp->get($dvi_il_map_unix,$dvi_il_map_vms);
   $ftp->get($dvi_ng_map_unix,$dvi_ng_map_vms);
   $ftp->get($metadata_file_unix,$metadata_file_vms);
   $ftp->get($dvi_issue_lastnum_unix,$dvi_issue_lastnum_vms);
   $ftp->get($dvi_issue_id_rn_map_unix,$dvi_issue_id_rn_map_vms);

   foreach my $headfile ($ftp->ls($headnote_dir_unix))
   {
      #print STDERR "Grabbing $headnote_dir_unix$headfile\n";
      $ftp->get($headnote_dir_unix.$headfile, $headnote_dir_vms.$headfile);
   }

   $ftp->quit;

   mprint (" Done!\n");

}#end of sub ftp_files
#===============================================================================
################################################################################
# Read in the piped access file and populate the eisbn_piped hash              #
################################################################################
sub read_metadata_file
{
   open(META,"<$metadata_file") || die "\nError opening $metadata_file: $!.\n";
   mprint("Opened metadata file: $metadata_file");

   local $/ = "\n";

   while(my $meta_line = <META>)
   {
      # Remove the DOS hard return...
      $meta_line =~s:[\r\n]*::g;

      (my @metadata_temp) = split (/[|]/, $meta_line);

      my ($mcode, $title, $xz_title, $short_title, $lccn_id, $language, $pubformat, $frequency, $variant_title, $start_year, $end_year, $xml_file, $city,
          $state, $state_abbr, $region, $country, $source_library, $matp_rn, $copyright, $author_BU, $publisher_PB, $shelfmark, $collection_marc,
          $collection_lccn, $collection_estc, $ij1, $ij2, $ij3, $ij4, $ij5, $module, $spotlight_rn, $ztag, $marc_rn);

      if (scalar(@metadata_temp) == 32)
      {
          ($mcode, $title, $xz_title, $short_title, $lccn_id, $language, $pubformat, $frequency, $variant_title, $start_year, $end_year, $xml_file, $city,
           $state, $state_abbr, $region, $country, $source_library, $matp_rn, $copyright, $author_BU, $publisher_PB, $shelfmark, $collection_marc,
	   $collection_lccn, $collection_estc, $ij1, $ij2, $ij3, $ij4, $ij5, $module) = @metadata_temp;
      }
      elsif (scalar(@metadata_temp) == 33)
      {
          ($mcode, $title, $xz_title, $short_title, $lccn_id, $language, $pubformat, $frequency, $variant_title, $start_year, $end_year, $xml_file, $city,
           $state, $state_abbr, $region, $country, $source_library, $matp_rn, $copyright, $author_BU, $publisher_PB, $shelfmark, $collection_marc,
	   $collection_lccn, $collection_estc, $ij1, $ij2, $ij3, $ij4, $ij5, $module, $marc_rn) = @metadata_temp;
      }
      elsif (scalar(@metadata_temp) == 30)
      {
         ($mcode, $title, $xz_title, $short_title, $lccn_id, $language, $pubformat, $frequency, $variant_title, $start_year, $end_year, $xml_file, $city,
          $state, $state_abbr, $region, $country,$source_library, $matp_rn, $copyright, $author_BU, $publisher_PB, $shelfmark, $collection_marc,
          $collection_lccn, $collection_estc, $module, $spotlight_rn, $ztag, $marc_rn) = @metadata_temp;
      }
      elsif (scalar(@metadata_temp) == 27)
      {
         ($mcode, $title, $xz_title, $short_title, $lccn_id, $language, $pubformat, $frequency, $variant_title, $start_year, $end_year, $xml_file, $city,
          $state, $state_abbr, $region, $country,$source_library, $matp_rn, $copyright, $author_BU, $publisher_PB, $shelfmark, $collection_marc,
          $collection_lccn, $collection_estc, $module) = @metadata_temp;
      }
      else
      {
         mprint ("\n*** Metadata file doesn't contain 30, 32 or 33 columns: $metadata_file");
         print STDERR "\n*** Metadata file doesn't contain 30, 32 or 33 columns: $metadata_file\n" . scalar(@metadata_temp) . "\n+++$meta_line---\n";
         exit (44);
      }


      # Skip the line if it contains field names...
      next if ($mcode eq "ba");


	  $xml_mcode{$lccn_id} = $mcode;
      $mcode_hash{$mcode}{JN} = $title;
      $mcode_hash{$mcode}{XZ}=$xz_title;
      $mcode_hash{$mcode}{HT}=$short_title;
      $mcode_hash{$mcode}{N_ID}=$lccn_id;
      $mcode_hash{$mcode}{ID}{$lccn_id}{VARIANT_TITLE} = $variant_title;
      $mcode_hash{$mcode}{ID}{$lccn_id}{XML_FILE} = $xml_file;
      $mcode_hash{$mcode}{ID}{$lccn_id}{START_YEAR} = $start_year;
      $mcode_hash{$mcode}{ID}{$lccn_id}{END_YEAR} = $end_year;
      $mcode_hash{$mcode}{MATP_RN} = $matp_rn;       ########### Dummy tag has been updated by Photon.........
      $mcode_hash{$mcode}{PC} = $city;
      $mcode_hash{$mcode}{PS} = $state;
      $mcode_hash{$mcode}{PN} = $country;
      $mcode_hash{$mcode}{LB} = $source_library;
      $mcode_hash{$mcode}{CP} = $copyright;
      $mcode_hash{$mcode}{BU} = $author_BU;
      $mcode_hash{$mcode}{PB} = $publisher_PB;
      $mcode_hash{$mcode}{HL} = $shelfmark;
      $mcode_hash{$mcode}{ID}{$lccn_id}{ZI} = $collection_marc;     #Updated by photon
      $mcode_hash{$mcode}{ID}{$lccn_id}{ZJ} = $collection_lccn;     #Updated by photon
      $mcode_hash{$mcode}{ID}{$lccn_id}{ZK} = $collection_estc;     #Updated by photon
      if($country eq "England" or $city eq "London")
      {
      	       $mcode_hash{$mcode}{PR} = $region;
      }
      $mcode_hash{$mcode}{LA} = $language;
      $mcode_hash{$mcode}{FQ} = $frequency;
      $mcode_hash{$mcode}{FO} = $pubformat;
      $mcode_hash{$mcode}{ST} = $state_abbr;
      $mcode_hash{$mcode}{IJ} = join('|',$ij1,$ij2,$ij3,$ij4,$ij5);
      $mcode_hash{$mcode}{SH} = $module;
      $mcode_hash{$mcode}{OUTPUT} = 1;
      $mcode_hash{$mcode}{SPOTLIGHT_RN} = $spotlight_rn;
      $mcode_hash{$mcode}{ZT} = $ztag;
      $mcode_hash{$mcode}{MARC_RN} = $marc_rn;       ########### Dummy tag has been updated by Photon.........


      $new_id{$lccn_id}{CP} = $copyright;
      $new_id{$lccn_id}{LB} = $source_library;

  }

   close(META);

}#end of sub read_metadata_file
#=========================================================

sub read_dvi_ng_map_file
{
   open(NG,"<$dvi_ng_map") || die "\nError opening $dvi_ng_map: $!.\n";
   mprint("Opened DVI_NG_map file: $dvi_ng_map");

   local $/ = "\n";

   while(my $ng_line = <NG>)
   {
	    $ng_line =~s/(\n|\r)//g;
	   (my $ngkey, my $ngvalue ) = split (/[|]/, $ng_line);
		$ngkey =~ s/(\s)(&amp;|&)(\s)/$1and$3/g;
	    $ng_hash{$ngkey} = $ngvalue;
   }
   close(NG);

}#end of sub read_dvi_ng_map_file
#=========================================================

sub read_dvi_il_map_file
{
   open(IL,"<$dvi_il_map") || die "\nError opening $dvi_ng_map: $!.\n";
   mprint("Opened DVI_IL_map file: $dvi_ng_map");

   local $/ = "\n";

   while(my $il_line = <IL>)
   {
	      $il_line =~s/(\n|\r)//g;
		(my $ilkey, my $ilvalue ) = split (/[|]/, $il_line);
   		$ilkey =~ s/(\s)(&amp;|&)(\s)/$1and$3/g;
	    $il_hash{$ilkey} = $ilvalue;
   }
   close(IL);

}#end of sub dvi_il_map_file
#=========================================================

sub read_manifest {

   while (my $man_line = <MANIFEST>){
     $man_line =~s:[\r\n]*::g;

     (my $xml_file) = split(',', $man_line);
     $xml_file =~s:(.xml)?$:.xml:;


#     print "XML File: +++$xml_file---\n";

     push(@datafiles, $input_dir.$xml_file);
   }
   close(MANIFEST);
   return;
}
#=========================================================
sub read_page_id_list {

   open(PAGEID,"<$PageIDList") || die "\nError opening $PageIDList: $!.\n";
   mprint("Opened Page ID Lookup List: $PageIDList");

   local $/ = "\n";

   while (my $line = <PAGEID>){
     $line =~s:[\r\n]*::g;

     (my $page_id, my $rec_num) = split(/\|/, $line);

     $page_id_hash{$page_id} = $rec_num;
   }
   close(PAGEID);
   return;
}
#=========================================================
sub read_table_id_list {

   open(TABLEID,"<$TableIDList") || die "\nError opening $TableIDList: $!.\n";
   mprint("Opened Table ID Lookup List: $TableIDList");

   local $/ = "\n";

   while (my $line = <TABLEID>){
     $line =~s:[\r\n]*::g;

     (my $table_id, my $rec_num) = split(/\|/, $line);

     $table_id_hash{$table_id} = $rec_num;
   }
   close(TABLEID);
   return;
}

################################################################################
# Read in the last issue number used file and assign the value to a variable.  #
################################################################################
sub read_issue_last_num_file
{
   my $prev_recsep = $/;
   $/ = "\n";

   print "\nEntering the subroutine read_issue_last_num_file\n";

   open(INLASTUSED,"<$dvi_issue_lastnum") || die "\n\nError opening DVI last issue num used input file, $dvi_issue_lastnum: $!.\n\n";
   mprint("\nOpened DVI Last Issue Num Used Input file: $dvi_issue_lastnum");
   print "\nOpened DVI Last Issue Num Used Input file = $dvi_issue_lastnum\n";

   while($last_num_line = <INLASTUSED>)
   {
      # Remove the DOS hard return...
      $last_num_line =~s:[\r\n]*::;

           #print "In while last_num_line\n";
                                                                                                   
           if ($last_num_line =~ m!([0-9]{5})!s)
           {
              $DVI_last_issue_num = $1;
           }
   }

   $DVI_last_issue_num_new   = sprintf("%05d", ($DVI_last_issue_num));

   $DVI_last_issue_num_saved = sprintf("%05d", ($DVI_last_issue_num));

   #print "\nDVI_last_issue_num       = $DVI_last_issue_num\n";
   #print "DVI_last_issue_num_new   = $DVI_last_issue_num_new\n";
   #print "DVI_last_issue_num_saved = $DVI_last_issue_num_saved\n";

   close(INLASTUSED);

   $/ = $prev_recsep;

   print "\nLeaving the subroutine read_issue_last_num_file\n";

} #end of sub read_issue_last_num_file

################################################################################
# Write to the last issue number used file and assign the last number assigned.#
################################################################################
sub write_issue_last_num_file
{
   my $prev_recsep = $/;
   $/ = "\n";

   print "\nEntering the subroutine write_issue_last_num_file\n";

   #print "\nDVI_last_issue_num_new   = $DVI_last_issue_num_new\n";
   #print "DVI_last_issue_num_saved = $DVI_last_issue_num_saved\n";

   if ( $DVI_last_issue_num_new > $DVI_last_issue_num_saved )
   {
      mprint("\nIn if DVI_last_issue_num_new > DVI_last_issue_num_saved\n");
      #print "\nIn if DVI_last_issue_num_new > DVI_last_issue_num_saved\n";

      open(OUTLASTUSED,">$dvi_issue_lastnum") || die "\n\nError opening GVRL Neutral last num used output file, $dvi_issue_lastnum: $!.\n\n";

      mprint("Writing to DVI Last Issue Number Used Output file: $dvi_issue_lastnum\n");
      #print "\nWriting to DVI Issue Last Number Used Output file:       $dvi_issue_lastnum\n";
      #print "Writing the new Last Issue Number Used, DVI_last_issue_num_new   = $DVI_last_issue_num_new\n";

      print OUTLASTUSED sprintf("%05d", ($DVI_last_issue_num_new));

      close(OUTLASTUSED);
   }
   else
   {
      mprint("\nIn else for DVI_last_issue_num_new > DVI_last_issue_num_saved\n");
      #print "In else for DVI_last_issue_num_new > DVI_last_issue_num_saved\n";
   }

   $/ = $prev_recsep;

   print "\nLeaving the subroutine write_issue_last_num_file\n";

} #end of sub write_issue_last_num_file

################################################################################
# Read in the DVI Issue ID and RN pipe delimited file to find if an Issue ID   #
# previously had a Issue record number (RN) previously assigned.               #
################################################################################
sub read_issue_id_rn_map_file
{
   open(INNUM,"<$dvi_issue_id_rn_map") || die "\nError opening $dvi_issue_id_rn_map as input: $!.\n";
   mprint("Opened input dvi_issue_id_rn_map: $dvi_issue_id_rn_map");

   print "\nEntering the subroutine read_issue_id_rn_map_file\n";

   my $prev_recsep = $/;
   $/ = "\n";

   while($dvi_issue_id_rn_map_line = <INNUM>)
   {
      # Remove the DOS hard return...
      $dvi_issue_id_rn_map_line =~s:[\r\n]*::;

      #print "In while dvi_issue_id_rn_map_line\n";

      #  skip header line                 Issue ID|Issue RN
      if ($dvi_issue_id_rn_map_line =~ m!^Issue ID\|Issue RN$!s)
      {
         print "In if skipping header line\n";
      }
                                             #STHA-1822-1020|00001
      elsif ( $dvi_issue_id_rn_map_line =~ m#^([A-Za-z]{4}-[0-9]{4}-[0-9]{4})\|([0-9]{5})$# )
      {
         $dvi_issue_id_map_number = $1;
         $dvi_issue_rn_map_number = $2;
         print 'In elsif (dvi_issue_id_rn_map_line =~ m!^([A-Za-z]{4}\-[0-9]{4}\-[0-9]{4})\|([0-9]{5})$!s)' . "\n";

         $DVI_issue_num_hash{$dvi_issue_id_map_number} = $dvi_issue_rn_map_number;
         print "dvi_issue_id_map_number                     = $dvi_issue_id_map_number\n";
         print "dvi_issue_rn_map_number                     = $dvi_issue_rn_map_number\n";
         #print "DVI_issue_num_hash{dvi_issue_id_map_number} = $DVI_issue_num_hash{$dvi_issue_id_map_number}\n";
      }
      else
      {
         print "In else match  dvi_issue_id_rn_map_line = $dvi_issue_id_rn_map_line\n";
      }
   }

   close(INNUM);

   $/ = $prev_recsep;

   print "\nLeaving the subroutine read_issue_id_rn_map_file\n";

} #end of sub read_issue_id_rn_map_file

################################################################################
# Write out the updated DVI Issue ID and RN hash to the dvi_issue_id_rn_map    #
# file.                                                                        #
################################################################################
sub write_issue_id_rn_map_file
{
   #$DVI_issue_num_hash{$dvi_issue_id_map_number} = $dvi_issue_rn_map_number;

   print "\nEntering the subroutine write_issue_id_rn_map_file\n";

   $dvi_id_rn_hash_write_count = 0;

   open(OUTNUM,">$dvi_issue_id_rn_map") || die "\nError opening $dvi_issue_id_rn_map as output: $!.\n";
   mprint("Opened output dvi_issue_id_rn_map: $dvi_issue_id_rn_map");

   # For every piece of data in the updated hash, print it out in the correct order to the dvi issue id rn map file.

   foreach my $key (sort (keys %DVI_issue_num_hash))
   {
      print OUTNUM $key . "|" . sprintf("%05d", ($DVI_issue_num_hash{$key})) . "\n";

      $dvi_id_rn_hash_write_count++;
   }

   print "\ndvi_id_rn_hash_write_count = $dvi_id_rn_hash_write_count\n";

   close(OUTNUM);

   print "\nLeaving the subroutine write_issue_id_rn_map_file\n";

   return;
   
} #end of sub write_issue_id_rn_map_file

################################################################################
sub mprint
{
    my $message=shift(@_);

    # Suppressed output to the screen to increase BLNP conversion speed
    #if ($platform eq 'VMS')
    #{
    #   print STDERR "$message\n";
    #}

    print LOGFP "$message\n";
    $mess .= "$message\n";
}
#=========================================================
sub lrtrim
{
    my $fld=shift @_;
    $fld =~s:^ +::gs;
    $fld =~s: +$::gs;
    return($fld);
}
#=========================================================
sub clean
{
   my $line=shift(@_);

   $line =~s:[\r\n]::gs;
   $line =~s:^ +::gs;
   $line =~s: +$::gs;

   $line =~s:& :&amp; :g;
   $line =~s:\205:...:g;
   $line =~s:\221:':g;
   $line =~s:\222:':g;
   $line =~s:\223:&quot;:g;
   $line =~s:\224:&quot;:g;
#   $line =~s:\225:&#x2022;:g;
   $line =~s:\226:-:g;
   $line =~s:\227:--:g;

   # Convert &#160; through &#255; to their actual characters...
   $line =~s:&#(\d+);:convert_entity($1):eig;

   # Remap some high-end hexadecimal entities that the LSNR application can't handle...
   if ($dvi_name eq 'LSNR')
   {
      $line =~s:&#x014D;:o:g;
      $line =~s:&#x0152;:OE:g;
      $line =~s:&#x0153;:oe:g;
      $line =~s:&#x0161;:s:g;
      $line =~s:&#x2013;:-:g;
      $line =~s:&#x2014;:--:g;
      $line =~s:&#x2026;:&hellip;:g;
      $line =~s:&#x20AC;:--:g;
      $line =~s:&#x2020;:+:g;
   }

   # Replace characters lower than 32 and higher than 255 with a space...
   $line =~s:[^ -\x{FF}]: :g;
   
   return ($line);
}
#=========================================================
sub conv_NCNP
{
   # Process the Text Preamble/Title
   foreach my $lead_text (@text_preamble, @text_title)
   {
      # Remove ALL whitespace in the content...
      $lead_text =~s:>\s+<:><:sg;
      $lead_text =~s:^\s+::sg;

      # Put a space between every word tag so that the words will index after tags are stripped...
      $lead_text =~s:</wd>:</wd> :sg;

      # Remove the trailing space in the content...
      $lead_text =~s:\s+$::sg;

      # For Page Information field:
      # Get the Position Guide (one per clip rectangle)
      #(my $pos_guide_tag) = $lead_text =~m:(<pg\s+pgref="(.*?)"[^>]+pos="(.*?)"):s;
      # Making this less-restrictive:
      (my $pos_guide_tag) = $lead_text =~m:(<pg[^>/]+):s;
	  #print STDERR "POS_GUIDE_TAG (lead): $pos_guide_tag\n";
      &create_AIF_PIF($pos_guide_tag);

      # Add Text Preamble/Title to beginning of fulltext
      push(@{$article_hash{TX}}, $lead_text);
   }


   # Process the Article Mainbody Text

#HANDLING PG , creating PIF fields:  format of pg tag:  <pg pgref="1" pos="93,1205,772,2376"></pg>
#now we have multi-paragraph text.cr sections, each with a pg tag at the top...
#there should now be one PIF field per pg tag (per clip rectangle)

   $article_hash{WC} = 0;

   foreach my $clip_rec (@text_cr)
   {
      # For Page Information field:
      # Get the Position Guide (one per clip rectangle)
      #(my $pos_guide_tag) = $clip_rec =~m:(<pg\s+pgref="(.*?)"[^>]+pos="(.*?)".*?>):s;
      # Making this less-restrictive:
      (my $pos_guide_tag) = $clip_rec =~m:(<pg[^>]+>):s;
	  #print STDERR "POS_GUIDE_TAG (cr): $pos_guide_tag\n";
      &create_AIF_PIF($pos_guide_tag);

      # Start the clip rectangle
      push(@{$article_hash{TX}}, '<text.cr>'.$pos_guide_tag);

      (my @para_array) = $clip_rec =~m:.*?(<p[^>]*>.*?</p>):sg;

      foreach my $para (@para_array)
      {
         (my @words) = ($para =~m:(<wd\spos.*?/wd>):sg);
         $article_hash{WC} += scalar(@words);

         # Remove ALL whitespace in the content...
         $para =~s:>\s+<:><:sg;
         $para =~s:^\s+::sg;
         $para =~s:\s+$::sg;

         # Fix the hyphenated words in the paragraph...
         $para = &fix_hyphenated($para);

         # Remove any trailing whitespace in the content...
         $para =~s:\s+$::sg;

         push(@{$article_hash{TX}}, '<p>' . $para . '</p>');
      }# end of foreach my $para (@para_array)

      # End the clip rectangle
      push(@{$article_hash{TX}}, '</text.cr>');

   }# end of foreach my $clip_rec (@text_cr)

   if ($article_hash{WC} != 0)
   {
      push(@{$article_hash{AC}}, 'F');
   }


   if (scalar(@{$article_hash{TX}}))
   {

      # Insert the <text> and </text> tags, if we actually had text...
      unshift(@{$article_hash{TX}}, '<text>');
      push(@{$article_hash{TX}}, '</text>');

      my @temp_text = ();

      foreach my $item (@{$article_hash{TX}})
      {
         # Prepare the XML data with namespace and NAK/SYN codes...
         $item = prep_XML_tags(prep_XML_entities(clean($item)));

         if(length($item) >= 8000)
         {
            my @out_tx = reduce_text($item);
            push(@temp_text, @out_tx);
         }
         else
         {
            push(@temp_text, $item);
         }

      }

      @{$article_hash{TX}} = @temp_text;
   }# end of if (scalar(@{$article_hash{TX}}))



####PA
#                $pavalue=$apa=$pg= 'PA  '.$pa;
#                 $apa =~s:^PA  ::; #start page
#
#                unless (exists $pgnum_hash{$pa}){
#                    $pgnum_hash{$pa} = "";
#
#                    mprint ('Current $pa = '.$pa);
#
#                    # If we have missing page(s), we need to fill the void(s) in @pgnum_array ...
#                    if ($rn_page - 1 > $pgnum_counted[-1]){
#
#                      # We could have multiple missing pages...
#                      for(my $i=$pgnum_counted[-1]+1; $i<$rn_page; $i++){
#
#                        # 1) Find *actual* value of the last processed page...
#                        my $prev_pgval = $pgnum_array[-1];
#
#                        # 2) Find its index (via %roman_hash). Then, using the
#                        #    index + 1, lookup actual page val in @roman_array.
#                        #    Push this value onto the @pgnum_array to fill in
#                        #    the array gaps...
#
#                        # If we have a letter in the previous page, assume we
#                        # have a letter in the current page (= roman value)...
#
#                        # If we have uppercase roman numerals...
#                        if($prev_pgval =~m:^[A-Z]+$:){
#
#                          my $next_idx = $roman_hash{"\L$prev_pgval"} + 1;
#                          my $next_pgval= $roman_array[$next_idx];
#
#                          if (exists $roman_hash{$next_pgval}){
#                            push(@pgnum_array, "\U$next_pgval");
##          push(@pgnum_array, $roman_array[$roman_hash{$prev_pgval} + 1]);
#                          }
#                          else{
#                            die "\nValue $next_pgval NOT found in roman hash";
#                          }
#                        }
#                        # If we have lowercase roman numerals...
#                        elsif($prev_pgval =~m:^[a-z]+$:){
#
#                          my $next_idx = $roman_hash{$prev_pgval} + 1;
#                          my $next_pgval= $roman_array[$next_idx];
#
#                          if (exists $roman_hash{$next_pgval}){
#                            push(@pgnum_array, $next_pgval);
##          push(@pgnum_array, $roman_array[$roman_hash{$prev_pgval} + 1]);
#                          }
#                          else{
#                            die "\nValue $next_pgval NOT found in roman hash";
#                          }
#                        }
#                        # Otherwise, just put the numeric value on the array
#                        else{
#
#                            mprint ("\nUsing value $i for fill-in page");
#                          push(@pgnum_array,$i);
#                        }
#                        push(@pgnum_counted,$i);
#                      }
#
#                    }
#
#                    push(@pgnum_counted,$rn_page);
#                    push(@pgnum_array,$pa);
#                }
#
#                #rounding out the composite PI field
#                $is =~m:^IS  (.*?)$:i;
#                $issuenum = $1;
#                $pi = $ipi; #bringing in the value saved from the issue record
#                $pi .= "; pg. ".$apa."; Issue ".$issuenum; #finishing of composite pi field


}#end of sub conv_NCNP
#===============================================================================
sub write_article_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

   foreach my $field ($start,$article_hash{RN},$article_hash{PID},$article_hash{RT},$article_hash{ZZ},$article_hash{XT},
                      $article_hash{SE},$article_hash{SC},$article_hash{OCR},$article_hash{REL},@{$article_hash{AC}},
                      $article_hash{FO},$article_hash{RD},$article_hash{PY},$article_hash{BA},
                      $article_hash{IS},$article_hash{PI},$article_hash{JN},$article_hash{TE},$article_hash{HT},
                      $article_hash{PF},$article_hash{DA},$article_hash{YE},$article_hash{ID},$article_hash{ZI},$article_hash{ZJ},$article_hash{ZK},
                      $article_hash{IN},$article_hash{HL},$article_hash{LB},$article_hash{CP},$article_hash{LA},
                      $article_hash{ZX},$article_hash{JJ},$article_hash{WC},$article_hash{PA},@{$article_hash{PIF}},
                      $article_hash{PG},$article_hash{TP},$article_hash{NG},$article_hash{AE},@{$article_hash{IL}},$article_hash{IY},
                      $article_hash{CL},@{$article_hash{IC}},@{$article_hash{OI}},@{$article_hash{CI}},$article_hash{DW},$article_hash{ED},
                      $article_hash{TS},$article_hash{TB},$article_hash{SI},$article_hash{TI},@{$article_hash{TA}},
                      @{$article_hash{AU}},@{$article_hash{UA}},@{$article_hash{AS}},@{$article_hash{VN}},@{$article_hash{UN}},$article_hash{FW},
		      @{$article_hash{WR}},@{$article_hash{WA}},@{$article_hash{WE}},@{$article_hash{TR}},@{$article_hash{IR}},
                      @{$article_hash{WP}},@{$article_hash{PW}},@{$article_hash{YR}},
                      @{$article_hash{IJ}},@{$article_hash{TX}},$article_hash{SH},$article_hash{UZ},
                      $article_hash{PC},$article_hash{PS},$article_hash{ST},$article_hash{PR},
                      $article_hash{PN})
   {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;
}# end of sub write_article_record
#===============================================================================
sub write_issue_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

   foreach $field($start,$issue_hash{RN},$issue_hash{RT},$issue_hash{IID},$issue_hash{OCR},$issue_hash{AC},
                  $issue_hash{FO},$issue_hash{BA},$issue_hash{IS},$issue_hash{VO},$issue_hash{NE},$issue_hash{JN},
                  $issue_hash{TE},$issue_hash{HT},$issue_hash{IP},$issue_hash{PF},$issue_hash{DA},$issue_hash{YE},$issue_hash{ID},$issue_hash{ZI},
                  $issue_hash{ZJ},$issue_hash{ZK},$issue_hash{IN},$issue_hash{HL},$issue_hash{LB},$issue_hash{CP},
                  $issue_hash{LA},$issue_hash{SH},$issue_hash{UZ})
   {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

}# end of sub write_issue_record
#===============================================================================
sub write_matp_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

    ###Updated by Photon ...
    foreach my $field ($start,$matp_hash{RN},$matp_hash{BA},$matp_hash{RF},$matp_hash{ZZ},$matp_hash{JN},$matp_hash{HT},
                      $matp_hash{ZI},$matp_hash{ZJ},$matp_hash{ZK},$matp_hash{PC},$matp_hash{PS},$matp_hash{ST},
                      $matp_hash{PR},$matp_hash{PN},@{$matp_hash{TX}},$matp_hash{PF},$matp_hash{XZ},@{$matp_hash{VT}},
                      $matp_hash{BU},$matp_hash{LA},$matp_hash{FO},$matp_hash{FQ},@{$matp_hash{IJ}},$matp_hash{PB})    #Removed 'AI, BE, PF' tag as per revised3 spec by Photon
  {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;
}# end of sub write_matp_record
#===============================================================================
sub write_spotlight_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

    foreach my $field ($start,$spotlight_hash{RN},$spotlight_hash{BA},$spotlight_hash{ZT},$spotlight_hash{RF},
                       @{$spotlight_hash{RM}},$spotlight_hash{JN},$spotlight_hash{JJ},$spotlight_hash{UZ},
                       $spotlight_hash{PF})
  {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;
}# end of sub write_spotlight_record
#===============================================================================
sub write_table_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

    foreach my $field ($start,$table_hash{RN},$table_hash{BA},$table_hash{TI},$table_hash{RF},$table_hash{TID},
                       @{$table_hash{TXT}},$table_hash{JN},$table_hash{JJ},$table_hash{UZ},$table_hash{PF})
  {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;
}# end of sub write_table_record
#===============================================================================
sub write_marc_record
{
   my $newrec = '';

   $output_count++; #counter for records in the file, to be put in trailer record...

   foreach my $field ($start,$marc_hash{RN},$marc_hash{FL},$marc_hash{BA},$marc_hash{RF},$marc_hash{ZZ},
                      $marc_hash{JN},$marc_hash{TE},$marc_hash{HT},$marc_hash{VT},$marc_hash{BU},
                      $marc_hash{ID},$marc_hash{ZI},$marc_hash{ZJ},$marc_hash{ZK},$marc_hash{IN},$marc_hash{HL},
                      $marc_hash{LB},$marc_hash{CP},$marc_hash{LA},$marc_hash{PB},
                      $marc_hash{FQ},$marc_hash{PF},$marc_hash{YS},$marc_hash{YE},$marc_hash{UD},
                      $marc_hash{PC},$marc_hash{PS},$marc_hash{PR},$marc_hash{PN}) ## Removed "BE" tag by Photon ..
   
   {
      $field = &make_B_format($field);
      $newrec .= $field;
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;
}# end of sub write_marc_record
#===============================================================================
sub write_page_record
{
   my $newrec = '';

   $output_count++; # counter for records in the file, to be put in trailer record...

	#Updated by photon 11-11-2008 [dd-mm-yyyy]
	if($page_hash{PI} ne ""){
 		(my $te) = $page_hash{PID} =~ m:PID (.*):i;
		if(exists $hash_pid_pa{$te})
		{
			$page_hash{PI} =~ s/pg\. (.*?)\;/pg. $hash_pid_pa{$te};/gi if($page_hash{PI} =~ /pg\./i);
			$page_hash{PI} =~ s/;/; pg. $hash_pid_pa{$te};/i if($page_hash{PI} !~ /pg\./i and $page_hash{PI} =~ /;/i);
		}else
		{
			$page_hash{PI} =~ s/ ?pg\. (.*?)\;//i;
		}
	}

   foreach my $field ($start,$page_hash{RN},$page_hash{PG},$page_hash{RT},$page_hash{ZZ},$page_hash{PID},
                      $page_hash{FO},$page_hash{BA},$page_hash{IS},$page_hash{PI},$page_hash{JN},$page_hash{TE},
                      $page_hash{HT},$page_hash{IP},$page_hash{PF},$page_hash{DA},$page_hash{YE},$page_hash{ID},$page_hash{ZI},$page_hash{ZJ},$page_hash{ZK},
                      $page_hash{IN},$page_hash{LB},$page_hash{CP},$page_hash{LA},@{$page_hash{AIF}},$page_hash{UZ},$page_hash{SH},
                      $page_hash{TS},$page_hash{TB},$page_hash{SI},$page_hash{AE})
   {
      $field = &make_B_format($field);
      $newrec .= $field;
	  $pPG = $page_hash{PG};
   }

   print $NCNPOUT $newrec;
   $write_count++;

   return;

}# end of sub write_page_record
#===============================================================================
sub writedummy
{
        my $numdummy = shift(@_);
        my $testpageid;

        for($it = $numdummy;$it >0;$it--)
        {

                $newrec = "";
                $testpageid = $pageid;

                $testpageid =~m:(.*-)(\d{3})$:;
                $testpageid = $1;
                $testpg = sprintf("%03d",$2-$it);
                $testpageid .= $testpg;
                $ppg = "PG  ".$testpg; #the page number for this page record
                $testpg =~s:^0+::g;
                $rn_page = $testpg;
                $rn_article = 0;

                # Note: this was changed, because there are sometimes roman
                #       numerals used in the <pa>...</pa> tag, which causes
                #       the $pi to *sometimes* have a non-numeric value.  Thus
                #       I'm changing this substitution, so that it looks for
                #       anything UP TO a semi-colon (versus LOOKING FOR only
                #       digits, and subbing in the current page value)
                #       thereby allowing roman numerals to be processed
                #       properly.  RTC 02/03/2003

                #$pi =~s:pg. \d+:pg. $testpg:;
                $pi =~s:pg. [^;]+:pg. $pgnum_array[eval($pagepg-$it-1)]:;

                    $rn = get_rn();

                     foreach $field($start,$rn,$ppg,$rt,$zz,$testpageid,$cy,$cp)
                    {
                            $field = &make_B_format($field);
                            $newrec .= $field;
                   }
                    foreach $audience(@ai){
                            $audience = &make_B_format($audience);
                            $newrec .= $audience;
                }
                    foreach $field($fo,$ba,$is,$pi,$jn,$ip,$pf)
                    {
                            $field = &make_B_format($field);
                            $newrec .= $field;
                    }
                    $output_count++; #counter for records in the file, to be put in trailer record.
                print $NCNPOUT $newrec;
                    mprint ("\nWrote dummy page record for page $testpageid");
         }#

}
#===============================================================================
sub write_header_rec
{
   my $header = '<<  '.sprintf("%06d",$file_no).$datestamp.$datestamp;
   $header = &make_B_format($header);
   print $NCNPOUT $header;
}
#===============================================================================
sub write_trailer_rec
{
   $linecount--; #remove the count for the header record

   $trailer = '>>  '.sprintf("%09d",$linecount).sprintf("%09d",$output_count);  #this is not complete, need to count lines
   $trailer = &make_B_format($trailer);
   print $NCNPOUT $trailer;

   $linecount=$output_count=0;
}

#===============================================================================
sub read_article_record
{
   %pi_pgref_hash = ();

            #print "PAGE: +++$page---\n";
            #print "REC: +++$record---\n";
            
   # Record Number
   ($article_hash{RN}) = $record =~m:<\?article zz="(\d+)"\?>:;

   if ($article_hash{RN} !~m:\d{10}:)
   {
      mprint ("\n" . '*** <?article zz="..."?> not present on page: ' . $true_page_id . ' ***');
      exit (44);
   }
   #print "\n rn value:$article_hash{RN}\n";
	
   # Grab base of RN from First Article in the Issue, for use in other RN assignments...
   unless ($first_article_found)
   {
      my $first_article_rn_base;

      if ($dvi_name eq 'STHA')
      {
         ($first_article_rn_base) = $article_hash{RN} =~m:^\d{5}(\d{5})$:;
      }
      else
      {
         ($first_article_rn_base) = $article_hash{RN} =~m:^\d{2}(\d{8})$:;
      }

      # Record Number
      if($dvi_name eq 'NCUP')
      {                                                                                                                                                              
         $issue_hash{RN} = '17' . $first_article_rn_base;
         $marc_hash{RN} =  '18' . $first_article_rn_base;
      }
      elsif ($dvi_name eq 'SASN')
      {
         $issue_hash{RN} = '37' . $first_article_rn_base;
         $marc_hash{RN} =  '38' . $first_article_rn_base;
      }
      elsif ($dvi_name eq 'FTIM')
      {
         $issue_hash{RN} = '39' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'ILN')
      {
         $issue_hash{RN} = '40' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'TLS')
      {
         $issue_hash{RN} = '10' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'ECON')
      {
         $issue_hash{RN} = '03' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'PPNP')
      {
         $issue_hash{RN} = '04' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'LSNR')
      {
         $issue_hash{RN} = '37' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      elsif ($dvi_name eq 'TDA')
      {
         $issue_hash{RN} = '08' . $first_article_rn_base;
         $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      }
      #############################################################
      # MAH 03/02/2012, moved assignment of these 2 RN values for #
      #                 STHA in the subroutine read_issue_record. #
      #############################################################
      #elsif ($dvi_name eq 'STHA')
      #{
      #   $issue_hash{RN} = '04002' . $first_article_rn_base;
      #   $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};
      #}

      $first_article_found = 1;
   }

   # Page ID
   push (@aif_multiple, $record =~m:<pi[^>]*>(.*?)</pi>:g);
   #@{$article_dummy{PID}}=@aif_multiple;
#   $article_hash{PID} = shift(@aif_multiple);
   $article_hash{PID} = $true_page_id;

   # Page ID / Article Sequential Number
   ($article_hash{SE}) = $record =~m:<id>.*?-(\d{3})</id>:;
	
	# Done for dummy process....
	($article_hash{pg_dummy}) = $record =~m:<pi\spgref=\".*\">.*?-(\d{4})</pi>:;

   # Record Type
   $article_hash{RT} = 'ARTI';

   # Database Flag
   $article_hash{ZZ} = 'ARTI';

   # Added for Economist...
   if ((my $table_ID, my $table_title) = $record =~m:<calsTableInfo\s+tableID="([^"]+)"[^>]*>([^<]+)</calsTableInfo>:)
   {
      $article_hash{XT} = $table_title . '|' . $table_ID;
   }

   unless ($dvi_name eq 'TLS' || $dvi_name eq 'ECON')
   {
      # (Start) Column Information
      ($article_hash{SC}) = $record =~m:<sc>(.*?)</sc>:;

      # OCR Relevance / OCR Level of Confidence
      ($article_hash{REL}, $article_hash{OCR}) = $record =~m:<ocr\srelevant="(.*?)">(.*?)</ocr>:;

      $article_hash{OCR}=~s#^0$##;     #Updated by Photon
   
      # Save the OCR value from each article, for use in calculating the average OCR value for the issue...
      push (@ocr_values, $article_hash{OCR});

      # Uppercase first letter of Relevance...
      $article_hash{REL} = "\U$article_hash{REL}";
   
      if( $article_hash{OCR} eq "")
      {
        $article_hash{REL}="";
      }
   }

   # Content Index Terms
   push (@{$article_hash{AC}}, 'P');

   # Publication Format
   $article_hash{FO} = $issue_hash{FO};

   # Record Creation Date
   $article_hash{RD} = $datestamp;

   # Publication Year  ##### Updated by Photon.......
   ($article_hash{PY}) = $issue_hash{PF} =~m:^(\d{4}):;    #Updated by Photon

   # Mcode
   $article_hash{BA} = $issue_hash{BA};

   # Source Issue Number
   $article_hash{IS} = $issue_hash{IS};

   # Article Page (Source Page Label) -- Only used in $article_hash{PI}...
   #(my $temp_PA) = $record =~m:<pa>(.*?)</pa>:;

#	## Updated by Photon - 07-10-2008 [DD-MM-YYYY]
#	my $temp_PA;
#	if(scalar(@temp_PA) == 0)
#	{
#		(@temp_PA) = $record =~ m/<pa>(.*?)<\/pa>/g;
#		print STDERR "\n first pa value:@temp_PA\n";
#		#$temp_PA = $temp_PA[-1];
#	}#else{
#		$temp_PA = $temp_PA[-1];
#		(@temp_PA) = $record =~ m/<pa>(.*?)<\/pa>/g if($record =~ /<pa>/si);
#		#print "\n current pa value:$temp_PA";
#		#print "\n next pa value:@temp_PA";
#	#}
#	$temp_PA =~ s/\[|\]//gi;

   # Publication Information, MAH 05/17/06 made change to PI based on spec change
   #$article_hash{PI} = $issue_hash{DA} . '; pg. ' . $temp_PA . '; Issue ' . $issue_hash{IS};
   $article_hash{PI} = $issue_hash{DA};
#   if ($temp_PA ne "")

#print STDERR "ARTICLE PID: $article_hash{PID}\n";
#print STDERR "TRUE PAGE ID: $true_page_id\n";

   if (exists $hash_pid_pa{$article_hash{PID}})
   {
#      $article_hash{PI} .= '; pg. ' . $temp_PA;
      $article_hash{PI} .= '; pg. ' . $hash_pid_pa{$article_hash{PID}};
   }
   if ($article_hash{IS} ne "")
   {
      if ($dvi_name eq 'FTIM')
      {
	     $article_hash{PI} .= '; Edition ' . $issue_hash{IS};
      }
      else
      {	   
	     $article_hash{PI} .= '; Issue ' . $issue_hash{IS};
      }
   }

   # Publication Date for Display
   $article_hash{DA} = $issue_hash{DA};
   
   # Journal Name
   $article_hash{JN} = $issue_hash{JN};

   # Full Title
   $article_hash{TE} = $issue_hash{TE};

   # Short Title
   $article_hash{HT} = $issue_hash{HT};  #Code added per revised4 spec by Photon

   # Fixed Publication Date (YYYYMMDD format)
   $article_hash{PF} = $issue_hash{PF};

   # Ending Date of Coverage (in YYYYMMDD format)
   $article_hash{YE} = $issue_hash{YE};

   # Newspaper ID
   $article_hash{ID} = $issue_hash{ID};

   # Collection ID Number (MARC Record Number)
   $article_hash{ZI} = $issue_hash{ZI};

   # LCCN# (aka Secondary Collection ID Number)
   $article_hash{ZJ} = $issue_hash{ZJ};

   # Collection ID Number (ESTC Number)
   $article_hash{ZK} = $issue_hash{ZK};  #Code added per revised4 spec by Photon
   
   # Source Holding Library
   $article_hash{IN} = $issue_hash{IN};

   # Shelfmark
   ($article_hash{HL}) = $issue_hash{HL};

   # Shelfmark
   $article_hash{LB} = $issue_hash{LB};  #Updated by Photon

   # Copyright Statement
   $article_hash{CP} = $issue_hash{CP};  #Updated by Photon

   #Language
   $article_hash{LA} = $issue_hash{LA};  #Updated by Photon

   #Module
   $article_hash{SH} = $issue_hash{SH};

   # Article Identifier
   ($article_hash{ZX}) = $record =~m:<id>(.*?)</id>:;

   # Journal Name (for search)
   $article_hash{JJ} = $mcode_hash{$article_hash{BA}}{JN};

   # Word Count (see text-processing function)...

   # Page Label
   #($article_hash{PA}) = $record =~m:<pa>(.*?)</pa>:;
   if (exists $hash_pid_pa{$article_hash{PID}})
   {
      ($article_hash{PA}) = $hash_pid_pa{$article_hash{PID}};
   }
   
   # Page Information
   # Populated in sub conv_NCNP

   # Starting Page Number
   #($article_hash{PG}) = $record =~m:<pa>(.*?)</pa>:;
   if (exists $hash_pid_pa{$article_hash{PID}})
   {
      ($article_hash{PG}) = $hash_pid_pa{$article_hash{PID}};
   }

   # Total Pages for current available document
   ($article_hash{TP}) = $record =~m:<pc>(.*?)</pc>:;

   # Content Type (Generic Section Description)
   (@{$article_hash{CT}}) = $record =~m:<ct>(.*?)</ct>:g; ###Updated by Photon

   foreach my $single_ct(@{$article_hash{CT}})
   {
      $single_ct =~ s/(\s)(&amp;|&)(\s)/$1and$3/g;

      if(exists($ng_hash{$single_ct}))
      {
         # push(@{$article_hash{NG}}, $ng_hash{$single_ct});
      	 $article_hash{NG} = $ng_hash{$single_ct};
         $article_hash{NG}=~s#\n$##;
      }
   }

   
   if ($dvi_name eq 'FTIM' || $dvi_name eq 'TLS')
   {
      # Article Series Title
      ($article_hash{AE}) = $record =~m:<sectiontype>(.*?)</sectiontype>:;

      # Save the AE value for later output in the Page record (old DTD/method)...
      if ($dvi_name eq 'TLS')
      {
         $AE_hash{$article_hash{PID}} = $article_hash{AE} if ($article_hash{AE} ne "");

         #print STDERR "XX: The AE_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_hash ), "\n";
      }

   }
   # This value is populated earlier from the <pageid> tag, instead of <sectiontype>...
   elsif ($dvi_name eq 'ILN' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
   {
      # Supplement Title
      ($article_hash{AE}) = $AE_hash{$article_hash{PID}} if (exists $AE_hash{$article_hash{PID}});
   }


   # Image Type
#   (@{$article_hash{IL_type}}) = $record =~m:<il [^>]*type=\"(.*?)\":gi;
   while ($record =~m:<il\s[^>]*type=\"(.*?)\":gi)
   {
      $article_hash{IL_type}{$1} = '';
   }


#   foreach my $single_il(@{$article_hash{IL_type}})
   foreach my $single_il(sort (keys (%{$article_hash{IL_type}})))
   {
      $single_ct =~ s/(\s)(&amp;|&)(\s)/$1and$3/g;

      if(exists($il_hash{$single_il}))
      {
         push(@{$article_hash{IL}}, $il_hash{$single_il});
      }
   }

   # Image Indicator
#   if ($record=~m:<il [^>]*type=\"(.*?)\":i)
#   if (@{$article_hash{IL_type}})
   if (keys (%{$article_hash{IL_type}}))
   {
      $article_hash{IY} = 'Yes';
   }

   # Content Index Terms (continued...) 
# if ($record=~m:<il [^>]*type=\"(.*?)\":i)
#   if (@{$article_hash{IL_type}})
   if (keys (%{$article_hash{IL_type}}))
   {
      push(@{$article_hash{AC}}, 'I')
   }
     
   # Color Image Indicator
   ($article_hash{CL}) = $record =~m:<il\s[^>]*colorimage\s*=\s*\"(yes)\":i;

   # Image Caption
   if ($dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
   {
      while ($record =~m#<il\s([^>]+>)(?:([^<]*)</il>)?#g)
      {
         my $il_attribs = $1;
         my $il_caption = $2;

         if ($il_caption =~m:\S:)
         {
            push (@{$article_hash{IC}}, $il_caption);
         
            if (length($il_caption) > 100)
            {
               #mprint ("BEFORE: $il_caption");

               # Grab 101 characters, and then chop off from the last space to the end of the trunc caption...
               (my $trunc_caption) = $il_caption =~m:^(.{101}):;
               $trunc_caption =~s: [^ ]*$::;
               $il_caption = $trunc_caption.'&hellip;';

               #mprint ("AFTER: $il_caption");
	    }
	 }
         # If the caption doesn't contain any text, set it to a default value...
         else
         {
            $il_caption = 'No caption available';
	 }

         # Licensed Image Details for Order Fulfillment
         if ($dvi_name eq 'ILN' || $dvi_name eq 'PPNP')
#         if ($dvi_name eq 'ILN' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR')
         {
            (my $il_type) = $il_attribs =~m:type\s*=\s*"([^"]*)":;
            (my $il_dbid) = $il_attribs =~m:dbid\s*=\s*"([^"]*)":;
            (my $il_clipimgfile) = $il_attribs =~m:clipimgfile\s*=\s*"([^"]*)":;
      
            # dbid|caption (truncated to 100 characters*)|type|clipimgfile
            push (@{$article_hash{OI}}, join('|', $il_dbid, $il_caption, $il_type, $il_clipimgfile));
         }
      }
   }
   
   # Clipped Article Image
   while ($record =~m:(<ci.*?</ci>):g)
   {
      my $temp_ci = $1;
      push (@{$article_hash{CI}}, $temp_ci);
   }

   # Day of the Week
   $article_hash{DW} = $issue_hash{DW};

   # Abbreviated Day of the Week (first three letters of DW)
   ($article_hash{ED}) = $article_hash{DW} =~m:^(\w{3}):;

   if ($dvi_name eq 'FTIM')
   {
      # Supplement Title
      ($article_hash{TS}) = $record =~m:<supptitle>(.*?)</supptitle>:;

      # Supplement Subtitle
      ($article_hash{TB}) = $record =~m:<suppsubtitle>(.*?)</suppsubtitle>:;
   }
   elsif ($dvi_name eq 'ILN' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'STHA')
   {
      # Supplement/Special Issue Indicator
      ($article_hash{SI}) = $SI_hash{$article_hash{PID}} if (exists $SI_hash{$article_hash{PID}});

      # Supplement Title
      ($article_hash{TS}) = $TS_hash{$article_hash{PID}} if (exists $TS_hash{$article_hash{PID}});

      # Supplement Subtitle
      ($article_hash{TB}) = $TB_hash{$article_hash{PID}} if (exists $TB_hash{$article_hash{PID}});
   }


   # Article Title
   ($article_hash{TI}) = $record =~m:<ti>(.*?)</ti>:;

   if ($article_hash{TI} eq "")                    #Updated by Photon
   {
	    $article_hash{TI} = $article_hash{NG};
   }

   # Clean/fix entities for TI field early, similar to TX ...
   $article_hash{TI} = prep_XML_entities(clean($article_hash{TI}));

   # Truncate the title if it's longer than 375 characters...
   if (length($article_hash{TI}) > 375)
   {
#      mprint ("BEFORE: $article_hash{TI}");

      # Grab 376 characters, and then chop off from the last space to the end of the trunc title...
      (my $trunc_title) = $article_hash{TI} =~m:^(.{376}):;
      $trunc_title =~s: [^ ]*$::;
      $article_hash{TI} = $trunc_title.$nak.'&hellip;'.$syn;

#      mprint ("AFTER: $article_hash{TI}");
   }
   $article_hash{TI} =~s:\.$::;
  					#Updated by Photon

   # Article Subtitle
   (@{$article_hash{TA}}) = $record =~m:<ta>(.*?)</ta>:g;

   # Author Name Composed
   (@{$article_hash{AU}}) = $record =~m:<au>(.*?)</au>:g;

   unless ($dvi_name eq 'ECON')
   {
      # Non-personal Author Name (Newspaper or Organization)
      (@{$article_hash{UN}}) = $record =~m:<altSource>(.*?)</altSource>:g;
   }
   
   $article_hash{UZ} = $issue_hash{UZ};
 
   # Updated by photon 13-10-2008 [dd-mm-yyyy]
   # Populate of author informations
   if($record =~ /<detailed_au>/si)
   {
      (my @au_info) = $record =~m:<detailed_au>(.*?)</detailed_au>:sgi;
      foreach my $au_info (@au_info)
      {
         # Count authors
         $author_count++;
         # Delete newline, tabs, multiple spaces, first space, and last spaces.
         $au_info =~ s/\n|\t//gi;
         $au_info =~ s/\s+/ /gi;
         $au_info =~ s/^\s*|\s*$//gi;
         
         # Extract all names from author content
         my($firstname) = $au_info =~ m:<first>\s*(.*?)\s*</first>:i;
         my($middlename) = $au_info =~ m:<middle>\s*(.*?)\s*</middle>:i;
         my($lastname) = $au_info =~ m:<last>\s*(.*?)\s*</last>:i;
         my($prefix) = $au_info =~ m:<prefix>\s*(.*?)\s*</prefix>:i;
         my($suffix) = $au_info =~ m:<suffix>\s*(.*?),?\s*</suffix>:i;
   
         # Composed author names
         my $composed_author;
         $composed_author .= $prefix if($prefix ne "");
         $composed_author .= " ".$firstname if($firstname ne "");
         $composed_author .= " ".$middlename if($middlename ne "");
         $composed_author .= " ".$lastname if($lastname ne "");
         $composed_author .= ", ".$suffix if($suffix ne "");
         $composed_author =~ s/^\s*|\s*$//g;
         $composed_author =~ s/\,\s*$//g;

         # Reversed author names
         my  $reversed_author;
         $reversed_author .= $lastname."," if($lastname ne "");
         $reversed_author .= " ".$prefix if($prefix ne "");
         $reversed_author .= " ".$firstname if($firstname ne "");
         $reversed_author .= " ".$middlename if($middlename ne "");
         $reversed_author .= ", ".$suffix if($suffix ne "");
         $reversed_author =~ s/^\s*|\s*$//g;
         $reversed_author =~ s/\,\s*$//g;
         
         # Reversed author names (for Sorting and Browse)
         my  $reversed_author_for_sort;
         $reversed_author_for_sort .= $lastname."," if($lastname ne "");
         $reversed_author_for_sort .= " ".$firstname if($firstname ne "");
         $reversed_author_for_sort .= " ".$middlename if($middlename ne "");
         $reversed_author_for_sort =~ s/^\s*|\s*$//g;
         $reversed_author_for_sort =~ s/\,\s*$//g;
         
         
         # Adding authors to article hash
         #print "\n\n composed author:$composed_author------------";
         #print "\n\n reversed author:$reversed_author-------------";

         if ($dvi_name eq 'TLS' && $composed_author =~m:\(AKA\):)
         {
            # Removed the '(AKA)' from the name...
            $composed_author =~s: *\(AKA\)::;

            # Variant Contributor Name
            push (@{$article_hash{VN}}, $composed_author);
         }
         else
         {
            # Contributor (Article Author) Name First-Last
            push @{$article_hash{AU}}, $composed_author;

            # Contributor (Article Author) Name Reversed
            push @{$article_hash{UA}}, $reversed_author;

            if ($dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'STHA')
            {
               # Author Name Reversed (for sorting and browse)
               push @{$article_hash{AS}}, $reversed_author_for_sort;
            }
         }
      }
   }

   # Code added 9/14/2011 by RTC...
   if ($dvi_name eq 'TDA' || $dvi_name eq 'STHA')
   {
      if($record =~ /<au_composed>/si)
      {
         (my @au_info) = $record =~m:<au_composed>(.*?)</au_composed>:sgi;
         foreach my $au_info (@au_info)
         {
            # Count authors
            $author_count++;
            # Delete newline, tabs, multiple spaces, first space, and last spaces.
            $au_info =~ s/\n|\t//gi;
            $au_info =~ s/\s+/ /gi;
            $au_info =~ s/^\s*|\s*$//gi;

            # Contributor (Article Author) Name First-Last
            push @{$article_hash{AU}}, $au_info;
         }
      }
   }
   
   # Code added 4/9/2010 by RTC...
   if ($dvi_name eq 'TLS')
   {
      my %contrib_hash = ();
      (my @work_info) = $record =~m:<work>(.*?)</work>:sgi;

      # Process the first work separately, for the FW tag only, but only if there is at least one <work> on the page...
      if (scalar(@work_info))
      {
         (my $nwtitle) = $work_info[0] =~m:<nwtitle>(.*?)</nwtitle>:;
         (my $nwauthor) = $work_info[0] =~m:<nwauthor>(.*?)</nwauthor>:;
      
#         $article_hash{FW} = $nwtitle . ' by ' . $nwauthor;
         $article_hash{FW} = $nwtitle if ($nwtitle =~m:\S:);
         $article_hash{FW} .= ' by ' . $nwauthor if ($article_hash{FW} =~m:\S: && $nwauthor =~m:\S:);
      }

      foreach my $work (@work_info)
      {
         (my $nwtitle) = $work =~m:<nwtitle>(.*?)</nwtitle>:;
         (my $nwauthor) = $work =~m:<nwauthor>(.*?)</nwauthor>:;

         push (@{$article_hash{WR}}, $nwtitle);

         $nwauthor =~s:&apos;:':g;

         (my @nwauthors_array) = split(/;\s/, $nwauthor);

         foreach my $contrib (@nwauthors_array)
         {
            $contrib =~s:':&apos;:g;

            if ($contrib =~m:\([^)]*\bauthor\b:i || $contrib !~m:\(:)
            {
               #print STDERR "Author found!: $contrib\n";
               my $contrib_temp = $contrib;

               $contrib_temp =~s:\([^)]*\bauthor\b[^)]*\)::;
               #print STDERR "Author fixed: $contrib_temp\n";

               if (!exists($contrib_hash{WA}{$contrib_temp}))
               {
                  $contrib_hash{WA}{$contrib_temp} = '';
                  push (@{$article_hash{WA}}, $contrib_temp);
               }
            }
            if ($contrib =~m:\([^)]*\bed[\w\.]*\b:i)
            {
               #print STDERR "Editor found!: $contrib\n";
               my $contrib_temp = $contrib;

               $contrib_temp =~s:\([^)]*\bed[\w\.]*\b[^)]*\)::i;
               #print STDERR "Editor fixed: $contrib_temp\n";

               if (!exists($contrib_hash{WE}{$contrib_temp}))
               {
                  $contrib_hash{WE}{$contrib_temp} = '';
                  push (@{$article_hash{WE}}, $contrib_temp);
               }
            }
            if ($contrib =~m:\([^)]*\btrans[\w\.]*\b:i)
            {
               #print STDERR "Translator found!: $contrib\n";
               my $contrib_temp = $contrib;

               $contrib_temp =~s:\([^)]*\btrans[\w\.]*\b[^)]*\)::i;
               #print STDERR "Translator fixed: $contrib_temp\n";

               if (!exists($contrib_hash{TR}{$contrib_temp}))
               {
                  $contrib_hash{TR}{$contrib_temp} = '';
                  push (@{$article_hash{TR}}, $contrib_temp);
               }
            }
            if ($contrib =~m:\([^)]*\billus[\w\.]*\b:i)
            {
               #print STDERR "Illustrator found!: $contrib\n";
               my $contrib_temp = $contrib;

               $contrib_temp =~s:\([^)]*\billus[\w\.]*\b[^)]*\)::i;
               #print STDERR "Illustrator fixed: $contrib_temp\n";

               if (!exists($contrib_hash{IR}{$contrib_temp}))
               {
                  $contrib_hash{IR}{$contrib_temp} = '';
                  push (@{$article_hash{IR}}, $contrib_temp);
               }
            }
         }


         (my @publisher) = $work =~m:<publisher>(.*?)</publisher>:g;
         push (@{$article_hash{WP}}, @publisher);

         (my @placepub) = $work =~m:<placepub>(.*?)</placepub>:g;
         push (@{$article_hash{PW}}, @placepub);

         (my @datepub) = $work =~m:<datepub>(.*?)</datepub>:g;
         push (@{$article_hash{YR}}, @datepub);

      }
   }

   ####################################################################

   # Page Illustration -- used to build PIF
   while ($record =~m:<pi.*?pgref="([^"]*)">(.*?)</pi>:sg)
   {
      $pi_pgref_hash{$1} = $2;
   }

   #print "\n prev num:$prev_page_number";
   #print "\n artical hash:$article_hash{PID}";
   # Save RN of First Article on the Page, for use in $page_hash{RN}...
#   print STDERR "\n A: prev:$prev_page_number \t True page ID:$true_page_id\n\n";

   my $prev_num = 0;
   if ($prev_page_number)
   {
      ($prev_num) = $prev_page_number =~m:.*-(\d+)$:;
   }
   
#   (my $article_num) = $article_hash{PID} =~m:.*-(\d+)$:;
    my $article_num = $true_page_num;
	
   #print STDERR ("B: prev_num: $prev_num\narticle_num: $article_num\n\n");
   if ($prev_num > $article_num)
   {
#      mprint ("***II. Non-sequential page ID encountered: prev_PID=$prev_page_number, curr_PID=$article_hash{PID} ***\n");
      mprint ("***II. Non-sequential page ID encountered: prev_PID=$prev_page_number, curr_PID=$true_page_id ***\n");
   }

   while ($prev_page_number ne $article_hash{PID} && $prev_num <= $article_num)
   {
        #my $curr_page_number = $article_hash{PID};
          my $curr_page_number = $true_page_id;
      
#     print STDERR "C: curr_page_number = $curr_page_number\n\n";

      # "Fake out" the program, if there are no articles on page 1, so that a record is created for page 1 upto the current page...
      if ($prev_num == 0 && $article_num > 1)
      {
         for (my $i=1; $i<$article_num-1; $i++)
         {
            #print STDERR "\nBEGIN: article_num:$true_page_id and prev page number:$prev_page_number" .
       #             "\nprev_num is $i and article num is $article_num";

            $prev_page_number = $curr_page_number;
            $prev_page_number =~s:$article_num$:sprintf("%04d", $i):e;

#            print STDERR "\nNEW PAGE ID: $prev_page_number\n\n";

            # Fake out the converter, so that continuation page records get the proper PID...
            $article_hash{PID} = $prev_page_number;

            ($page_rn_base) = $article_hash{RN} =~m:^\d{2}(\d{8})$:;
            &create_page_record();

            mprint ('+++Writing record for page: '.$prev_page_number."\n");
#            print STDERR '+++Writing record for page: '.$prev_page_number."\n\n";
            &add_format_b_tags('page_hash');
            &write_page_record();
            %page_hash = ();
         }

         # Assign the actual Page ID back to $article_hash{PID}...
         $article_hash{PID} = $curr_page_number;

#         print STDERR "BEFORE prev_page_number: $prev_page_number\n\n";

         $prev_page_number = $curr_page_number;
         $prev_page_number =~s:$article_num$:sprintf("%04d", $article_num - 1):e;

#         print STDERR "AFTER prev_page_number: $prev_page_number\n\n";

         # Fake out the converter, so that continuation page records get the proper PID...
         $article_hash{PID} = $prev_page_number;

         # Create the last dummy page record, but don't print it out (the next block of code will)...
	 &create_page_record();
      }

      # Write out a page record if the page number changes, but only if it's not the first page...
      if ($prev_page_number)
      {
#	print STDERR "\n D: prev: $prev_page_number\ttrue page ID: $true_page_id\tcurr_page_number: $curr_page_number\n";
		  #print "\n if length:".scalar(@{$page_hash{AIF}}). "\n";

         # Populate the AE, SI, TS and TB tags from the stored values at the page-level, if present...
         # Need to know current page (use $prev_num or $curr_num)

         #print STDERR "3: The AE_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_hash ), "\n";

         if (exists($AE_hash{$prev_page_number}))# && !(exists($AE_written_hash{$prev_page_number})))
         {
            ($page_hash{AE}) = $AE_hash{$prev_page_number};
            delete $AE_hash{$prev_page_number};
#            $AE_written_hash{$prev_page_number} = '';
         }
         #print STDERR "3: The AE_written_hash contents are as follows: ", Data::Dumper::Dumper( \%AE_written_hash ), "\n";

         #print STDERR "3: The SI_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_hash ), "\n";

         if (exists($SI_hash{$prev_page_number}))# && !(exists($SI_written_hash{$prev_page_number})))
         {
            ($page_hash{SI}) = $SI_hash{$prev_page_number};
            delete $SI_hash{$prev_page_number};
#            $SI_written_hash{$prev_page_number} = '';
         }
         #print STDERR "3: The SI_written_hash contents are as follows: ", Data::Dumper::Dumper( \%SI_written_hash ), "\n";

         #print STDERR "3: The TB_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_hash ), "\n";

         if (exists($TB_hash{$prev_page_number}))# && !(exists($TB_written_hash{$prev_page_number})))
         {
            ($page_hash{TB}) = $TB_hash{$prev_page_number};
            delete $TB_hash{$prev_page_number};
#            $TB_written_hash{$prev_page_number} = '';
         }
         #print STDERR "3: The TB_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TB_written_hash ), "\n";

         if (exists($TS_hash{$prev_page_number}))# && !(exists($TS_written_hash{$prev_page_number})))
         {
            ($page_hash{TS}) = $TS_hash{$prev_page_number};
            delete $TS_hash{$prev_page_number};
#            $TS_written_hash{$prev_page_number} = '';
         }
         #print STDERR "3: The TS_written_hash contents are as follows: ", Data::Dumper::Dumper( \%TS_written_hash ), "\n";
     

         mprint ('+++Writing record for page: '.$prev_page_number."\n");
#         print STDERR '+++Writing record for page: '.$prev_page_number."\n\n";

         &add_format_b_tags('page_hash');
         &write_page_record();
         %page_hash = ();
         # Increment the prev_page_number, by incrementing just the page ID at the end of the value...
         (my $prev_id, $prev_num) = $prev_page_number =~m:^(.*)-(\d+)$:;
         $next_num = $prev_num + 1;
         $prev_page_number = $prev_id . "-".sprintf("%04d", $next_num);
		 # If the page numbers still aren't equal, we need to populate the AIF information...
         #mprint ("NEW prev_page_number: $prev_page_number\narticle_hash{PID}: $article_hash{PID}\n");
		 #print "\n prev:$prev_page_number \t article hash $article_hash{PID}";			 

         if ($prev_page_number ne $article_hash{PID})
         {
            #print "\nnext_num: $next_num";
            if (@AIF_array)
            {
			   for (my $i=0; $i<=$#AIF_array; $i++)
			   {
				  if ($AIF_array[$i] =~ m:pgref="$next_num":ms)
				  {
					  #mprint ("Found AIF data: $AIF_array[$i]\n");
					  push (@{$page_hash{AIF}}, $AIF_array[$i]);
					  $AIF_array[$i] = undef;
				  }
			   }
            }
         }

         # Fake out the converter, so that continuation page records get the proper PID...
         $article_hash{PID} = $prev_page_number;
      }
		
      ($page_rn_base) = $article_hash{RN} =~m:^\d{2}(\d{8})$:;
      &create_page_record();

      if ($prev_page_number)
      {
         # Assign the actual Page ID back to $article_hash{PID}...
         $article_hash{PID} = $curr_page_number;
      }
      else
      {
         #$prev_page_number = $article_hash{PID};
         $prev_page_number = $true_page_id;

         # If there wasn't a previous page, there's no reason to print out any pages yet, so skip to the end...
         last;
      }
   }

   #print STDERR "a) article_hash{PID} = $article_hash{PID}\n";

      if ($prev_num > $article_num)
   {
#	  $article_hash{PID} = shift(@aif_multiple);
      $article_hash{PID} = $true_page_id;
   }

   #print STDERR "b) article_hash{PID} = $article_hash{PID}\n";

   ($text) = ($record =~m:<text>(.*?)</text>:si);        #full text, must be cleaned and split
   # Text processing goes here...
   if ($text =~m:\S:)
   {
      &divide_text();

      &conv_NCNP();
   }

   
   # Place of Publication - City
   $article_hash{PC} = $mcode_hash{$article_hash{BA}}{PC};

   # Place of Publication - State
   $article_hash{PS} = $mcode_hash{$article_hash{BA}}{PS};

   # Place of Publication - State Code
   $article_hash{ST} = $mcode_hash{$article_hash{BA}}{ST};

   # Place of Publication - Country                     #Updated by Photon
   $article_hash{PN} = $mcode_hash{$article_hash{BA}}{PN};
   
   # Place of Publication - Region                      #Updated by Photon
   $article_hash{PR} = $mcode_hash{$article_hash{BA}}{PR};
   
   # Populate marcname from XML....
   # (@{$issue_hash{BU}}) = $record =~ m:<marcName>(.*?)</marcName>:g;

}# end of sub read_article_record
#===============================================================================
sub divide_text
{
        @text_cr=@text_title=@text_preamble=();

        # Text preamble - for persistent headings - NOW MULTIPLE
        (@text_preamble) = $text =~m:(<text\.preamble>.*?</text\.preamble>):sg;

        # Text title - now MULTIPLE
        (@text_title) = $text =~m:(<text\.title>.*?</text\.title>):sg;

        # Text clip rectangle - body of text
        (@text_cr) = $text =~m:(<text\.cr>.*?</text\.cr>):sg;

}# end of sub divide_text
#===============================================================================
sub read_issue_record
{
        $rn_year=$rn_month=$rn_day="";
        $mnth="";


        # Record Type
        $issue_hash{RT} = 'I';

        # Issue Identifier
        ($temp_issue_record_number) = $record =~m:<id>(.*?)</id>:;
        $issue_hash{IID} = $temp_issue_record_number;

        # Record Number
        # Assigned in sub read_article_record, except for project STHA...
        # MAH 03/02/2012
        if ($dvi_name eq 'STHA')
        {
           if (exists $DVI_issue_num_hash{$temp_issue_record_number})
           {
              $issue_hash{RN} = '04002' . sprintf ("%05d", $DVI_issue_num_hash{$temp_issue_record_number});
              $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};

              $DVI_issue_existing_num_ctr++;
              print "IN sub read_issue_record, DVI_issue_existing_num_ctr = $DVI_issue_existing_num_ctr\n";
           }
           #####################################################################
           # Issue ID has never been assigned a record number, therefore       #
           # increment the value of the last issue number used.  Number was    #
           # retrieved in subroutine read_issue_last_num_file.  Also, add the  #
           # RN value to the Issue ID in the hash, so it is written to the     #
           # file when this conversion is complete.                            #
           #####################################################################
           else
           {
              $DVI_last_issue_num_new++;  #retrieved from file
              print "IN sub read_issue_record, DVI_last_issue_num_new = $DVI_last_issue_num_new\n";

              $DVI_issue_num_hash{$temp_issue_record_number} = sprintf ("%05d", $DVI_last_issue_num_new);

              $issue_hash{RN} = '04002' . sprintf ("%05d", $DVI_issue_num_hash{$temp_issue_record_number});
              $marc_hash{RN} =  $mcode_hash{$issue_hash{BA}}{MARC_RN};

              $DVI_issue_new_num_ctr++;
              print "IN sub read_issue_record, DVI_issue_new_num_ctr = $DVI_issue_new_num_ctr\n";
           }

        } #end if dvi_name eq STHA


        # OCR Level of Confidence
        # Calculated elsewhere...

        # Content Index Terms
        $issue_hash{AC} = "I";

    ######## Mcode value populated from Lookup table by Photon.....
    
           (my $file_name) = $record =~ m:<newspaperID>(.*?)</newspaperID>:;
           #$file_name = $file_name.".xml";

           foreach $key (keys %xml_mcode)
           {
             if($key eq $file_name)
             {
              ($issue_hash{BA}) = $xml_mcode{$key};

              last;
             }
           }

        ###Dummy usage of Tag...........
        ($issue_hash{PID}) = $record =~m:<pageid[^>]*>(.*?)</pageid>:;
        push(@{$issue_hash{AI}},$mcode_hash{$issue_hash{BA}}{AI}) ; # #Updated by Photon for AI here since we are using the value of BA
        $issue_hash{FO}= $mcode_hash{$issue_hash{BA}}{FO};  # #Updated by Photon for FO here since we are using the value of BA

        #Source Issue Number
        ($issue_hash{IS}) = $record =~m:<is>(.*?)</is>:;

        #Source Volume Number
        ($issue_hash{VO}) = $record =~m:<volNum>(.*?)</volNum>:;

        unless ($dvi_name eq 'ECON' || $dvi_name eq 'PPNP')
        {
           #Newspaper Edition (Morning, Afternoon, Evening, etc.)
           ($issue_hash{NE}) = $record =~m:<ed>(.*?)</ed>:;
        }

        #Journal Name (for display)
        ($issue_hash{JN}) = $mcode_hash{$issue_hash{BA}}{JN} ;         #Updated by Photon
        ($issue_hash{ID_dummy}) = $record =~m:<newspaperID>(.*?)</newspaperID>:;
        ($issue_hash{ID}) = $issue_hash{ID_dummy};


        #Full Title ### Updated for TE tag by Photon....
		 $issue_hash{TE} = $mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID}}{VARIANT_TITLE};

        $issue_hash{HT} = $mcode_hash{$issue_hash{BA}}{HT};            #Updated by Photon

        #Issue Page Count
        ($issue_hash{IP}) = $record =~m:<ip>(.*?)</ip>:;

        #Updated for Fixed Publication Date (YYYYMMDD format) by Photon...
        ($issue_hash{PF}) = $record =~m:<pf>(.*?)</pf>:;

        #Ending date of coversion (in YYYYMMDD format)...
        ($issue_hash{YE}) = $record =~m:<tdate>(.*?)</tdate>:;

        unless ($dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'LSNR')
        {
           # Newspaper ID (aka Document ID #) #### Updated by Photon...
           ($issue_hash{ZI}) = $mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}{ZI};   #Updated by photon

           #LCCN# (aka Secondary Collection ID Number)
           ($issue_hash{ZJ}) = $mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}{ZJ};   #Updated by photon

           #Collection ID Number (ESTC Number)
           ($issue_hash{ZK}) = $mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID_dummy}}{ZK};   #Updated by photon

           #Source Holding Institution
           ($issue_hash{IN}) = $record =~m:<sourceLibrary>(.*?)</sourceLibrary>:;

           #Shelfmark
           ($issue_hash{HL}) = $mcode_hash{$issue_hash{BA}}{HL};  #Code Updated by Photon

           # Source Library Name Code
           #($issue_hash{LB}) = $mcode_hash{$issue_hash{BA}}{LB};  #Code added by Photon
           ($issue_hash{LB}) = $new_id{$file_name}{LB};
        }

        # Copyright Statement
        #$issue_hash{CP} = $mcode_hash{$issue_hash{BA}}{CP};  #Code added by Photon
        $issue_hash{CP} = $new_id{$file_name}{CP};

        $issue_hash{LA} = $mcode_hash{$issue_hash{BA}}{LA};  #Code added per revised6 spec by Photon

        # Module Title
	$issue_hash{SH} = $mcode_hash{$issue_hash{BA}}{SH};

        #Content Set Acronym - Set this dynamically, based on the uppercased version of the value in the OPT file...
        $issue_hash{UZ} = $dvi_name;

        # Publication Date -- Used in $article_hash{PI} and $issue_hash{PI}...
        ($issue_hash{DA}) = $record =~m:<da>(.*?)</da>:;                          #Updated by Photon

        # Day of the Week -- Used only in $article_hash{DW}...
        ($issue_hash{DW}) = $record =~m:<dw>(.*?)</dw>:;                          #Updated by Photon
        $issue_hash{DW} =~s:NotAvailable::i;  #Code added per revised4 spec by Photon

	 #Updated by photon 13-11-2008 [dd-mm-yyyy]
	#(@temp_PA) = $record =~ m/<pa>(.*?)<\/pa>/g;

}# end of sub read_issue_record
#===============================================================================
sub create_matp_record
{
        # Record Number
	$matp_hash{RN} = $mcode_hash{$issue_hash{BA}}{MATP_RN};   ### Dummy tag has been updated by Photon.....

        # Mcode (for PARIS system)
        $matp_hash{BA} = $issue_hash{BA};

        # Record Functional Type
        $matp_hash{RF} = 'Master Publication Metadata Record';

        # Database Flag
        $matp_hash{ZZ} = 'MPUB';

        # Newspaper Title (Master Publication Title from PARIS)
				$matp_hash{JN} = $mcode_hash{$matp_hash{BA}}{JN}; #Updated by Photon

        # Short Title (HT TAg from Lookup Table..)
        $matp_hash{HT} = $issue_hash{HT};    ####  Updated by Photon on 30-Aug..

        # Collection ID Number (MARC Record Number) Updated by Photon####
        $matp_hash{ZI} = $issue_hash{ZI};
        $matp_hash{ZJ} = $issue_hash{ZJ};       ##########Updated By Photon
        $matp_hash{ZK} = $issue_hash{ZK};       ##########Updated By Photon


    		# Populate BU tag from Lookup table by Photon...
		    $matp_hash{BU} = $mcode_hash{$article_hash{BA}}{BU};

        # Place of Publication -- City
        $matp_hash{PC} = $mcode_hash{$matp_hash{BA}}{PC};

        # Place of Publication -- State
        $matp_hash{PS} = $mcode_hash{$matp_hash{BA}}{PS};

        # Place of Publication -- State Code
        $matp_hash{ST} = $mcode_hash{$matp_hash{BA}}{ST};

        # Place of Publication -- Country
        $matp_hash{PN} = $mcode_hash{$matp_hash{BA}}{PN};

        # Place of Publication -- Region
        $matp_hash{PR} = $mcode_hash{$matp_hash{BA}}{PR};
        
        ###MODIFIED BY Photon ########
        
        # Headnote Text
        my $headnote_file = $headnote_dir.$matp_hash{BA}.'.txt';
        if (-f $headnote_file)
        {
           # Open the headnote file...
           open(HEAD,"<$headnote_file") || die "\n***In if for create_matp_record, Error opening headnote file $headnote_file: $!.\n";

           local $/ = "\n";

           push (@{$matp_hash{TX}}, prep_XML_tags('<headnote>'));

           #while (my $head_para = <HEAD>)
           #{
           #   $head_para = prep_XML_tags(prep_XML_entities(clean($head_para)));
           #   push (@{$matp_hash{TX}}, $head_para);
           #}

	   while (my $head_para = <HEAD>)
	   {
	       $head_para =~ s/\<a(.*?)\>/\<a$1 style="external"\>/smg;
	       $head_para = prep_XML_tags(prep_XML_entities(clean($head_para)));
	       $head_para=~s/<LTO.a /<XEB.a /gi;
	       $head_para=~s/<\/LTO.a>/<\/XEB.a>/gi;
	       push (@{$matp_hash{TX}}, $head_para);
	   }

           push (@{$matp_hash{TX}}, prep_XML_tags('</headnote>'));
        }
        else
        {
           #############################################################################
           # MAH 05/12/06 commented out the die statement per discussion with Laura B. #
           # NOTE: If there is no headnote txt file for the mcode don't output         #
           #       a TX tag and continue processing.                                   #
           #############################################################################

           #die "\nIn else for create_matp_record, Error opening headnote file $headnote_file: File doesn't exist!\n"

           mprint("+++No Headnote txt file for mcode $matp_hash{BA}, therefore no TX tag in matp record.");
        }

        # Fixed Publication Date #### Update by Photon ....
        
        $matp_hash{PF} = $issue_hash{PF};

        # Document Title for Sorting the Search Results List ##### Updated by Photon...

          $matp_hash{XZ} = $mcode_hash{$matp_hash{BA}}{XZ};

          ### Variant Title (VT) Populated from Lookup Table.....

		     my $get_BA_VT = $issue_hash{BA};
         open(OPENMETA,"<$metadata_file") || die "\nError opening $metadata_file: $!.\n";
         local $/ = "\n";
         while(my $lookup_line = <OPENMETA>)
         {
           if($lookup_line=~m#$get_BA_VT#)
           {
              (my $mcode, my $title,my $xz_title,my $short_title, my $lccn_id,my $language,my $pubformat,my $frequency,my $variant_title) = split (/[|]/, $lookup_line);  ##updated by Photon...
               push(@{$matp_hash{VT}}, $variant_title ."|".  $lccn_id);
          }
         }
         close(OPENMETA);

         
        ### Reversed Editor Name (BE) Populated from XML file..
 #      @{$matp_hash{BE}} = @{$matp_hash{BU}};  ### New tag added by Photon ..

        ### Newspaper ID (ID) Populated from Lookup Table.....
        $matp_hash{ID} = $mcode_hash{$matp_hash{BA}}{N_ID}; ### New tag added by Photon..

		# Language
		$matp_hash{LA} = $mcode_hash{$matp_hash{BA}}{LA};		###MODIFIED BY Photon

		# Publication Frequency
      	$matp_hash{FQ} = $mcode_hash{$matp_hash{BA}}{FQ};		###MODIFIED BY Photon

       	# Publication Subject Primary
		my @ij_values = split('\|', $mcode_hash{$matp_hash{BA}}{IJ});
	    foreach my $ij_val (@ij_values)
		{
			push (@{$matp_hash{IJ}}, $ij_val);
		}
		
      	# Publication Format
      	$matp_hash{FO} = $mcode_hash{$matp_hash{BA}}{FO};		###MODIFIED BY Photon

		$matp_hash{PB} = $mcode_hash{$matp_hash{BA}}{PB}; #Updated by Photon

}# end of sub create_matp_record
#===============================================================================
sub create_spotlight_record
{
   # Mcode (for PARIS system)
   if ($dvi_name eq "PPNP" || $dvi_name eq 'LSNR')
   {
      #$spotlight_hash{BA} = $xml_mcode{'PPNP0001'};
      $spotlight_hash{BA} = $xml_mcode{$dvi_name.'0001'};
   }
   else
   {
      $spotlight_hash{BA} = $xml_mcode{$dvi_name};
   }

   # Record Number
   $spotlight_hash{RN} = $mcode_hash{$spotlight_hash{BA}}{SPOTLIGHT_RN};

   # Ztag
   $spotlight_hash{ZT} = $mcode_hash{$spotlight_hash{BA}}{ZT};

   # Record Functional Type
   $spotlight_hash{RF} = 'Spotlight Record';

   # Spotlight Information
   if (-f $spotlight_file)
   {
      my $excel = Spreadsheet::ParseExcel::Workbook->Parse($spotlight_file);

      # Manually clean this data, and remove the resulting 'LTO.' namespace...
      $temp_RM = prep_XML_tags(prep_XML_entities(clean('<XRF.spotlightRecord>')));
      $temp_RM =~s:LTO\.::g;

      push (@{$spotlight_hash{RM}}, $temp_RM);

      foreach my $sheet (@{$excel->{Worksheet}})
      {
         next if($sheet->{MaxRow} eq "");

         foreach my $row ($sheet->{MinRow} .. $sheet->{MaxRow})
         {
            $sheet->{MaxCol} ||= $sheet->{MinCol};

            if($row > 0)
            {
               # Skip the row, if it contains field names...
               next if $sheet->{Cells}[$row][1]->{Val} eq 'Year';

               my $temp_RM = '<XRF.spotlightItem>' . "\n";

               $temp_RM .= '<XRF.zz>' . $sheet->{Cells}[$row][9]->{Val}  . '</XRF.zz>' . "\n";

               if ($sheet->{Cells}[$row][7]->{Val} =~m:Issue:i)
               {
                  my $year = $sheet->{Cells}[$row][1]->{Val};
                  my $month_day = $sheet->{Cells}[$row][2]->{Val};

                  $month_day =~s:/::;

                  $temp_RM .= '<XRF.link>' . $spotlight_hash{BA} . '|' . $year . $month_day  . '</XRF.link>' . "\n";
               }

	       my $filename = $sheet->{Cells}[$row][8]->{Val};
               $filename =~s:\.[^\.]*$:-F:;
               $temp_RM .= '<XRF.filename>' . $filename . '</XRF.filename>' . "\n";

               print STDERR "row: $row -- after filename: $filename\n";

               $temp_RM .= '<XRF.description>' . $sheet->{Cells}[$row][4]->{Val} . '</XRF.description>' . "\n";

               print "Cell Value: " . $sheet->{Cells}[$row][5]->{Val} . "\n";

               # NOTE: The ExcelLocalTime is used to determine the day of the week, because the 'dddd' format in ExcelFmt was always returning "Monday"...
               if ($sheet->{Cells}[$row][5]->{Val} =~ m:^[0-9]+$:)
	       {
                  my (@date_time) = ExcelLocaltime($sheet->{Cells}[$row][5]->{Val});
                  $temp_RM .= '<XRF.dateDisplay>' . (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$date_time[6]] . ExcelFmt('"," mmmm dd"," yyyy', $sheet->{Cells}[$row][5]->{Val}) . '</XRF.dateDisplay>' . "\n";
               }
               else
	       {
                  $temp_RM .= '<XRF.dateDisplay>' . $sheet->{Cells}[$row][5]->{Val} . '</XRF.dateDisplay>' . "\n";
               }

               $temp_RM .= '<XRF.navigate>' . $sheet->{Cells}[$row][7]->{Val}  . '</XRF.navigate>';

               $temp_RM .= '</XRF.spotlightItem>' . "\n";

               # Manually clean this data, and remove the resulting 'LTO.' namespace...
               $temp_RM = prep_XML_tags(prep_XML_entities(clean($temp_RM)));
               $temp_RM =~s:LTO\.::g;

               push (@{$spotlight_hash{RM}}, $temp_RM);
            }
         }
      }

      # Manually clean this data, and remove the resulting 'LTO.' namespace...
      $temp_RM = prep_XML_tags(prep_XML_entities(clean('</XRF.spotlightRecord>')));
      $temp_RM =~s:LTO\.::g;

      push (@{$spotlight_hash{RM}}, $temp_RM);

   }
   else
   {
      die "\nIn else for create_spotlight_record, Error opening spotlight file $spotlight_file: File doesn't exist!\n"
   }

   # Journal Name (for display)
   $spotlight_hash{JN} = $mcode_hash{$spotlight_hash{BA}}{JN};

   # Journal Name (for search)
   $spotlight_hash{JJ} = $mcode_hash{$spotlight_hash{BA}}{JN};

   #Content Set Acronym - Set this dynamically, based on the uppercased version of the value in the OPT file...
   $spotlight_hash{UZ} = $dvi_name;

   # Fixed Publication Date (Record Creation Date)
   $spotlight_hash{PF} = $datestamp;
         
}# end of sub create_spotlight_record
#===============================================================================
sub create_table_record
{
   my $table_file = shift(@_);

   $table_hash{TID} = basename($table_file, '.xml');

   # Mcode (for PARIS system)
   if ($dvi_name eq "PPNP" || $dvi_name eq 'LSNR')
   {
      $table_hash{BA} = $xml_mcode{$dvi_name.'0001'};
   }
   else
   {
      $table_hash{BA} = $xml_mcode{$dvi_name};
   }

   # Record Number
   $table_hash{RN} = $table_id_hash{$table_hash{TID}};

   # Record Functional Type
   $table_hash{RF} = 'Table Record';

   # Spotlight Information
   if (-f $table_file)
   {
      # Open the table file...
      open(TABLE,"<$table_file") || die "\n***In if for create_table_record, Error opening table file $table_file: $!.\n";

      # Read in the table row by row...
      local $/ = "</row>";


      # Table Text...
      while (my $table_data = <TABLE>)
      {
         # Table Title
         if ($table_data =~m:<table .*?caption="(.*?)":)
         {
            $table_hash{TI} = $1;
            #print STDERR "Caption found: $table_hash{TI}\n";
         }

         $table_data =~s:<\?xml[^>]*>::;
         $table_data =~s:<!DOCTYPE[^>]*>::;

         $table_data =~s:(<table\s.*?)\s+caption="([^"]+)":$1 title="$2":;
         $table_data =~s:(<table.*?)\s+pos=".*?":$1 border="1":;

         $table_data =~s#<(/?)(table|tbody|td|thead|tr|th)(\s+[^>]+)*>#<$1XHTML.\L$2\E$3>#sgi;

         $table_data =~s#<(/?)(tgroup)(\s*[^>]*)>##sgi;

         $table_data =~s#<colspec(\s*[^>]*)>##sgi;



         # Process each of these row elements with attributes, one at a time...
         while ($table_data =~m#<(?:row)(\s+[^>]+)>#sgi)
         {
            my $orig_row_attribs = $1;
            my $fixed_row_attribs = $orig_row_attribs;
            my $while_pos2 = pos ($table_data);

      #      print STDERR "TAG DATA BEFORE: $table_data\n";

      #      print STDERR "ALL ATTRIBS BEFORE: $orig_row_attribs\n";

            $fixed_row_attribs =~s#\s*rowsep="(.*?)"##si;
            $fixed_row_attribs =~s#\s*valign="(.*?)"# valign="\L$1\E"#si;

#            print STDERR "ALL ATTRIBS AFTER: $fixed_row_attribs\n";

            # Swap the "original" attributes with the "fixed" (well-formed) version...
            $table_data =~s#$orig_row_attribs#$fixed_row_attribs#;

#            print STDERR "TAG DATA AFTER: $table_data\n";

            # If the length the "fixed" attributes is shorter (due to whitespace cleanup, etc.), we need to
            # account for the discrepany; otherwise, the next sequential tag with attributes might get skipped...
            if (length($orig_row_attribs) - length($fixed_row_attribs) > 0)
            {
              $while_pos2 = $while_pos2 - length($orig_row_attribs) + length($fixed_row_attribs);
            }

            pos $table_data = $while_pos2;
         }

         $table_data =~s#<(/?)row(\s*[^>]*)>#<$1XHTML.tr$2>#sgi;     #ALL - 01/30/08

         while ($table_data =~m#<(?:entry)(\s+[^>]+)>#sgi)
         {
            my $orig_entry_attribs = $1;
            my $fixed_entry_attribs = $orig_entry_attribs;
            my $while_pos3 = pos ($table_data);
            my $hold_colspan_value = "";

#            print STDERR "TAG DATA BEFORE: $table_data\n";

#            print STDERR "ALL ATTRIBS BEFORE: $orig_entry_attribs\n";

            $fixed_entry_attribs =~s#\s*colname="(.*?)"# id="$1"#si;
            $fixed_entry_attribs =~s#\s*colsep="(.*?)"##si;
            $fixed_entry_attribs =~s#\s*rowsep="(.*?)"##si;
            $fixed_entry_attribs =~s#\s*char="(.*?)"# char="$1"#si;
            $fixed_entry_attribs =~s#\s*(v?align)="(.*?)"# \L$1\E="\L$2\E"#sig;

            (my $num_rows) = $fixed_entry_attribs =~m#\s*morerows="(.*?)"#si;

            if (defined $num_rows)
            {
               my $tmp_morerows = $num_rows + 1;
               $fixed_entry_attribs =~s#\s*morerows="(.*?)"# rowspan="$tmp_morerows"#si;
            }


            if ($fixed_entry_attribs =~m#\s+namest="[A-Za-z]*(\d+)"*#si &&
                $fixed_entry_attribs =~m#(\s+nameend="[A-Za-z]*(\d+)")*#si)
            {
               (my $start_column) = $fixed_entry_attribs =~m#\s+namest="[A-Za-z]*(\d+)"*#si;
               (my $end_column) = $fixed_entry_attribs =~m#\s+nameend="[A-Za-z]*(\d+)"*#si;

               # When namest, nameend AND colspan are present (in the input) we can't trust the colspan, so remove it...
               $fixed_entry_attribs =~s#\s+colspan="\d+"##si;

               # Use namest and nameend to compute the colspan, which is more reliable...
	       $hold_colspan_value = $end_column - $start_column + 1;
               $fixed_entry_attribs =~s#\s+namest="[A-Za-z]*(\d+)"##si;
               $fixed_entry_attribs =~s#\s+nameend="[A-Za-z]*(\d+)"# colspan="$hold_colspan_value"#si;
	    }
            # If both namest and nameend aren't present, remove the orphan attribute, and report it...
            else
	    {
               mprint ("Orphan namest or nameend found in $table_hash{TID}...");

               $fixed_entry_attribs =~s#\s+namest="[A-Za-z]*(\d+)"##si;
               $fixed_entry_attribs =~s#\s+nameend="[A-Za-z]*(\d+)"##si;
            }

#            print STDERR "ALL ATTRIBS AFTER: $fixed_entry_attribs\n";


            # Swap the "original" attributes with the "fixed" (well-formed) version...
            $table_data =~s#$orig_entry_attribs#$fixed_entry_attribs#;

#            print STDERR "TAG DATA AFTER: $table_data\n";

            # If the length the "fixed" attributes is shorter (due to whitespace cleanup, etc.), we need to
            # account for the discrepany; otherwise, the next sequential tag with attributes might get skipped...
            if (length($orig_entry_attribs) - length($fixed_entry_attribs) > 0)
            {
               $while_pos3 = $while_pos3 - length($orig_entry_attribs) + length($fixed_entry_attribs);
            }

            pos $table_data = $while_pos3;
         }

#         print STDERR "BEFORE: $table_data\n";

         if ($table_data =~m#</XHTML\.thead>#si)
         {
            $thead_sw = 0;
 
#            print STDERR "Close thead found...\n";

            if ($table_data =~m#(.*?</XHTML\.thead>)#si)
            {
               my $orig_data = $1;
               my $replace_data = $orig_data;

#               print STDERR "Fixing entries before /thead...\n";

               $replace_data =~s#<(/?)entry(\s*[^>]*)>#<$1XHTML.th$2>#sgi;

               $table_data =~s:\Q$orig_data:$replace_data:si;
            }
         }
         elsif ($table_data =~m#<XHTML\.thead>#si || $thead_sw == 1)
         {
            $thead_sw = 1;
 
#            print STDERR "Within thead...\n";

            if ($table_data =~m#(<XHTML\.thead>.*?)$#si)
            {
               my $orig_data = $1;
               my $replace_data = $orig_data;

#               print STDERR "Fixing entries after thead...\n";

               $replace_data =~s#<(/?)entry(\s*[^>]*)>#<$1XHTML.th$2>#sgi;

#               print STDERR "ORIG DATA: $orig_data\nREPLACE DATA: $replace_data\n";

               $table_data =~s:\Q$orig_data:$replace_data:si;
            }
            else
            {
               $table_data =~s#<(/?)entry(\s*[^>]*)>#<$1XHTML.th$2>#sgi;
            }
         }

         $table_data =~s#<(/?)entry(\s*[^>]*)>#<$1XHTML.td$2>#sgi;

#         print STDERR "AFTER: $table_data\n";

 
         $temp_TXT = prep_XML_tags(prep_XML_entities(clean($table_data)));
         $temp_TXT =~s:LTO\.::g;
         push (@{$table_hash{TXT}}, $temp_TXT);
      }
   }
   else
   {
      die "\nIn else for create_table_record, Error opening table file $table_file: File doesn't exist!\n"
   }

   # Journal Name (for display)
   $table_hash{JN} = $mcode_hash{$table_hash{BA}}{JN};

   # Journal Name (for search)
   $table_hash{JJ} = $mcode_hash{$table_hash{BA}}{JN};

   #Content Set Acronym - Set this dynamically, based on the uppercased version of the value in the OPT file...
   $table_hash{UZ} = $dvi_name;

   # Fixed Publication Date (Record Creation Date)
   $table_hash{PF} = $datestamp;
         
}# end of sub create_table_record
#===============================================================================
sub create_marc_record
{
        #mprint("\nIN sub create marc record");
        # Record Number
        # Assigned in sub read_article_record...

        # Source Filename (XML file ID)
        $marc_hash{FL} = $issue_hash{IID};

        # Mcode (for PARIS system)
        $marc_hash{BA} = $issue_hash{BA};

        # Record Functional Type
        $marc_hash{RF} = 'MARC Metadata Record';

        # Database Flag
        $marc_hash{ZZ} = 'MARC';

        # Newspaper Title (Master Publication Title from PARIS)
        $marc_hash{JN} = $issue_hash{JN};

        # Variant Title  ## Updated by Photon...
        $marc_hash{VT} = $mcode_hash{$issue_hash{BA}}{ID}{$issue_hash{ID}}{VARIANT_TITLE};

        # Full Title
        $marc_hash{TE} = $marc_hash{VT};
        
        $marc_hash{HT} = $issue_hash{HT};

	    # Newspaper ID (aka Document ID #)
        $marc_hash{ID} = $issue_hash{ID};

        # Collection ID Number (MARC Record Number)
        $marc_hash{ZI} = $issue_hash{ZI};

        # LCCN# (aka Secondary Collection ID Number)
        $marc_hash{ZJ} = $issue_hash{ZJ};
		
		#  Collection ID Number (ESTC Number)
        $marc_hash{ZK} = $issue_hash{ZK};  #Code added per revised4 spec by Photon

        # Source Holding Institution (Library) Name
        #($marc_hash{IN}) = $record_for_marc =~m:<sourceLibrary>(.*?)</sourceLibrary>:;
        ($marc_hash{IN}) = $issue_hash{IN};

	     	# Shelfmark
        $marc_hash{HL} = $issue_hash{HL};  #Code added per revised4 spec by Photon

        # Source Library Name Code
        $marc_hash{LB} = $issue_hash{LB};  #Code added per revised4 spec by Photon

        # Copyright Statement
        $marc_hash{CP} = $issue_hash{CP};  #Code added per revised4 spec by Photon

        # Language of Publication
        $marc_hash{LA} = $mcode_hash{$issue_hash{BA}}{LA};
        # Publication Frequency
        $marc_hash{FQ} = $mcode_hash{$issue_hash{BA}}{FQ};

   		# Populate BU tag from Lookuptable by Photon ....
   		$marc_hash{BU} = $mcode_hash{$issue_hash{BA}}{BU};

	    # Populate PB tag from Lookuptable by Photon ....
   		$marc_hash{PB} = $mcode_hash{$issue_hash{BA}}{PB};
  
        # Place of Publication - City
       $marc_hash{PC} = $mcode_hash{$issue_hash{BA}}{PC};

       # Place of Publication - State
       $marc_hash{PS} = $mcode_hash{$issue_hash{BA}}{PS};

        # Place of Publication - Country                     #Updated by Photon
       $marc_hash{PN} = $mcode_hash{$issue_hash{BA}}{PN};

        # Place of Publication - Region                      #Updated by Photon
       $marc_hash{PR} = $mcode_hash{$issue_hash{BA}}{PR};
		
        # Fixed Publication Date
        $marc_hash{PF} = $issue_hash{PF};

        # Starting Year of Coverage (in YYYY Format)
        $marc_hash{YS} = $mcode_hash{$marc_hash{BA}}{ID}{$marc_hash{ID}}{START_YEAR};

        # Ending Year of Coverage (in YYYY Format)
        $marc_hash{YE} = $mcode_hash{$marc_hash{BA}}{ID}{$marc_hash{ID}}{END_YEAR};

        # Update Release Date (in YYYYMMDD format)
        $marc_hash{UD} = $datestamp;

}# end of sub create_marc_record
#===============================================================================
sub create_page_record
{
        # Record Number
       # $page_hash{RN} = '27' . $page_rn_base;
       
       ############# Updated by Photon
        $page_hash{RN} = '16' . $page_rn_base;
        if (exists ($page_id_hash{$article_hash{PID}}))
        {
           $page_hash{RN} = $page_id_hash{$article_hash{PID}};
        }
        else
        {
           mprint ("\n*** Page ID not found in lookup file.  No RN assigned: $article_hash{PID}\n");
           exit (44);
        }

        # Page Number
        #$page_hash{PG} = $article_hash{pg_dummy};           #Updated by Photon
		($page_hash{PG}) = $article_hash{PID} =~ m:^.*-(\d+):g;           #Updated by Photon

        # Record Type
        $page_hash{RT} = 'PAGE';

        # Database Flag
        $page_hash{ZZ} = 'PAGE';
        
        # Page Number
        #$page_hash{PID} = $issue_hash{PID};
		$page_hash{PID} = $article_hash{PID};

        $page_hash{FO}= $mcode_hash{$issue_hash{BA}}{FO};  #Updated by Photon for FO here since we r using the value of BA

        # Mcode
        $page_hash{BA} = $issue_hash{BA};

        # Source Issue Number
        $page_hash{IS} = $issue_hash{IS};

        # Publication Information
        $page_hash{PI} = $article_hash{PI};
        
        # Publication Date for Display
        $page_hash{DA} = $issue_hash{DA};

        # Journal Name (for display)
        $page_hash{JN} = $issue_hash{JN};

        # Full Title
        $page_hash{TE} = $issue_hash{TE};
        
         # Short Title
        $page_hash{HT} = $issue_hash{HT};

        # Page Count
        $page_hash{IP} = $issue_hash{IP};

        # Fixed Publication Date (in YYYYMMDD format)
        $page_hash{PF} = $issue_hash{PF};

        # Ending Date of Coverage (in YYYYMMDD format)
        $page_hash{YE} = $issue_hash{YE};

        # Newspaper ID (aka Document ID #)
        $page_hash{ID} = $issue_hash{ID};

        # Collection ID Number (MARC Record Number)
        $page_hash{ZI} = $issue_hash{ZI};

        # LCCN# (aka Secondary Collection ID Number)
        $page_hash{ZJ} = $issue_hash{ZJ};
        
        #  Collection ID Number (ESTC Number)
        $page_hash{ZK} = $issue_hash{ZK};  #Code added per revised4 spec by Photon

        # Source Holding Institution
        $page_hash{IN} = $issue_hash{IN};

        # Source Library Name Code
        $page_hash{LB} = $issue_hash{LB};  #Updated by Photon

        # Copyright Statement
        $page_hash{CP} = $issue_hash{CP};  #Updated by Photon
        
        # Source Library Name Code
        $page_hash{LA} = $issue_hash{LA};  #Updated by Photon
		$page_hash{SH} = $issue_hash{SH};        
        $page_hash{UZ} = $issue_hash{UZ};  #Updated by Photon



}# end of sub create_page_record
#===============================================================================
###############################################################################
# Name of hash passed into subroutine for the five different possible record  #
# types.  The hash name is passed as a string, and using symbolic references, #
# the tag names are added in.  e.g. $$hashname{$key}  could be $meta_hash{BA} #
# ($hashname eq "meta_hash").                                                 #
###############################################################################
sub add_format_b_tags
{
   my $hashname = shift @_;

#   mprint ('In subroutine add_format_b tags');
#   mprint ('HASH: '.$hashname);

   # For every piece of data, we now need to add the Dialog_B tag and a space.
   foreach my $key (keys(%$hashname))
   {
#      mprint ('KEY: '.$key);

      if (ref ($$hashname{$key}) eq "HASH")
      {
         foreach my $subkey (keys (%{$$hashname{$key}}))
         {
#            mprint ('HASH VALUE: '.$$hashname{$key}{$subkey});
            $$hashname{$key}{$subkey} = sprintf("%-4s", $key) . $$hashname{$key}{$subkey} if ($$hashname{$key}{$subkey} =~m:\S:);
         }
      }
      elsif (ref (\$$hashname{$key}) eq "SCALAR")
      {
#         mprint ('SCALAR VALUE: '.$$hashname{$key});
         $$hashname{$key} = sprintf("%-4s", $key) . $$hashname{$key} if ($$hashname{$key} =~m:\S:);
      }
      elsif (ref ($$hashname{$key}) eq "ARRAY")
      {
         foreach my $element (@{$$hashname{$key}})
         {
#            mprint ('ARRAY VALUE: '.$element);
            $element = sprintf("%-4s", $key) . $element if ($element =~m:\S:);
         }
      }
      else
      {
         die "\n\n***Error in add_format_b_tags function: improper reference type.\n\n";
      }
   }

#   mprint ('Exiting add_format_b_tags subroutine...');
   return;

}#end of sub add_format_b_tags
#===============================================================================
sub make_B_format
{
   my $teststring = shift(@_);

   # I grab the tagname for use on wrapping lines...
   (my $tagname) = $teststring =~m:^(.{3}):;

   # TX content has already been cleaned and prepped...
   $teststring = prep_XML_entities(clean($teststring)) unless ($tagname =~m:^(TX |AIF|TI |RM |TXT)$:);
   $teststring = add_tag_namespace($teststring) if ($tagname =~m:^(AIF|CI |PIF)$:);
   $teststring = prep_XML_tags($teststring) unless ($tagname =~m:^(<< |TX |>> |AIF|CI |PIF|RM |TXT)$:);

   my $stringlength = length($teststring);
   my $outstring = '';

   if($stringlength == 0)
   {
      return $teststring;
   }

   if($stringlength < 72)
   {
      $padlength = 80;
      $template = "A$padlength";
      $outstring = pack($template, $teststring);
      $outstring .= $hard_ret;
      $linecount++;
   }
   else #length is greater than 72, need to split it
   {
      $teststring=~m:^(.{72})(.*?)$:s;
      $firstline = $1;
      $remainder = $2;
      $padlength = 80;
      $template = "A$padlength";

      $outstring .= pack($template, $firstline);
      $outstring .= $hard_ret;
      $linecount++;
      @rest = $remainder =~m:(.{1,68}):sg;   #68+4=72

      foreach $nextline(@rest)
      {
         $outstring .= '    '; #the 4 leading spaces (we have some 3-character B tags)
         $padlength = 76;
         $template = "A$padlength";
         $outstring .= pack($template, $nextline);
         $outstring .= $hard_ret;
         $linecount++;
      }#foreach
   } # end of else

   return($outstring);

}#make_B_format
#===============================================================================

sub get_date
{
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
    $yearstamp=sprintf("%4d",$year+1900);
    $daystamp=sprintf("%02d",$mday);
    $monthstamp=sprintf("%02d",$mon+1);
    $datestamp=$yearstamp.$monthstamp.$daystamp;
}
#===============================================================================
sub naksyn
{
        my $item = shift @_;
        $item =~s:(\<.*?\>):$nak$1$syn:sig;
        return $item;
}
#===============================================================================
sub create_AIF_PIF
{
        my $position_guide = shift @_;

        # Position Guide
		# Changing this, as attributes can occur in any order...
        #(my $page_num, my $pg_pos) = $position_guide =~m:<pg\s+pgref="(.*?)"[^>]+pos="(.*?)":s;
		
		(my $page_num) = $position_guide =~m:<pg[^>]*\s+pgref="(.*?)":s;
		(my $pg_pos) = $position_guide =~m:<pg[^>]*\s+pos="(.*?)":s;
		
		#print STDERR "PAGE NUM: $page_num\n";
		#print STDERR "PAGE POS: $pg_pos\n";
		
         my $pPG = $page_hash{PG};
         $pPG =~ s/^0+//;

        # Strip leading zeros from the article's RN, to prevent linking issues within the application...
        (my $temp_article_RN) = $article_hash{RN} =~m:^0*(\d+)$:;
        #print STDERR "TEMP RN: $temp_article_RN\n";

        # Create Page Information (for Article records)...
        push(@{$article_hash{PIF}}, '<page pid="' . $pi_pgref_hash{$page_num} . '" pos="' . $pg_pos . '">'
                                    . $article_hash{PA} . '</page>');

        # Create Article Information (for Page records)...

        # Replace double-quote instances with single quotes...
        my $temp_article_title = $article_hash{TI};
        $temp_article_title =~s:":':g;
        if ($page_num ne $pPG) {
			(my $chkID) = $article_hash{ZX} =~ m:-\d+-(\d+)-:gi;
			$chkID =~ s/^0+//gi;
			if(scalar(@aif_multiple)>0 and $chkID < $page_num){
				$article_hash{ZX} = shift(@aif_multiple);
				$article_hash{ZX} = $article_hash{ZX}."-".$article_hash{SE};
			}
			#print "\n article_hash:.$article_hash{ZX}";
			push(@AIF_array, '<article ti="' . $temp_article_title . '" pgref="' . $page_num .
#					  '" pos="' . $pg_pos . '" XXRN="' . $xxrn_value . $article_hash{RN} . '">' .
					  '" pos="' . $pg_pos . '" XXRN="' . $xxrn_value . $temp_article_RN . '">' .
		                       $article_hash{ZX} . '</article>');
		}else
        {
		  if (@AIF_array)
          {
            for (my $i=0; $i<=$#AIF_array; $i++)
            {
    		  if ($AIF_array[$i] =~ m:pgref="$pPG":ms)
              {
					push (@{$page_hash{AIF}}, $AIF_array[$i]);
					$AIF_array[$i] = undef;
			    }
   	        }
		   }

          push (@{$page_hash{AIF}}, '<article ti="' . $temp_article_title . '" pgref="' . $page_num .
#                                  '" pos="' . $pg_pos . '" XXRN="' . $xxrn_value . $article_hash{RN} . '">' .
                                  '" pos="' . $pg_pos . '" XXRN="' . $xxrn_value . $temp_article_RN . '">' .
                                  $article_hash{ZX} . '</article>');
        }

}# end of sub create_AIF_PIF
#===============================================================================
sub reduce_text
{
    my $text_item = shift(@_);

    my @sent = ();
    my $outstring = '';
    my $templength = 0;

    while ($text_item =~m:($nak<.*?/.*?>$syn ?):sg)
    {
       my $tag_pair = $1;

       if ($templength + length($tag_pair) >= 8000)
       {
          #print "+++ Paragraph will be too large ($templength + " . length($tag_pair) . ")... Ending current paragraph...\n";

          # End the paragraph...
          push (@sent, $outstring . prep_XML_tags('</p>') );

          # Start new paragraph...
          $outstring = prep_XML_tags('<p>');

          # Reset the length counter...
          $templength = 0;
       }

       $templength += length($tag_pair);

       $outstring .= $tag_pair;


#       $templength += length($tag_pair);
#
#       $outstring .= $tag_pair;
#
#       if ($templength >= 8000)
#       {
##          print "+++ Paragraph too large ($templength)... Splitting up into multiple pieces...\n";
#
#          # End the paragraph...
#          push (@sent, $outstring . prep_XML_tags('</p>') );
#
#          # Start new paragraph...
#          $outstring = prep_XML_tags('<p>');
#
#          $templength = length($outstring);
#       }
    }

    # Pick up remainder in output array...
    push (@sent, $outstring);

    return(@sent);
}
#===============================================================================
sub get_rn
{
        $yearstr = getbin($rn_year, 24); #8 bits
        $monthstr = getbin($rn_month,28); #4 bits
        $daystr = getbin($rn_day,27); #5 bits
        $pagestr = getbin($rn_page,24); #8 bits
        $artstr = getbin($rn_article,25); #7 bits

        $combined = "$pagestr$artstr$yearstr$monthstr$daystr"; # to correct RM overflow
        $temp_rn = bin2dec($combined);
        $record_number = sprintf("%08u",$temp_rn);
        $temp_rn = "RN  ".sprintf("%08u",$temp_rn);
        return $temp_rn;
}
#===============================================================================

sub getbin
{
    my($number,$bits) = @_;
    my $str = unpack("B32", pack("N", $number));
    $str =~s:^.{$bits}::;
    return $str;
}
#===============================================================================

sub bin2dec {
    return unpack("N", pack("B32", substr("0" x 32 . shift, -32)));
}

#===============================================================================
sub fix_hyphenated{

   # This code handles the recombinination of hyphenated words. It does this by checking for a word that
   # contains a word character, followed directly by a hyphen, followed directly by the </wd> tag. In
   # addition, to make sure the words should be combined, it takes the y0 positional coordinate (2nd
   # number in pos="..." value) from second word, subtracts 25, and makes sure it's greater than the y0
   # positional coordinate from the original word, containing the hyphen.

   # If the word has a word character, followed by a hyphen at the end of the word, store it...

   # Grab the paragraph...
   my $old_temp_text = shift (@_);

   my $xml_word = '';
   my $xml_y0 = '';
   my $hyphen_word = '';
   my $first_word = '';
   my $hyphen_y0 = '';
   my $new_temp_text = '';
   my $pos2 = '';


   while ($old_temp_text =~m:(<wd[^>]*>(.*?)</wd>):g)
   {
      # Put a space between every word tag so that the words will index after tags are stripped...
      $xml_word = ' '.$1;

      # We're already working with a hyphenated word...
      if ($hyphen_word ne "")
      {
         # First, Grab the y0 pos value for the "2nd" word...
         ($pos2, $xml_y0) = $xml_word =~m:<wd\s+pos="([^,]*,([^,]*),[^"]*)":;

         # If the y0 difference is more than 24, we have a legit hyphenated word
         if (($xml_y0 - $hyphen_y0 - 25) >= 0)
         {
            # Now, try to "fix"/join the two words...
            # Find the 2nd "word". It could contain junk before the real letters, so we make sure to only
            # grab starting from letters or numbers...
            $xml_word =~m:<[^>]*>(.*?)<:;
            $bad_2nd_word = $1;
            $bad_2nd_word =~m:^[^A-Za-z0-9&]*(.*?)$:;
            $good_2nd_word = $1;

            # If, after grabbing the word (starting from letters/numbers), we have a word, continue...
            if ($good_2nd_word ne "")
            {
               # Join the two "halves" of the word...
               $new_word = $first_word.$good_2nd_word;

               # Delimit the 2nd word, in case there's a strange character...
               $quoted_2nd_word = quotemeta($good_2nd_word);

               # And, replace each half of the word with the new word...
               $hyphen_word =~s:\Q$first_word-</:$new_word</:;
               $hyphen_word =~s:(pos="[^"]*")>:$1 pos2="$pos2">:;
            }
            else
            {
               # Only remove the hyphen from the first word, since we couldn't make a new word...
               $hyphen_word =~s:\Q$first_word-</:$first_word</:;
            }
         }# end of if (($xml_y0 - $hyphen_y0 - 25) >= 0)

         # Either way, we need put our new (or unchanged) words into the paragraph...
         # NOTE: Instead of duplicating the same word, the pos of the 2nd word is now moved to the first,
         #       into the pos2 attribute...

         $new_temp_text .= $hyphen_word;
         $hyphen_word = '';
      }# end of if ($hyphen_word ne "")

      # Otherwise, we can look for new hyphenated words...
      # Find the y0 position, as well as the first half of the word, without the hyphen...
      elsif ($xml_word =~m:<wd\s+pos="[^,]*,([^,]*),[^>]*>(.*?[A-Za-z0-9])-</:)
      {
         $hyphen_y0 = $1;
         $first_word = $2;
         $hyphen_word = $xml_word;
         $xml_word = "";
      }

      # No hyphenated words found, so keep the word as-is...
      else
      {
         $new_temp_text .= $xml_word;
      }
   }# end of while ($old_temp_text =~m: ...

   return ($new_temp_text);
}
#===============================================================================
# This subroutine adds namespace to and NAK and SYN codes around all tags...
sub prep_XML_tags
{
   my $line=shift(@_);

   # This call adds namespace to all tags...
   $line = add_tag_namespace($line);

   # Add NAK and SYN codes around tags...
   $line =~s:(<[^>]+>):$nak$1$syn:sg;

   return($line);

}#end of sub prep_XML_tags
#===============================================================================
# This subroutine adds namespace to all tags...
sub add_tag_namespace
{
   my $line=shift(@_);

   $line =~s:(</?):$1$namespace\.:sg;

   # Remove namespace from italics tagging...
   $line =~s:(</?)$namespace\.(i|I)>:$1I>:sg;

   return($line);

}#end of sub add_tag_namespace
#=========================================================
# This subroutine adds NAK and SYN codes around all entities...
sub prep_XML_entities
{
   my $line=shift(@_);

   # Add NAK and SYN codes around entities...
   $line =~s:(&[^;]*;):$nak$1$syn:sg;

   return($line);

}#end of sub prep_XML_entities
#=========================================================
# This subroutine converts decimal entities between 160 and 255 to their actual characters...
# All other decimal entities (i.e. &#8212;) are left alone...
sub convert_entity
{
   my $ent=shift(@_);

   if ($ent >= 160 && $ent <= 255)
   {
      $ent = chr($ent);
   }
   else
   {
      $ent = '&#' . $ent . ';';
   }

   return($ent);

}#end of sub convert_entity
#=========================================================
sub process_only_headnotes
{
   foreach my $mcode (keys %mcode_hash)
   {
      if ($mcode_hash{$mcode}{OUTPUT})
      {
         $issue_hash{BA} = $mcode;
         mprint ("Creating MATP record for Mcode: $mcode");
         &create_matp_record();
         &add_format_b_tags('matp_hash');
         &write_matp_record();
         %matp_hash = ();
         $mcode_hash{$mcode}{OUTPUT} = 0;
      }
   }
   return;
}
#=========================================================
sub process_only_spotlight
{
         mprint ("Creating Spotlight record");
         create_spotlight_record();
         &add_format_b_tags('spotlight_hash');
         &write_spotlight_record();
         %spotlight_hash = ();

   return;
}
#=========================================================
sub process_only_tables
{
   my @table_files = ();

   # Query the directory for table files...
   opendir (TABLEDIR,$table_dir) || die "\nError opening table directory $table_dir: $!.";

   # Get the directory listing of all table files, and prefix each one with the directory name...
   push (@table_files, grep {!/^\.\.?$/ && s/^/$table_dir/} readdir (TABLEDIR) );

   closedir (TABLEDIR);

   foreach my $table_file (sort(@table_files))
   {
#      next unless ($table_file =~m:ECON-2000-1223-0195-002.xml: || $table_file =~m:ECON-1994-0813-0098-001.xml:);

      mprint ("Creating Table record for File: $table_file");
      &create_table_record($table_file);
      &add_format_b_tags('table_hash');
      &write_table_record();
      %table_hash = ();

#      next unless ($table_file =~m:ECON-2000-1223-0195-002.xml:);

#      last;
   }
   return;
}
#=========================================================
my $prev_pos=0;
my $errStr="";
sub continuation_page_backward
{
	my $cur_pos = tell($NCNPOUT);
	my $len = $cur_pos - $prev_pos;
	if(-s $output_file){
		my $size = -s $output_file;
		my $filestr;
		close($NCNPOUT);

        if ($dvi_name eq 'FTIM' || $dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
        {
   	   open($NCNPOUT,'+<:encoding(ISO-8859-1)', $output_file);
        }
        else
        {
           open($NCNPOUT,"+<$output_file");
        }
        
		seek($NCNPOUT,$prev_pos,0);
		read($NCNPOUT,$filestr,$len);
		foreach my $aif (@AIF_array) {
			if(defined $aif){
				(my $pg) = $aif =~ m:pgref=\"(\d+)\":gi;
				$pg = sprintf("%04d",$pg);
				$aif =~ s/(.*?>.*?)-(\d+)-/$1-$pg-/i;
				$filestr =~ s/(PG  $pg.*?\n)(UZ  )/sprintf("%s", $1 . &make_B_format("AIF ".$aif) . $2)/smegi;
			}
		}
#                foreach my $page_pid (keys %TS_hash)
#                {
#                   #print STDERR "\n*** NEED TO OUTPUT: $page_pid\n\n";
#
#                   $filestr =~ s/(PID $page_pid.*?\n)(\$\$)/sprintf("%s", $1 . &make_B_format("TS  " . $TS_hash{$page_pid}[0]) . $2)/smegi;
#                }

		truncate($NCNPOUT,$prev_pos);
		close($NCNPOUT);
		
        if ($dvi_name eq 'FTIM' || $dvi_name eq 'ILN' || $dvi_name eq 'TLS' || $dvi_name eq 'ECON' || $dvi_name eq 'PPNP' || $dvi_name eq 'LSNR' || $dvi_name eq 'TDA' || $dvi_name eq 'STHA')
        {
   	   open($NCNPOUT,'>>:encoding(ISO-8859-1)', $output_file);
        }
        else
        {
           open($NCNPOUT,">>$output_file");
        }
		
		print $NCNPOUT $filestr;
	}
	$prev_pos = $cur_pos;
}

END
{
   for my $lccn (keys %missing_lccn)
   {
      print LOGFP $missing_lccn{$lccn};
      $send_mail = 1;
   }


   close (LOGFP);
   $message_file = $output_dir."ncnp_message.txt" ;

   if($send_mail)
   {
      my $status = 1;

      # Send a message if there was a problem during conversion...
      unless($complete)
      {
         $mess = "Program terminated prematurely\n\n".$mess;
         $status = 44;

         open(MSG,">$message_file") || die "\n\nError opening message file $message_file: $!.\n\n";
         print MSG $mess;
         close(MSG);


         if ($platform eq "Unix")
         {
            print STDERR `mailx -s "NCNP automated run summary" $email_address < $message_file`;
            system "rm $message_file";
         }
         elsif ($platform eq "VMS")
         {
            $email_address = "pe_prod";
            print STDERR `PMDF MAIL/SUBJECT="NCNP automated run summary" $message_file $email_address`;
            system "delete $message_file;*";
         }
      }

      # Send an email with details relating to the conversion...
      if ($platform eq "Unix")
      {
         print STDERR `mailx -s "NCNP: Missing LCCN Value(s)" $email_address < $logfile`;
      }
      elsif ($platform eq "VMS")
      {
#         $email_address = "pe_prod";
         print STDERR `PMDF MAIL/SUBJECT="NCNP: Missing LCCN Value(s)" $logfile $email_address`;
      }

      exit($status);  #return VMS status, 44 for failure, 1 for success

   }#end of if($send_mail)
}
