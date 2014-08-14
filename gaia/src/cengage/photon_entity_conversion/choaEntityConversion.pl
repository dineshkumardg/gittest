#!/usr/bin/perl

# Author :: Photon
# Date   :: Jun'29, 2013
################################
# Initial Release Version : 0.0
# History 
################################
##
## Purpose :: Do the entity conversion for following elements, <meta:authors> , <meta:editors> and <gift-doc:document-titles> against
##            GIFT xml feeds.
##  
## Dependency file :: comprehensive_entity_list.html [Important :: should exists in current directory where script runs]
##
## Usage   :: perl choaEntityConversion.pl ./<feedfile>
##
## example :: perl choaEntityConversion.pl ./NOINDEX-CHOA_20131028_00609.xml.gz
##
## Manually create the zip file in the output directory after ran the script. 
##            cd ./output
## example :: gzip -c91 ./NOINDEX-CHOA_20131028_00609.xml > ./NOINDEX-CHOA_20131028_00609.xml.gz
##
## Following were perl modules downloaded from CPAN, a recommended repository for perl modules 


use strict;
use warnings;

use Archive::Extract;

my $gzFileName = $ARGV[0];


### build an Archive::Extract object ###
my $ae = Archive::Extract->new( archive => "$gzFileName");

### extract to cwd() ###
my $ok = $ae->extract;

### extract to /tmp ###
$ok = $ae->extract( to => "." );

### what if something went wrong?
$ok = $ae->extract or die $ae->error;

### files from the archive ###
my $files   = $ae->files;

### dir that was extracted to ###
my $outdir  = $ae->extract_path;

### quick check methods ###
$ae->is_gz;     # is it a .gz

(my $outputfilename = $gzFileName) =~ s/\.gz$//;
my $inputFileName = $outputfilename ;

my $item_counter = "";
my %entity_map_hash;

&createDirectory('logs');
&createDirectory('output');
&createLogFile("$inputFileName");
&Read_Entity_Mapping_Table();
&processSources ();

##======================================================================
##  Create directory if not exists
##======================================================================
sub createDirectory {
  my $directory = shift;  
  die "Unable to create $directory\n" unless(-e $directory or mkdir $directory);
}

##======================================================================
##  Create indivudual log file
##======================================================================
sub createLogFile {
 my $logFileName = shift;
 $logFileName =~s /\.xml/_/g; 
  (my $sec, my $min, my $hour, my $mday, my $mon, my $year, my $wday, my $yday, my $isdst) = localtime(time);
  my $logFile =  "$logFileName" . sprintf("%04d%02d%02d", $year+1900, $mon+1, $mday) . '.log';
  unless (open LOG, "> ./logs/$logFile") {
    print " Can't create $logFile : $!";  
    exit;
 } 
}

##======================================================================
##  Subroutine to do the source files for processing
##======================================================================
sub processSources {
  my ($content, $item, $feed) = ();  
  my ($total_counter, $file_counter) = (0,0);
  my (@itemsList, @sourceList) = ();  
  
  print LOG "Reading input file \t[$inputFileName]\n";
  
  my $tmprs = $/;
  undef $/;
  die "Unable to read the file [./$inputFileName] ...\n" unless (open FH,"<./$inputFileName");
  $content = <FH>;
  close (FH);
  $/ = $tmprs;

  unless (open COUT, "> ./output/$outputfilename") {
    print " Can't create $outputfilename : $!";  
    exit;
  }
  
  my ($header) = $content =~ m/(<gold:feed[^>]*>)/sgi;
  my ($footer) = $content =~ m/(<gold:metadata>.*)/sgi;
  
  $feed = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
  $feed .= $header;
  $item_counter = 0;
  
  if (&valid_format( $content)){
   my $i =  @itemsList = &splitItems( $content );   
	foreach $item (@itemsList) {
	  $item_counter++;          
	  $item =~ s/<meta:authors>(.*?)<\/meta:authors>/'<meta:authors>'.convertAuthorsEntity($1).'<\/meta:authors>'/sgie;
	  $item =~ s/<meta:editors>(.*?)<\/meta:editors>/'<meta:editors>'.convertEditorsEntity($1).'<\/meta:editors>'/sgie;
	  $item =~ s/<gift-doc:document-titles>(.*?)<\/gift-doc:document-titles>/'<gift-doc:document-titles>'.convertTitleEntity($1).'<\/gift-doc:document-titles>'/sgie;
	  $feed .= $item;
	}
	 $feed .= $footer;
  }
  binmode(COUT, ":utf8");
  print COUT "$feed";  
  close(COUT);  
  print LOG "Total item counter\t$item_counter\n";
  #&gzip($outputfilename);
  close(LOG);
}

