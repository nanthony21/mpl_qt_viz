# mpl_qt_viz.roiSelection.AxManager


### class mpl_qt_viz.roiSelection.AxManager(ax)
Bases: `object`

An object to manage multiple selector tools on a single axes. Only one of these should exist per Axes object.


* **Parameters**

    **ax** (`Axes`) – The matplotlib Axes object to draw on.



#### addArtist(artist)
Adds an artist to the manager.


* **Parameters**

    **artist** (`Artist`) – A new matplotlib Artist to be managed.



#### removeArtist(artist)
Remove a single Artist from the manaager


* **Parameters**

    **artist** (`Artist`) – A previously added matplotlib Artist.



#### update()
Re-render the axes. Call this after you know that something has changed with the plot.
