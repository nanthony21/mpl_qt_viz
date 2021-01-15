# mpl_qt_viz.visualizers.PlotNd


### class mpl_qt_viz.visualizers.PlotNd(data, names=None, initialCoords=None, title='', parent=None, indices=None)
Bases: `PyQt5.QtWidgets.QWidget`

A convenient widget for visualizing data that is 3D or greater. This is a standalone widget which extends the
functionality of PlotNdCanvas.


* **Parameters**

    
    * **data** (`ndarray`) – A 3D or greater numpy array of numeric values.


    * **names** (`Optional`[`Tuple`[`str`, …]]) – A sequence of labels for each axis of the data array.


    * **initialCoords** (`Optional`[`Tuple`[`int`, …]]) – An optional sequence of the coordinates to initially se the ND crosshair to. There should be one
    coordinate for each axis of the data array.


    * **title** (`Optional`[`str`]) – A title for the window.


    * **parent** (`Optional`[`QWidget`]) – The Qt Widget that serves as the parent for this widget.


    * **indices** (`Optional`[`List`[`ndarray`]]) – An optional tuple of 1d arrays of values to set as the indexes for each dimension of the data. Elements of the list can be set to None to skip
    setting a custom index for that dimension.



#### data()
A reference the the 3D or greater numpy array. This can be safely modified.


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

#### blockSignals(self, bool)

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

#### dropEvent(self, QDropEvent)

#### dumpObjectInfo(self)

#### dumpObjectTree(self)

#### dynamicPropertyNames(self)

#### effectiveWinId(self)

#### ensurePolished(self)

#### enterEvent(self, QEvent)

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

#### grab(self, rectangle: QRect = QRect(QPoint(0, 0), QSize(- 1, - 1)))

#### grabGesture(self, Qt.GestureType, flags: Union[Qt.GestureFlags, Qt.GestureFlag] = Qt.GestureFlags())

#### grabKeyboard(self)

#### grabMouse(self)
grabMouse(self, Union[QCursor, Qt.CursorShape])


#### grabShortcut(self, Union[QKeySequence, QKeySequence.StandardKey, str, int], context: Qt.ShortcutContext = Qt.WindowShortcut)

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

#### inherits(self, str)

#### initPainter(self, QPainter)

#### inputMethodEvent(self, QInputMethodEvent)

#### inputMethodHints(self)

#### inputMethodQuery(self, Qt.InputMethodQuery)

#### PlotNd.insertAction(self, QAction, QAction)()

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

#### keyPressEvent(self, QKeyEvent)

#### keyReleaseEvent(self, QKeyEvent)

#### keyboardGrabber()

#### killTimer(self, int)

#### layout(self)

#### layoutDirection(self)

#### leaveEvent(self, QEvent)

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

#### mouseDoubleClickEvent(self, QMouseEvent)

#### mouseGrabber()

#### mouseMoveEvent(self, QMouseEvent)

#### mousePressEvent(self, QMouseEvent)

#### mouseReleaseEvent(self, QMouseEvent)

#### move(self, QPoint)
move(self, int, int)


#### moveEvent(self, QMoveEvent)

#### moveToThread(self, QThread)

#### nativeEvent(self, Union[QByteArray, bytes, bytearray], sip.voidptr)

#### nativeParentWidget(self)

#### nextInFocusChain(self)

#### normalGeometry(self)

#### objectName(self)

#### objectNameChanged()
objectNameChanged(self, str) [signal]


#### overrideWindowFlags(self, Union[Qt.WindowFlags, Qt.WindowType])

#### overrideWindowState(self, Union[Qt.WindowStates, Qt.WindowState])

#### paintEngine(self)

#### paintEvent(self, QPaintEvent)

#### paintingActive(self)

#### palette(self)

#### parent(self)

#### parentWidget(self)

#### physicalDpiX(self)

#### physicalDpiY(self)

#### pos(self)

#### previousInFocusChain(self)

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

#### restoreGeometry(self, Union[QByteArray, bytes, bytearray])

#### saveGeometry(self)

#### screen(self)

#### PlotNd.scroll(self, int, int)()
scroll(self, int, int, QRect)


#### setAcceptDrops(self, bool)

#### setAccessibleDescription(self, str)

#### setAccessibleName(self, str)

#### setAttribute(self, Qt.WidgetAttribute, on: bool = True)

#### setAutoFillBackground(self, bool)

#### setBackgroundRole(self, QPalette.ColorRole)

#### PlotNd.setBaseSize(self, int, int)()
setBaseSize(self, QSize)


#### PlotNd.setContentsMargins(self, int, int, int, int)()
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

#### setInputMethodHints(self, Union[Qt.InputMethodHints, Qt.InputMethodHint])

#### setLayout(self, QLayout)

#### setLayoutDirection(self, Qt.LayoutDirection)

#### setLocale(self, QLocale)

#### setMask(self, QBitmap)
setMask(self, QRegion)


#### setMaximumHeight(self, int)

#### PlotNd.setMaximumSize(self, int, int)()
setMaximumSize(self, QSize)


#### setMaximumWidth(self, int)

#### setMinimumHeight(self, int)

#### PlotNd.setMinimumSize(self, int, int)()
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

#### PlotNd.setSizeIncrement(self, int, int)()
setSizeIncrement(self, QSize)


#### setSizePolicy(self, QSizePolicy)
setSizePolicy(self, QSizePolicy.Policy, QSizePolicy.Policy)


#### setStatusTip(self, str)

#### setStyle(self, QStyle)

#### setStyleSheet(self, str)

#### PlotNd.setTabOrder(QWidget, QWidget)()

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

#### statusTip(self)

#### style(self)

#### styleSheet(self)

#### tabletEvent(self, QTabletEvent)

#### testAttribute(self, Qt.WidgetAttribute)

#### thread(self)

#### toolTip(self)

#### toolTipDuration(self)

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

#### updateMicroFocus(self)

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
