This SOURCES directory
----------------------

Only add-on source elements are included in this repository. Upstream source
archives can be found at the link listed below this paragraph.

<https://github.com/laurent22/joplin/releases/>

See also, the Source0 value in the `.spec` files. Like this, for example:

<https://github.com/laurent22/joplin/archive/v2.3.5/joplin-2.3.5.tar.gz>

Binary-based upstream will be the AppImage of the appropriate release, for example, like this:

<https://github.com/laurent22/joplin/releases/download/v2.3.5/Joplin-2.3.5.AppImage>

---

I have also experimented with retaining a copy of the AppImage in the SOURCES directory.
So that github doesn't get upset, I have to share the binary using `split` and then
recombine the shares into an AppImage using `cat`. Kinda like this.

`split -n 16 Joplin-2.3.5.AppImage Joplin-2.3.5.AppImage-`  
... that produces files `Joplin-2.3.5.AppImage-aa through `Joplin-2.3.5.AppImage-ap`

They are stitched back together during the RPM build with, essentially:
  `cat Joplin-2.3.5.AppImage-* > Joplin-2.3.5.AppImage`

