The upstream app is missing highcontrast icons. I created them here. I
submitted them to the project, but the project lead did not want another set of
icons to maintain. So, here they remain.

I also added two commonly expected hicolor icons: 64px and scalable.

The RPM should place the icons in
```
/usr/share/icons/HighContrast/NNNxNNN/apps/org.joplinapp.joplin.png
/usr/share/icons/HighContrast/scalable/apps/org.joplinapp.joplin.svg
```

Note, a flatpak build will place them in
```
/app/share/icons/HighContrast/NNNxNNN/apps/org.joplinapp.joplin.png
/app/share/icons/HighContrast/scalable/apps/org.joplinapp.joplin.svg
```

