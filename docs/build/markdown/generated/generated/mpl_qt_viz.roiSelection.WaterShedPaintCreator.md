# mpl_qt_viz.roiSelection.WaterShedPaintCreator


### class mpl_qt_viz.roiSelection.WaterShedPaintCreator(axMan, im, onselect=None)
Bases: `mpl_qt_viz.roiSelection._creatorWidgets._base.CreatorWidgetBase`

Uses Watershed technique in an attempt to highlight all bright selectable regions in a fluorescence image.


* **Parameters**

    
    * **axMan** (*AxManager*) – The manager for a matplotlib Axes that you want to interact with.


    * **im** (*AxesImage*) – A reference to a matplotlib AxesImage. The data from this object is used to detect bright regions.


    * **onselect** – A callback that will be called when the user hits ‘enter’. Should have signature (polygonCoords, sparseHandleCoords).



#### property active()
Is the widget active?


#### addArtist(artist)
Add a matplotlib artist to be managed.


#### connect_event(event, callback)
Connect callback with an event.

This should be used in lieu of `figure.canvas.mpl_connect` since this
function stores callback ids for later clean up.


#### disconnect_events()
Disconnect all events created by this widget.


#### static getHelpText()
Return a description of the selector which can be used as a tooltip.


#### get_active()
Get whether the widget is active.


#### ignore(event)
return *True* if *event* should be ignored. No event callbacks will be called if this returns true.


#### on_key_press(event)
Key press event handler and validator for all selection widgets


#### on_key_release(event)
Key release event handler and validator


#### on_scroll(event)
Mouse scroll event handler and validator


#### onmove(event)
Cursor move event handler and validator


#### onselect(verts, handles)
This method should be called when the interaction is done to execute whatever finalization function was specified
in the constructor.


* **Parameters**

    
    * **verts** (*PolygonCoords*) – A sequence of 2-tuple coordinates that fully define the polygon.


    * **handles** (*PolygonCoords*) – A reduced sequence of coordinates that define special points onthe shape to potentially be used as draggable handles for a modifier.



#### paint(forceRedraw=True)
Refresh the detected regions.


* **Parameters**

    **forceRedraw** (`bool`) – If True then polygons will be cleared and redrawn even if we don’t detect that our status is stale



#### press(event)
Button press handler and validator


#### release(event)
Button release event handler and validator


#### removeArtists()
Remove all artist objects associated with this selector


#### reset()
Reset the state of the selector so it’s ready for a new selection.


#### setArtistVisible(artist, visible)
set visibility of a single artist, invisible artists will not be reenabled with set_visible True.


#### set_active(active)
Set whether the widget is active.


#### set_visible(visible)
Set the visibility of our artists
