Only add-on source elements are included in this repository. Upstream source
archives can be found at the link listed below. See also, the Source0 and
Source1 values in the `.spec` files.
- <https://github.com/laurent22/joplin/releases/>

For pre-built binaries as source, I have to split them up so that github
doesn't revolt.

For example, `split -n 16 Joplin-2.3.5.AppImage Joplin-2.3.5.AppImage-` produces:
  `Joplin-2.3.5.AppImage-aa through `Joplin-2.3.5.AppImage-ap`

They are stitched back together during the RPM build with, essentially:
  `cat Joplin-2.3.5.AppImage-* > Joplin-2.3.5.AppImage`
