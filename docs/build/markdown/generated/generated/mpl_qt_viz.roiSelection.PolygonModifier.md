# mpl_qt_viz.roiSelection.PolygonModifier


### class mpl_qt_viz.roiSelection.PolygonModifier(axMan, onselect=None, onCancelled=None)
Bases: `mpl_qt_viz.roiSelection._modifierWidgets._base.ModifierWidgetBase`

A polygon editor.
[https://matplotlib.org/gallery/event_handling/poly_editor.html](https://matplotlib.org/gallery/event_handling/poly_editor.html)
Key-bindings:

> ‘d’ delete the vertex under point
> ‘i’ insert a vertex at point.  You must be within epsilon of the

> > line connecting two existing vertices


* **Parameters**

    
    * **axMan** (*AxManager*) – The manager for a matplotlib Axes that you want to interact with.


    * **onselect** (*typing.Optional**[**ModifierWidgetBase.SelectionFunction**]*) – A callback that will be called when the user hits ‘enter’. Should have signature (polygonCoords, sparseHandleCoords).



#### epsilon()
The pixel distance required to detect a mouse-over event.


* **Type**

    int



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


#### initialize(handles)
Given a set of points this will initialize the artists to them to begin modification.


* **Parameters**

    **handles** (`Sequence`[`Sequence`[`Tuple`[`float`, `float`]]]) – A sequence of 2d coordinates to intialize the polygon to. Each point will become a draggable handle



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

    
    * **verts** (`Sequence`[`Sequence`[`Tuple`[`float`, `float`]]]) – A sequence of sequences of 2-tuple coordinates that each fully define the polygon.


    * **handles** (`Sequence`[`Sequence`[`Tuple`[`float`, `float`]]]) – A sequence of reduced sequences of coordinates that define special points on each shape to potentially be used as draggable handles for a modifier.



#### press(event)
Button press handler and validator


#### release(event)
Button release event handler and validator


#### removeArtists()
Remove all artist objects associated with this selector


#### setArtistVisible(artist, visible)
set visibility of a single artist, invisible artists will not be reenabled with set_visible True.


#### set_active(active)
Set whether the widget is active.


#### set_visible(visible)
Set the visibility of our artists
