# mpl_qt_viz.visualizers.PlotNdCanvas


### class mpl_qt_viz.visualizers.PlotNdCanvas(data, names, initialCoords=None, indices=None, cmap=<matplotlib.colors.LinearSegmentedColormap object>)
Bases: `matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg`

The matplotlib canvas for the PlotND widget.


* **Parameters**

    
    * **data** (`ndarray`) – 3D or greater numeric data


    * **names** (`Tuple`[`str`, …]) – The names to label each dimension of the data with.


    * **initialCoords** (`Optional`[`Tuple`[`int`, …]]) – An optional tuple of coordinates to set the Nd crosshair to.


    * **indices** (`Optional`[`List`]) – An optional tuple of 1d arrays of values to set as the indexes for each dimension of the data.



#### class PaintDeviceMetric()
Bases: `int`


#### class RenderFlag()
Bases: `int`


#### class RenderFlags()
Bases: `sip.simplewrapper`

QWidget.RenderFlags(Union[QWidget.RenderFlags, QWidget.RenderFlag])
QWidget.RenderFlags(QWidget.RenderFlags)


#### acceptDrops(self)

#### accessibleDescription(self)

#### accessibleName(self)

#### actionEvent(self, QActionEvent)

#### actions(self)

#### activateWindow(self)

#### addAction(self, QAction)

#### addActions(self, Iterable[QAction])

#### adjustSize(self)

#### autoFillBackground(self)

#### backgroundRole(self)

#### baseSize(self)

#### blit(bbox=None)
Blit the canvas in bbox (default entire canvas).


#### blockSignals(self, bool)

#### buffer_rgba()
Get the image as a memoryview to the renderer’s buffer.

draw must be called at least once before this function will work and
to update the renderer for any subsequent changes to the Figure.


#### button_press_event(x, y, button, dblclick=False, guiEvent=None)
Callback processing for mouse button press events.

Backend derived classes should call this function on any mouse
button press.  (*x*, *y*) are the canvas coords ((0, 0) is lower left).
button and key are as defined in MouseEvent.

This method will call all functions connected to the
‘button_press_event’ with a MouseEvent instance.


#### button_release_event(x, y, button, guiEvent=None)
Callback processing for mouse button release events.

Backend derived classes should call this function on any mouse
button release.

This method will call all functions connected to the
‘button_release_event’ with a MouseEvent instance.


* **Parameters**

    
    * **x** (*float*) – The canvas coordinates where 0=left.


    * **y** (*float*) – The canvas coordinates where 0=bottom.


    * **guiEvent** – The native UI event that generated the Matplotlib event.



#### changeEvent(self, QEvent)

#### childAt(self, QPoint)
childAt(self, int, int) -> QWidget


#### children(self)

#### childrenRect(self)

#### childrenRegion(self)

#### clearFocus(self)

#### clearMask(self)

#### close(self)

#### closeEvent(self, QCloseEvent)

#### close_event(guiEvent=None)
Pass a CloseEvent to all functions connected to `close_event`.


#### colorCount(self)

#### contentsMargins(self)

#### contentsRect(self)

#### contextMenuEvent(self, QContextMenuEvent)

#### contextMenuPolicy(self)

#### create(self, window: sip.voidptr = 0, initializeWindow: bool = True, destroyOldWindow: bool = True)

#### createWindowContainer(QWindow, parent: QWidget = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = 0)

#### cursor(self)

#### customContextMenuRequested()
customContextMenuRequested(self, QPoint) [signal]


#### deleteLater(self)

#### depth(self)

#### destroy(self, destroyWindow: bool = True, destroySubWindows: bool = True)

#### destroyed()
QObject = None) [signal]