##======================================================================
##  Subroutine to check valid format
##======================================================================
sub valid_format {
  my $content = shift;
  my $valid = 0;
  if ($content =~ /<gold:feed[^>]*>/si) {
	$valid = 1;
  }
  return $valid;
}

##======================================================================
sub splitItems {   
   my $content = shift;
   my @articles;
   my $ct =0 ;
   while ($content =~ /(<gold:document-instance>.*?<\/gold:document-instance>)/sgi) {   
      push (@articles, "$1\n");
   }
   return (@articles);
}

##======================================================================
sub convertAuthorsEntity {
  my $authorsName = shift;
  $authorsName =~ s/<(meta:(prefix|first-name|middle-name|last-name|suffix|composed-name|name))>(.*?)<\/\1>/"<$1>".make_utf8_entities($3)."<\/$1>"/sgie;
  return $authorsName;
}  

##======================================================================
sub convertEditorsEntity {
  my $editorsName = shift;  
  $editorsName =~ s/<(meta:(prefix|first-name|middle-name|last-name|suffix|composed-name|name))>(.*?)<\/\1>/"<$1>".make_utf8_entities($3)."<\/$1>"/sgie;  
  return $editorsName;
}  

##======================================================================
sub convertTitleEntity {
  my $titleName = shift;  
  $titleName =~ s/<(meta:(title-display|title-sort|title-open-url))>(.*?)<\/\1>/"<$1>".make_utf8_entities($3)."<\/$1>"/sgie;
  return $titleName;
}

##======================================================================
sub gzip {
  my $file = shift;	
  #print $ENV{PWD}, "\n";
   `gzip -c91 $file > $file.gz` if($^O !~ /win/i);
}

##======================================================================
sub Read_Entity_Mapping_Table {
  my $entity_file = "comprehensive_entity_list.html";
  open (ENTITYMAP,"<$entity_file") || die "\nError opening $entity_file: $!.\n";
  
  my %entity_map_hash;
  while(my $entity_line = <ENTITYMAP>){		
  (my $hex, my $dec, my $char, my $non_std_char, my $display, my $desc) = split (m:</td>:, $entity_line);
		
	# Remove any HTML tags...
  $hex =~s:<[^>]*>::g if (defined ($hex));
  $dec =~s:<[^>]*>::g if (defined ($dec));
  $char =~s:<[^>]*>::g if (defined ($char));
  $non_std_char =~s:<[^>]*>::g if (defined ($non_std_char));
  $display =~s:<[^>]*>::g if (defined ($display));
  $desc =~s:<[^>]*>::g if (defined ($desc));
		
  #print "$hex,$dec, $char,$non_std_char,$display,$desc \n";
  #$dec =~s:&amp;#([^;]*);:$1: if (defined($dec));
		
  # Skip any lines that don't have contents within the "Character Entity" or "Non Standard Character Entity" field...
  if ((! defined($char) || $char !~m:\S:) && (! defined($non_std_char) || $non_std_char !~m:\S:))
  {next};	
  
  $display =~s:&#x([^;]*);:$1:g if (defined ($display));
  # Store the 'real' or "Non Standard Character Entity" character entities, with the hex number as the value...
  if (defined ($non_std_char) && $non_std_char !~m:&nbsp;: ) {
	$non_std_char =~s:&amp;:&:g;
				
	#&mprint ("NON-STD CHAR: $non_std_char\nHEX: $hex\n\n");				
	# Treat &Lt; special...
	if ($non_std_char =~m:&Lt;:) {
	  $entity_map_hash{$non_std_char} = '&lt;';
	} else {
	  #Process multiple entity values, if present...
	  while ($non_std_char =~m:(&[^;]*;):g) {    
		my $ns_char = $1;
						
		#Process multiple hex values/non-std entity, if present...
		  while ($hex =~m:&amp;#x([^;]*);:g) {
			$entity_map_hash{$ns_char} .= chr(hex($1));
		  }
	  }
	}
  }      

  if (defined ($char) && $char !~m:&nbsp;: ) {
	$char =~s:&amp;:&:;
	# Treat &amp; &apos; &quot; &gt; or &lt; special...
	if ($char =~m:&(amp|apos|gt|lt|quot);:) {
	  $dec =~s:&amp;#([^;]*);:$1:;
	  $entity_map_hash{$dec} = $char;
    } else {
	  #Process multiple hex values, if present...
	  while ($hex =~m:&amp;#x([^;]*);:g) {
		$entity_map_hash{$char} .= chr(hex($1));
	  }
	}
  }
  # Store the Windows-1252 char num, with the display value (hex number) as the value...
  elsif ($desc =~m:Windows-1252: && $dec >= 128) {
	#print STDERR "DEC: $dec\nHEX: $display\n\n";
	$entity_map_hash{$dec} = chr(hex($display));
   }
  }
  
  close(ENTITYMAP);
}#end of sub read_entity_mapping_table
	################################################################################
	
