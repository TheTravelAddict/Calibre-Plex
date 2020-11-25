# Calibre-Plex
Getting metadata in my Plex Audiobook libraries

This project revolves around tweaking Plex and Calibre so as to have better access to my audiobooks.

It is a simple Python Script that you run on demand; but would also work fine as a chron job.

One benefit from using Plex rather than another player, is that I can play my audiobooks from anywhere Plex runs, and it will pick up where I last left off, so I can move from listening on my phone whilst out and about, to then listening from the TV whilst I workout or cook.  
It works by reading the Calibre metadata and then altering the tags in the Mb4 files that Plex reads.  It also creates some additional files in the Calibre source tree that Plex picks up for postering purposes.

It does not use the Calibre API as I found that the Calibre API is blocking if Calibre is currently running; so instead it scrapes metadata from the calibre generated OPF files.
It puts a new tag in these OPF files to indicate that it has already run against the book in question.  This is nice, as if you later alter the metadata using Calibre, Calibre will remove this tag, causing my script to update the mb4 file with the new metadata.

It also pulls the Author's image off of goodreads.com - but requires you generate your own API key for this; so unless you have a goodreads account you should comment out those lines.

It would probably be way better to write a Plex Agent to read the Calibre data - but I have found exactly 0 documantation on creating Plex agents.  

In anycase - it works for me which is all that is important; and if anyone else finds it useful; then bonus for them.

In order for this to work, you will need to do the following:
1. set up a new Plex library of type Music, and select the "Store Track Progress" option under advanced.  Failing to do this means Plex will re-start the book each time you play it.
1. You may also choose to install the unofficial Audiobook agent (https://github.com/macr0dev/Audiobooks.bundle) which will help catch any missing metadata that did not make the tag list from Calibre.
1. Point the library at your Calibre root directory (on a mac that is usually ~/username/Calibre\ Library)
1. Populate Calibre with a single M4B file for each book that you want.
    1. If your audiobooks are not in M4B format then you can use Audiobook Builder (https://www.splasm.com/audiobookbuilder/) to convert them.
    1. If you have an e-reader version of the book already in Calibre, then you simply select the book in calibre and click on the "Add" Button and choose: "Add file to selected Book" then browse to your MB4 (you may have to select "All Files" from the file filter)
    1. If you don't have an e-reader version of the book, then you will first need to add a blank book to calibre and then populate the Metadata.
    
    Requires:
    * Python 3
    * Pillow
    * Mutagen
    * Beautiful Soup
    * a goodreads API key if you want it to also download the author's pic