* **Type**

    destroyed(self, object



#### devType(self)

#### devicePixelRatio(self)

#### devicePixelRatioF(self)

#### devicePixelRatioFScale()

#### disconnect(QMetaObject.Connection)
disconnect(self)


#### dragEnterEvent(self, QDragEnterEvent)

#### dragLeaveEvent(self, QDragLeaveEvent)

#### dragMoveEvent(self, QDragMoveEvent)

#### draw()
Render the .Figure.


#### draw_cursor(event)
[*Deprecated*] Draw a cursor in the event.axes if inaxes is not None.  Use
native GUI drawing for efficiency if possible

### Notes

**Deprecated:** Deprecated since version 3.2.


#### draw_event(renderer)
Pass a DrawEvent to all functions connected to `draw_event`.


#### draw_idle()
Queue redraw of the Agg buffer and request Qt paintEvent.


#### dropEvent(self, QDropEvent)

#### dumpObjectInfo(self)

#### dumpObjectTree(self)

#### dynamicPropertyNames(self)

#### effectiveWinId(self)

#### ensurePolished(self)

#### enterEvent(self, QEvent)

#### enter_notify_event(guiEvent=None, xy=None)
Callback processing for the mouse cursor entering the canvas.

Backend derived classes should call this function when entering
canvas.


* **Parameters**

    
    * **guiEvent** – The native UI event that generated the Matplotlib event.


    * **xy** (*(**float**, **float**)*) – The coordinate location of the pointer when the canvas is entered.



#### event(self, QEvent)

#### eventFilter(self, QObject, QEvent)

#### find(sip.voidptr)

#### findChild(self, type, name: str = '', options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively)
findChild(self, Tuple, name: str = ‘’, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> QObject


#### findChildren(self, type, name: str = '', options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively)
findChildren(self, Tuple, name: str = ‘’, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> List[QObject]
findChildren(self, type, QRegExp, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> List[QObject]
findChildren(self, Tuple, QRegExp, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> List[QObject]
findChildren(self, type, QRegularExpression, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> List[QObject]
findChildren(self, Tuple, QRegularExpression, options: Union[Qt.FindChildOptions, Qt.FindChildOption] = Qt.FindChildrenRecursively) -> List[QObject]


#### flush_events()
Flush the GUI events for the figure.

Interactive backends need to reimplement this method.


#### focusInEvent(self, QFocusEvent)

#### focusNextChild(self)

#### focusNextPrevChild(self, bool)

#### focusOutEvent(self, QFocusEvent)

#### focusPolicy(self)

#### focusPreviousChild(self)

#### focusProxy(self)

#### focusWidget(self)

#### font(self)

#### fontInfo(self)

#### fontMetrics(self)

#### foregroundRole(self)

#### frameGeometry(self)

#### frameSize(self)

#### geometry(self)

#### getContentsMargins(self)

#### get_default_filename()
Return a string, which includes extension, suitable for use as
a default filename.


#### classmethod get_default_filetype()
Return the default savefig file format as specified in


```
:rc:`savefig.format`
```

.

The returned string does not include a period. This method is
overridden in backends that only support a single file type.


#### classmethod get_supported_filetypes()
Return dict of savefig file formats supported by this backend.


#### classmethod get_supported_filetypes_grouped()
Return a dict of savefig file formats supported by this backend,
where the keys are a file type name, such as ‘Joint Photographic
Experts Group’, and the values are a list of filename extensions used
for that filetype, such as [‘jpg’, ‘jpeg’].


#### get_width_height()
Return the figure width and height in points or pixels
(depending on the backend), truncated to integers.


#### get_window_title()
Return the title text of the window containing the figure, or None
if there is no window (e.g., a PS backend).


#### grab(self, rectangle: QRect = QRect(QPoint(0, 0), QSize(- 1, - 1)))

#### grabGesture(self, Qt.GestureType, flags: Union[Qt.GestureFlags, Qt.GestureFlag] = Qt.GestureFlags())

#### grabKeyboard(self)

#### grabMouse(self)
grabMouse(self, Union[QCursor, Qt.CursorShape])


#### grabShortcut(self, Union[QKeySequence, QKeySequence.StandardKey, str, int], context: Qt.ShortcutContext = Qt.WindowShortcut)

#### grab_mouse(ax)
Set the child ~.axes.Axes which is grabbing the mouse events.

Usually called by the widgets themselves. It is an error to call this
if the mouse is already grabbed by another axes.


#### graphicsEffect(self)

#### graphicsProxyWidget(self)

#### hasFocus(self)

#### hasHeightForWidth(self)

#### hasMouseTracking(self)

#### hasTabletTracking(self)

#### height(self)

#### heightForWidth(self, int)

#### heightMM(self)

#### hide(self)

#### hideEvent(self, QHideEvent)

#### inaxes(xy)
Return the topmost visible ~.axes.Axes containing the point *xy*.


* **Parameters**

    **xy** (*(**float**, **float**)*) – (x, y) pixel positions from left/bottom of the canvas.



* **Returns**

    The topmost visible axes containing the point, or None if no axes.



* **Return type**

    ~matplotlib.axes.Axes or None



#### inherits(self, str)

#### initPainter(self, QPainter)

#### inputMethodEvent(self, QInputMethodEvent)

#### inputMethodHints(self)

#### inputMethodQuery(self, Qt.InputMethodQuery)

#### PlotNdCanvas.insertAction(self, QAction, QAction)()

#### insertActions(self, QAction, Iterable[QAction])

#### installEventFilter(self, QObject)

#### isActiveWindow(self)

#### isAncestorOf(self, QWidget)

#### isEnabled(self)

#### isEnabledTo(self, QWidget)

#### isFullScreen(self)

#### isHidden(self)

#### isLeftToRight(self)

#### isMaximized(self)

#### isMinimized(self)

#### isModal(self)

#### isRightToLeft(self)

#### isVisible(self)

#### isVisibleTo(self, QWidget)

#### isWidgetType(self)

#### isWindow(self)

#### isWindowModified(self)

#### isWindowType(self)

#### is_saving()
Return whether the renderer is in the process of saving
to a file, rather than rendering for an on-screen buffer.


#### keyPressEvent(self, QKeyEvent)

#### keyReleaseEvent(self, QKeyEvent)

#### key_press_event(key, guiEvent=None)
Pass a KeyEvent to all functions connected to `key_press_event`.


#### key_release_event(key, guiEvent=None)
Pass a KeyEvent to all functions connected to `key_release_event`.


#### keyboardGrabber()

#### killTimer(self, int)

#### layout(self)

#### layoutDirection(self)

#### leaveEvent(self, QEvent)

#### leave_notify_event(guiEvent=None)
Callback processing for the mouse cursor leaving the canvas.

Backend derived classes should call this function when leaving
canvas.


* **Parameters**

    **guiEvent** – The native UI event that generated the Matplotlib event.



#### locale(self)

#### logicalDpiX(self)

#### logicalDpiY(self)

#### lower(self)

#### mapFrom(self, QWidget, QPoint)

#### mapFromGlobal(self, QPoint)

#### mapFromParent(self, QPoint)

#### mapTo(self, QWidget, QPoint)

#### mapToGlobal(self, QPoint)

#### mapToParent(self, QPoint)

#### mask(self)

#### maximumHeight(self)

#### maximumSize(self)

#### maximumWidth(self)

#### metaObject(self)

#### metric(self, QPaintDevice.PaintDeviceMetric)

#### minimumHeight(self)

#### minimumSize(self)

#### minimumSizeHint(self)

#### minimumWidth(self)

#### motion_notify_event(x, y, guiEvent=None)
Callback processing for mouse movement events.

Backend derived classes should call this function on any
motion-notify-event.

This method will call all functions connected to the
‘motion_notify_event’ with a MouseEvent instance.


* **Parameters**

    
    * **x** (*float*) – The canvas coordinates where 0=left.


    * **y** (*float*) – The canvas coordinates where 0=bottom.


    * **guiEvent** – The native UI event that generated the Matplotlib event.



#### mouseDoubleClickEvent(self, QMouseEvent)

#### mouseEventCoords(pos)
Calculate mouse coordinates in physical pixels.

Qt5 use logical pixels, but the figure is scaled to physical
pixels for rendering.  Transform to physical pixels so that
all of the down-stream transforms work as expected.

Also, the origin is different and needs to be corrected.


#### mouseGrabber()

#### mouseMoveEvent(self, QMouseEvent)

#### mousePressEvent(self, QMouseEvent)

#### mouseReleaseEvent(self, QMouseEvent)

#### move(self, QPoint)
move(self, int, int)


#### moveEvent(self, QMoveEvent)

#### moveToThread(self, QThread)

#### mpl_connect(s, func)
Bind function *func* to event *s*.


* **Parameters**

    
    * **s** (*str*) – One of the following events ids:


        * ’button_press_event’


        * ’button_release_event’


        * ’draw_event’


        * ’key_press_event’


        * ’key_release_event’


        * ’motion_notify_event’


        * ’pick_event’


        * ’resize_event’


        * ’scroll_event’


        * ’figure_enter_event’,


        * ’figure_leave_event’,


        * ’axes_enter_event’,


        * ’axes_leave_event’


        * ’close_event’.



    * **func** (*callable*) – The callback function to be executed, which must have the
    signature:

    ```
    def func(event: Event) -> Any
    ```

    For the location events (button and key press/release), if the
    mouse is over the axes, the `inaxes` attribute of the event will
    be set to the ~matplotlib.axes.Axes the event occurs is over, and
    additionally, the variables `xdata` and `ydata` attributes will
    be set to the mouse location in data coordinates.  See .KeyEvent
    and .MouseEvent for more info.




* **Returns**

    A connection id that can be used with
    .FigureCanvasBase.mpl_disconnect.



* **Return type**

    cid


### Examples

```
def on_press(event):
    print('you pressed', event.button, event.xdata, event.ydata)

cid = canvas.mpl_connect('button_press_event', on_press)
```


#### mpl_disconnect(cid)
Disconnect the callback with id *cid*.

### Examples

```
cid = canvas.mpl_connect('button_press_event', on_press)
# ... later
canvas.mpl_disconnect(cid)
```


#### nativeEvent(self, Union[QByteArray, bytes, bytearray], sip.voidptr)

#### nativeParentWidget(self)

#### new_timer(interval=None, callbacks=None)
Create a new backend-specific subclass of .Timer.

This is useful for getting periodic events through the backend’s native
event loop.  Implemented only for backends with GUIs.


* **Parameters**

    
    * **interval** (*int*) – Timer interval in milliseconds.


    * **callbacks** (*List**[**Tuple**[**callable**, **Tuple**, **Dict**]**]*) – Sequence of (func, args, kwargs) where `func(\*args, \*\*kwargs)`
    will be executed by the timer every *interval*.

    Callbacks which return `False` or `0` will be removed from the
    timer.



### Examples

```python
>>> timer = fig.canvas.new_timer(callbacks=[(f1, (1,), {'a': 3})])
```


#### nextInFocusChain(self)

#### normalGeometry(self)

#### objectName(self)

#### objectNameChanged()
objectNameChanged(self, str) [signal]


#### overrideWindowFlags(self, Union[Qt.WindowFlags, Qt.WindowType])

#### overrideWindowState(self, Union[Qt.WindowStates, Qt.WindowState])

#### paintEngine(self)

#### paintEvent(event)
Copy the image from the Agg canvas to the qt.drawable.

In Qt, all drawing should be done inside of here when a widget is
shown onscreen.


#### paintingActive(self)

#### palette(self)

#### parent(self)

#### parentWidget(self)

#### performBlit()
Re-render the axes efficiently using matplotlib blitting.


#### physicalDpiX(self)

#### physicalDpiY(self)

#### pick_event(mouseevent, artist, \*\*kwargs)
Callback processing for pick events.

This method will be called by artists who are picked and will
fire off PickEvent callbacks registered listeners.


#### pos(self)

#### previousInFocusChain(self)

#### print_figure(\*args, \*\*kwargs)
Render the figure to hardcopy. Set the figure patch face and edge
colors.  This is useful because some of the GUIs have a gray figure
face color background and you’ll probably want to override this on
hardcopy.


* **Parameters**

    
    * **filename** (*str** or **path-like** or **file-like*) – The file where the figure is saved.


    * **dpi** (float, default: 

    ```
    :rc:`savefig.dpi`
    ```

    ) – The dots per inch to save the figure in.


    * **facecolor** (color or ‘auto’, default: 

    ```
    :rc:`savefig.facecolor`
    ```

    ) – The facecolor of the figure.  If ‘auto’, use the current figure
    facecolor.


    * **edgecolor** (color or ‘auto’, default: 

    ```
    :rc:`savefig.edgecolor`
    ```

    ) – The edgecolor of the figure.  If ‘auto’, use the current figure
    edgecolor.


    * **orientation** (*{'landscape'**, **'portrait'}**, **default: 'portrait'*) – Only currently applies to PostScript printing.


    * **format** (*str**, **optional*) – Force a specific file format. If not given, the format is inferred
    from the *filename* extension, and if that fails from


    ```
    :rc:`savefig.format`
    ```

    .


    * **bbox_inches** (‘tight’ or .Bbox, default: 

    ```
    :rc:`savefig.bbox`
    ```

    ) – Bounding box in inches: only the given portion of the figure is
    saved.  If ‘tight’, try to figure out the tight bbox of the figure.


    * **pad_inches** (float, default: 

    ```
    :rc:`savefig.pad_inches`
    ```

    ) – Amount of padding around the figure when *bbox_inches* is ‘tight’.


    * **bbox_extra_artists** (list of ~matplotlib.artist.Artist, optional) – A list of extra artists that will be considered when the
    tight bbox is calculated.


    * **backend** (*str**, **optional*) – Use a non-default backend to render the file, e.g. to render a
    png file with the “cairo” backend rather than the default “agg”,
    or a pdf file with the “pgf” backend rather than the default
    “pdf”.  Note that the default backend is normally sufficient.  See
    the-builtin-backends for a list of valid backends for each
    file format.  Custom backends can be referenced as “module://…”.



#### print_jpeg(filename_or_obj, \*args, dryrun=<deprecated parameter>, pil_kwargs=None, \*\*kwargs)
Write the figure to a JPEG file.


* **Parameters**

    **filename_or_obj** (*str** or **path-like** or **file-like*) – The file to write to.



* **Other Parameters**

    
    * **quality** (int, default: 

    ```
    :rc:`savefig.jpeg_quality`
    ```

    ) – The image quality, on a scale from 1 (worst) to 95 (best).
    Values above 95 should be avoided; 100 disables portions of
    the JPEG compression algorithm, and results in large files
    with hardly any gain in image quality.  This parameter is
    deprecated.


    * **optimize** (*bool, default: False*) – Whether the encoder should make an extra pass over the image
    in order to select optimal encoder settings.  This parameter is
    deprecated.


    * **progressive** (*bool, default: False*) – Whether the image should be stored as a progressive JPEG file.
    This parameter is deprecated.


    * **pil_kwargs** (*dict, optional*) – Additional keyword arguments that are passed to
    PIL.Image.Image.save when saving the figure.  These take
    precedence over *quality*, *optimize* and *progressive*.



#### print_jpg(filename_or_obj, \*args, dryrun=<deprecated parameter>, pil_kwargs=None, \*\*kwargs)
Write the figure to a JPEG file.


* **Parameters**

    **filename_or_obj** (*str** or **path-like** or **file-like*) – The file to write to.



* **Other Parameters**

    
    * **quality** (int, default: 

    ```
    :rc:`savefig.jpeg_quality`
    ```

    ) – The image quality, on a scale from 1 (worst) to 95 (best).
    Values above 95 should be avoided; 100 disables portions of
    the JPEG compression algorithm, and results in large files
    with hardly any gain in image quality.  This parameter is
    deprecated.


    * **optimize** (*bool, default: False*) – Whether the encoder should make an extra pass over the image
    in order to select optimal encoder settings.  This parameter is
    deprecated.


    * **progressive** (*bool, default: False*) – Whether the image should be stored as a progressive JPEG file.
    This parameter is deprecated.


    * **pil_kwargs** (*dict, optional*) – Additional keyword arguments that are passed to
    PIL.Image.Image.save when saving the figure.  These take
    precedence over *quality*, *optimize* and *progressive*.



#### print_png(filename_or_obj, \*args, metadata=None, pil_kwargs=None)
Write the figure to a PNG file.


* **Parameters**

    
    * **filename_or_obj** (*str** or **path-like** or **file-like*) – The file to write to.


    * **metadata** (*dict**, **optional*) – Metadata in the PNG file as key-value pairs of bytes or latin-1
    encodable strings.
    According to the PNG specification, keys must be shorter than 79
    chars.

    The [PNG specification](https://www.w3.org/TR/2003/REC-PNG-20031110/#11keywords) defines some common keywords that may be
    used as appropriate:


        * Title: Short (one line) title or caption for image.


        * Author: Name of image’s creator.


        * Description: Description of image (possibly long).


        * Copyright: Copyright notice.


        * Creation Time: Time of original image creation
    (usually RFC 1123 format).


        * Software: Software used to create the image.


        * Disclaimer: Legal disclaimer.


        * Warning: Warning of nature of content.


        * Source: Device used to create the image.


        * Comment: Miscellaneous comment;
    conversion from other image format.

    Other keywords may be invented for other purposes.

    If ‘Software’ is not given, an autogenerated value for Matplotlib
    will be used.  This can be removed by setting it to *None*.

    For more details see the [PNG specification](https://www.w3.org/TR/2003/REC-PNG-20031110/#11keywords).



    * **pil_kwargs** (*dict**, **optional*) – Keyword arguments passed to PIL.Image.Image.save.

    If the ‘pnginfo’ key is present, it completely overrides
    *metadata*, including the default ‘Software’ key.




#### property(self, str)

#### pyqtConfigure(...)
Each keyword argument is either the name of a Qt property or a Qt signal.
For properties the property is set to the given value which should be of an
appropriate type.
For signals the signal is connected to the given value which should be a
callable.


#### raise_(self)

#### rect(self)

#### releaseKeyboard(self)

#### releaseMouse(self)

#### releaseShortcut(self, int)

#### release_mouse(ax)
Release the mouse grab held by the ~.axes.Axes *ax*.

Usually called by the widgets. It is ok to call this even if *ax*
doesn’t have the mouse grab currently.


#### removeAction(self, QAction)

#### removeEventFilter(self, QObject)

#### render(self, QPaintDevice, targetOffset: QPoint = QPoint(), sourceRegion: QRegion = QRegion(), flags: Union[QWidget.RenderFlags, QWidget.RenderFlag] = QWidget.RenderFlags(QWidget.RenderFlag.DrawWindowBackground | QWidget.RenderFlag.DrawChildren))
render(self, QPainter, targetOffset: QPoint = QPoint(), sourceRegion: QRegion = QRegion(), flags: Union[QWidget.RenderFlags, QWidget.RenderFlag] = QWidget.RenderFlags(QWidget.RenderFlag.DrawWindowBackground|QWidget.RenderFlag.DrawChildren))


#### repaint(self)
repaint(self, int, int, int, int)
repaint(self, QRect)
repaint(self, QRegion)


#### resize(self, QSize)
resize(self, int, int)


#### resizeEvent(self, QResizeEvent)

#### resize_event()
Pass a ResizeEvent to all functions connected to `resize_event`.


#### restoreGeometry(self, Union[QByteArray, bytes, bytearray])

#### rollAxes()
Change the order of the axes of the data. Allows viewing the sideview of the data.


#### saveGeometry(self)

#### screen(self)

#### PlotNdCanvas.scroll(self, int, int)()
scroll(self, int, int, QRect)


#### scroll_event(x, y, step, guiEvent=None)
Callback processing for scroll events.

Backend derived classes should call this function on any
scroll wheel event.  (*x*, *y*) are the canvas coords ((0, 0) is lower
left).  button and key are as defined in MouseEvent.

This method will call all functions connected to the ‘scroll_event’
with a MouseEvent instance.


#### setAcceptDrops(self, bool)

#### setAccessibleDescription(self, str)

#### setAccessibleName(self, str)

#### setAttribute(self, Qt.WidgetAttribute, on: bool = True)

#### setAutoFillBackground(self, bool)

#### setAxesNames(names)
Set the names of to label each plot.
:type names: `Iterable`[`str`]
:param names: the order of the names should match the order of each corresponding axis in the data array.


#### setBackgroundRole(self, QPalette.ColorRole)

#### PlotNdCanvas.setBaseSize(self, int, int)()
setBaseSize(self, QSize)


#### PlotNdCanvas.setContentsMargins(self, int, int, int, int)()
setContentsMargins(self, QMargins)


#### setContextMenuPolicy(self, Qt.ContextMenuPolicy)

#### setCursor(self, Union[QCursor, Qt.CursorShape])

#### setDisabled(self, bool)

#### setEnabled(self, bool)

#### setFixedHeight(self, int)

#### setFixedSize(self, QSize)
setFixedSize(self, int, int)


#### setFixedWidth(self, int)

#### setFocus(self)
setFocus(self, Qt.FocusReason)


#### setFocusPolicy(self, Qt.FocusPolicy)

#### setFocusProxy(self, QWidget)

#### setFont(self, QFont)

#### setForegroundRole(self, QPalette.ColorRole)

#### setGeometry(self, QRect)
setGeometry(self, int, int, int, int)


#### setGraphicsEffect(self, QGraphicsEffect)

#### setHidden(self, bool)

#### setIndices(indices)
Set the index values for each dimension of the array.


* **Parameters**

    **indices** (`Sequence`[`Sequence`[`float`]]) – A list or tuple of index values for each dimension of the data array.



#### setInputMethodHints(self, Union[Qt.InputMethodHints, Qt.InputMethodHint])

#### setLayout(self, QLayout)

#### setLayoutDirection(self, Qt.LayoutDirection)

#### setLocale(self, QLocale)

#### setMask(self, QBitmap)
setMask(self, QRegion)


#### setMaximumHeight(self, int)

#### PlotNdCanvas.setMaximumSize(self, int, int)()
setMaximumSize(self, QSize)


#### setMaximumWidth(self, int)

#### setMinimumHeight(self, int)

#### PlotNdCanvas.setMinimumSize(self, int, int)()
setMinimumSize(self, QSize)


#### setMinimumWidth(self, int)

#### setMouseTracking(self, bool)

#### setObjectName(self, str)

#### setPalette(self, QPalette)

#### setParent(self, QWidget)
setParent(self, QWidget, Union[Qt.WindowFlags, Qt.WindowType])


#### setProperty(self, str, Any)

#### setShortcutAutoRepeat(self, int, enabled: bool = True)

#### setShortcutEnabled(self, int, enabled: bool = True)

#### PlotNdCanvas.setSizeIncrement(self, int, int)()
setSizeIncrement(self, QSize)


#### setSizePolicy(self, QSizePolicy)
setSizePolicy(self, QSizePolicy.Policy, QSizePolicy.Policy)


#### setSpectraViewActive(active)
Determines whether or not the Nd crosshair respons to mouse input. Allows us to disable the crosshair if we
want the mouse to trigger other sorts of actions (e.g. ROI drawing)


#### setStatusTip(self, str)

#### setStyle(self, QStyle)

#### setStyleSheet(self, str)

#### PlotNdCanvas.setTabOrder(QWidget, QWidget)()

#### setTabletTracking(self, bool)

#### setToolTip(self, str)

#### setToolTipDuration(self, int)

#### setUpdatesEnabled(self, bool)

#### setVisible(self, bool)

#### setWhatsThis(self, str)

#### setWindowFilePath(self, str)

#### setWindowFlag(self, Qt.WindowType, on: bool = True)

#### setWindowFlags(self, Union[Qt.WindowFlags, Qt.WindowType])

#### setWindowIcon(self, QIcon)

#### setWindowIconText(self, str)

#### setWindowModality(self, Qt.WindowModality)

#### setWindowModified(self, bool)

#### setWindowOpacity(self, float)

#### setWindowRole(self, str)

#### setWindowState(self, Union[Qt.WindowStates, Qt.WindowState])

#### setWindowTitle(self, str)

#### set_window_title(title)
Set the title text of the window containing the figure.  Note that
this has no effect if there is no window (e.g., a PS backend).


#### sharedPainter(self)

#### show(self)

#### showEvent(self, QShowEvent)

#### showFullScreen(self)

#### showMaximized(self)

#### showMinimized(self)

#### showNormal(self)

#### signalsBlocked(self)

#### size(self)

#### sizeHint(self)

#### sizeIncrement(self)

#### sizePolicy(self)

#### stackUnder(self, QWidget)

#### startTimer(self, int, timerType: Qt.TimerType = Qt.CoarseTimer)

#### start_event_loop(timeout=0)
Start a blocking event loop.

Such an event loop is used by interactive functions, such as
~.Figure.ginput and ~.Figure.waitforbuttonpress, to wait for
events.

The event loop blocks until a callback function triggers
stop_event_loop, or *timeout* is reached.

If *timeout* is 0 or negative, never timeout.

Only interactive backends need to reimplement this method and it relies
on flush_events being properly implemented.

Interactive backends should implement this in a more native way.


#### statusTip(self)

#### stop_event_loop(event=None)
Stop the current blocking event loop.

Interactive backends need to reimplement this to match
start_event_loop


#### style(self)

#### styleSheet(self)

#### switch_backends(FigureCanvasClass)
Instantiate an instance of FigureCanvasClass

This is used for backend switching, e.g., to instantiate a
FigureCanvasPS from a FigureCanvasGTK.  Note, deep copying is
not done, so any changes to one of the instances (e.g., setting
figure size or line props), will be reflected in the other


#### tabletEvent(self, QTabletEvent)

#### testAttribute(self, Qt.WidgetAttribute)

#### thread(self)

#### toolTip(self)

#### toolTipDuration(self)

#### tostring_argb()
Get the image as ARGB bytes.

draw must be called at least once before this function will work and
to update the renderer for any subsequent changes to the Figure.


#### tostring_rgb()
Get the image as RGB bytes.

draw must be called at least once before this function will work and
to update the renderer for any subsequent changes to the Figure.


#### tr(self, str, disambiguation: str = None, n: int = - 1)

#### underMouse(self)

#### ungrabGesture(self, Qt.GestureType)

#### unsetCursor(self)

#### unsetLayoutDirection(self)

#### unsetLocale(self)

#### update(self)
update(self, QRect)
update(self, QRegion)
update(self, int, int, int, int)


#### updateGeometry(self)

#### updateLimits(Max, Min)
Update the range of values displayed. Similar to the set_clim method of a matplotlib image.


* **Parameters**

    
    * **Max** (`float`) – The maximum value displayed


    * **Min** (`float`) – The minimum value displayed



#### updateMicroFocus(self)

#### updatePlots(blit=True)
This should be called after self.coords have been changed to update the data of each plot.


* **Parameters**

    **blit** – If True then drawing will be done more efficiently through blitting. Sometimes this needs to be false
    to trigger a full redraw though.



#### updatesEnabled(self)

#### visibleRegion(self)

#### whatsThis(self)

#### wheelEvent(self, QWheelEvent)

#### width(self)

#### widthMM(self)

#### winId(self)

#### window(self)

#### windowFilePath(self)

#### windowFlags(self)

#### windowHandle(self)

#### windowIcon(self)

#### windowIconChanged()
windowIconChanged(self, QIcon) [signal]


#### windowIconText(self)

#### windowIconTextChanged()
windowIconTextChanged(self, str) [signal]


#### windowModality(self)

#### windowOpacity(self)

#### windowRole(self)

#### windowState(self)

#### windowTitle(self)

#### windowTitleChanged()
windowTitleChanged(self, str) [signal]


#### windowType(self)

#### x(self)

#### y(self)