sub make_utf8_entities{
  my $line = shift;
  
  while ($line =~m:(&[^;().,!'"`~%\$\^ ]*;):g) {
	my $ent = $1;			
			# Save the position for later, because the substitution (farther below) resets the position...
	my $while_pos = pos ($line);			
	if((my $hex_value) = $ent =~m:&#x([^;]*);:) {		
	  # Replace the hex entity with the actual character (except for ", ', &, < and >)
	  # The characters then become UTF-8 upon output...
	  if (exists ($entity_map_hash{hex($hex_value)})) {
		$line =~s:$ent:$entity_map_hash{hex($hex_value)}:eg;
	  } else {
		$line =~s:$ent:chr(hex($hex_value)):eg;
	  }	# Restore the position...
	  pos $line = $while_pos - length ($ent);
				
	} elsif ((my $dec_value) = $ent =~m:&#([\d]+):)	{
	  # Replace the dec entity with the actual character (except for ", ', &, < and >)
	  # The characters then become UTF-8 upon output...
	  if (exists ($entity_map_hash{$dec_value})) {
		$line =~s:$ent:$entity_map_hash{$dec_value}:g;
	  }else {
		$line =~s:$ent:chr($dec_value):eg;
	 }				
	  # Restore the position...
	  pos $line = $while_pos - length ($ent);
	} elsif (exists ($entity_map_hash{$ent})) {
	  # Replace the char entity with the actual character
	  # The characters then become UTF-8 upon output...
	  $line =~s:$ent:$entity_map_hash{$ent}:g;				
	  # Restore the position...
	  pos $line = $while_pos - length ($ent);
	} elsif ($ent =~m:&(amp|apos|gt|lt|quot);:) {
	# Note that &amp; &apos; &gt; &lt; and &quot; are not in the table, as they are the only
	# character entities inherently allowed within XML...
	# Restore the position...			  
	pos $line = $while_pos;
	} else {
	  $line =~s:$ent::g;
	  pos $line = $while_pos - length ($ent);
	}
			
  }# end of while ($line =~ m:(&[^;]*;):g)
		
  # Replace Windows-1252 characters with acceptable replacement characters...
  while ($line =~m:([\x80-\x9F]):g)	{
    # Save the position for later, because the substitution (farther below) resets the position...
    my $while_pos = pos $line;			
    my $ent = $1;
			
    #&mprint("Fixing Windows-1252 chars...\n");
			
   if (exists ($entity_map_hash{ord($ent)})) {
	# Replace the char entity with the actual character (which then becomes UTF-8 upon output)...
	$line =~s:$ent:$entity_map_hash{ord($ent)}:eg;
   } else {
	$line =~s:$ent::g;
   }
   pos $line = $while_pos - length ($ent);
  }# while ($line =~ m:([\x80-\x9F]):g)
		
  # Now, clean up any stray '&' occurrences...
  # $line =~s:&amp;:&:g;
  # $line =~s: & : &amp; :g;  Note: stray & not surrounded by spaces were not being converted.
		
  while ($line =~ /&([^ ]*)/g) {
	unless ($1 =~ /;/) {	
	  my $savepos = pos $line;
	  $line = $` . '&amp;' . $1 . $' ;
	  pos $line = $savepos + 4;
	}
  }

  # Lastly, remove all errant control characters...
  $line =~s:([\x00-\x08\x0A\x0B\x0E-\x1F])::g;
  #$line =~ s/&(?!#x[0-9A-Za-z]+|amp)/&amp;/g;

  return($line);

}# end of sub make_utf8_entities
################################################################################

