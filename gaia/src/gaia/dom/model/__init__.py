''' 
    ==========================================================
    The Gaia Document Object Model

    ----------------------------------------------------------
    Summary:
    ----------------------------------------------------------
    ref: http://wiki.gale.com/display/EDT/Source+Schema+Ideas
    ..in the following, the minus ("-") means "has"..

    Item - Document
         - Page
         - Chunk ("article-like")
         - Clip
         - Links (eg for related audio files? or links to other Documents, etc)

    Document - Info

    Page(implicitly in Document) - Info

    Chunk(on Pages) - Info

    Clip(on Page) - Info (mostly clip-coords data)

    Link - Info? (from Page/article or both?)


    ----------------------------------------------------------
    Notes:
    ----------------------------------------------------------
    An Item is a container.
    An Item contains one Document object, and possibly many
    Pages, Chunks and Clips

    Documents encapsulate the xml files
    Pages encapsulate the page data and the page-image files
    Chunks represent logical parts of Pages (eg one article spread across a number of (clips of) pages.)
    Clips are areas on one Page.
    Links are references to other files (including other docs, mp3 files, etc).
    ==========================================================
'''
