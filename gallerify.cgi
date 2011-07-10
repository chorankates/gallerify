#!/usr/bin/perl -w
## gallerify.cgi -- create thumbnails based on a directory of images

use strict;
use warnings;

use CGI qw(:standard);
use CGI::Carp 'fatalsToBrowser'; # dbgz
use File::Basename;
use File::Spec;
use Time::HiRes;
use XML::Simple;

my $config_file = $ENV{gallerify_config} // 'gallerify-default.xml';

%CFG::settings = get_xml($config_file); # global settings, stored on disk in XML
%CFG::parameters; # session settings, received via URL

## print global headers
print(
        header(),
        start_html(
            	-title=> "gallerify",
            	-text   => "black",
		-style => { src => $CFG::settings{css} }, # was '../style.css'
        ),
        "<div class='header'>",
        "<h2><a href='/cgi-bin/gallerify.cgi'>gallerify</a> - simple folder to thumbs</h2>",
        "</div>",
        "<div class='main'>",
    );


## traffic cop
unless (param()) {
    # no params, build the start page
    print (h2("information"), "<ul>");
        
    my @information = (
        "gallerify takes a folder and turns its contents into a page of thumbnails. very basic for now",
    );
    
    print "<ul>";
    foreach (@information) {
        print "<li>$_</li>";
    } print ("</ul>");
    
} else {
	# build the thumbnails page
   my @p = param();
   
   $CFG::parameters{$_} = param($_) foreach(@p); # this is a quick and dirty way to handle most parameters.. does not work when you've got multiple controls with the same name but different values

	error ("unable to use directory $CFG::parameters{directory}") unless -d $CFG::parameters{directory};
	
	if (-d $CFG::parameters{directory}) {
		# find the files.. all the files
		
		#use File::Find; <-- will use this when incorporating recursion.. next rev
		my @files = glob($CFG::parameters{directory} . '/*');
		print h2("gallerifying $CFG::parameters{directory}");
		print "<table border=0>"; 
		my @links;
		foreach my $file (@files) {
			next if -d $file;
			next unless $file =~ /(jpg|png|bmp|gif|jpeg)$/;
			
			push @links, make_thumbnail_link($file, $CFG::settings{directory_www});
		}
		
		my $links_per_row = 5; # better abstraction in the next rev
		
		for (my $i = 0; $i < $#links; $i += $links_per_row) {
			my @local_links = @links[$i..$i+$links_per_row];
			print "<tr>";
			foreach my $link (@local_links) {
				print "<td>$link</td>";
			}
			print "</tr>";
		}
		
	} else {
		error ("couldn't open $CFG::parameters{directory}");
	}
	
	
	
}

## cleanup

exit;

## subs below


sub make_thumbnail_link {
	# make_thumbnail_link($ffp_of_image, $relative_www_accessible_path) - returns an <a href=""></a> HTML string or 0
	# example: make_thumbnail_link('/home/conor/git/ndb/diffs/this_is_an_image.jpg', '/ndb/') returns 'NEED TO FINISH THIS EXAMPLE'
	my ($ffp, $dir_www) = @_;
	my $fname = Basename($ffp);
	my $dir_local = $ffp =~ s/$fname//;
	my $results = 0;
	
	my $path_www = $dir_www . $fname;
	
	my $x = 30;
	my $y = 30;
	
	$results = "<a href='$path_www'><img src='$path_www' height=$y width=$x><br>$fname</a>";
	
	return $results;
}

sub error {
	# error ($message) -- prints $message in large red text
	my $message = shift;
	
	print "<h2><font color='red'>ERROR: $message</font></h2>";
	
	return;
}

sub get_xml {
	# get_xml($ffp) - returns %hash of $ffp or 0
	my $ffp = shift;
	
	return 0 unless -r $ffp;
	
	my $worker = XML::Simple->new();
	my $doc;
	
	eval {
		$doc = $worker->XMLin($ffp);
	};
	
	if ($@) {
		warn "WARN:: unable to use '$ffp': $@";
		return 0;
	}
	
	return %{$doc};
}