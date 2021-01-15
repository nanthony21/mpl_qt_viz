# mpl_qt_viz.roiSelection.AdjustableSelector


### class mpl_qt_viz.roiSelection.AdjustableSelector(axManager, image, selectorClass, onfinished=None, onPolyTuningCancelled=None)
Bases: `object`

This class manages an roi selector. By setting adjustable true then when the selector calls its onselect function
the results will be passed on to a PolygonInteractor for further tweaking. Tweaking can be confirmed by pressing enter.
at the end the selector will pass a set of coordinates to the onfinished function if it has been set.


* **Parameters**

    
    * **ax** – A matplotlib Axes to interact with.


    * **image** (*AxesImage*) – A matplotlib AxesImage. Some selectors use the data in this image for their selection.


    * **selectorClass** (*typing.Type**[**CreatorWidgetBase**]*) – A class that implements SelectorWidgetBase. This will be the intial selector used.


    * **onfinished** (*typing.Optional**[**typing.Callable**]*) – a callback function when the selection finished. The function should accept a single input argument
    which is a list of the 2d coordinated outlining the selected polygon.



#### property adjustable()
Determines whether or not the polygon interactor will be used to adjust the selection at the end of the initial
selection.


* **Return type**

    `bool`



#### finish(verts, handles)
This callback is registered with the selectorWidget when we are not in adjustable mode. In adjustable mode it
is instead registered with the polygon adjuster. It deactivates the class and calls the onfinished callback.


#### reset()
Clear all artists used by the selector. :todo: Shouldn’t this check if the adjuster is active and reset it as well?


#### setActive(active)
This activates the selector. for a looping selection you should call this method from the onfinished function.


#### setSelector(selectorClass)
Remove the current selector and replace it with a new type of selector.


* **Parameters**

    **selectorClass** (`Type`) – A class the implements SelectorWidgetBase.
