## Additions to Upstream Joplin

This archive supplies additions to Joplin upstream and are used to flesh out
the Joplin package build. Fedora and the linux desktop standards (LSB, etc) and the linux package standards require more than upstream provides. Namely,

1. Additional desktop icons. In particular high-contrast icons for the visually
   impaired and a missing 64px hicolor icon. Note, I pull-requested them
   upstream, but upstream rejected them as sometime they did not want to
   additionally maintain. Fair enough. So here they remain. Note, the standard is
   64, 128, 256, and 512px images (and an svg) and only those are added.
2. A complete metainfo.xml (appstream data) file.
3. All the upstream source bits that need to be included if we build from
   binary, but don't want to include the entire upstream source as well.
   Namely, upstream icons, license text. This way, if we are forced to build
   packages from pre-built binaries, the SRPM isn't doubled in size. Note, the
   standard for included icons are 64, 128, 256, and 512px images (and an svg)
   and only those are copied over (I provide the missing 64px hicolor icon in the
   desktop-icons folder.


The RPM will place the icons in
```
/usr/share/icons/HighContrast/NNNxNNN/apps/org.joplinapp.joplin.png
/usr/share/icons/HighContrast/scalable/apps/org.joplinapp.joplin.svg
```

Note, a flatpak build (a project I am sometimes working on) will place them in
```
/app/share/icons/HighContrast/NNNxNNN/apps/org.joplinapp.joplin.png
/app/share/icons/HighContrast/scalable/apps/org.joplinapp.joplin.svg
```


Some links:

* https://www.freedesktop.org/software/appstream/docs/chap-Metadata.html
* https://en.wikipedia.org/wiki/Linux_Standard_Base
* https://docs.fedoraproject.org/en-US/packaging-guidelines/
