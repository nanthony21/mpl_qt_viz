# mpl_qt_viz.visualizers.DockablePlotWindow


### class mpl_qt_viz.visualizers.DockablePlotWindow(title='Dockable Plots')
Bases: `PyQt5.QtWidgets.QMainWindow`


#### class DockOption()
Bases: `int`


#### class DockOptions()
Bases: `sip.simplewrapper`

QMainWindow.DockOptions(Union[QMainWindow.DockOptions, QMainWindow.DockOption])
QMainWindow.DockOptions(QMainWindow.DockOptions)


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

#### actions(self)

#### activateWindow(self)

#### addAction(self, QAction)

#### addActions(self, Iterable[QAction])

#### addDockWidget(self, Qt.DockWidgetArea, QDockWidget)
addDockWidget(self, Qt.DockWidgetArea, QDockWidget, Qt.Orientation)


#### addToolBar(self, Qt.ToolBarArea, QToolBar)
addToolBar(self, QToolBar)
addToolBar(self, str) -> QToolBar


#### addToolBarBreak(self, area: Qt.ToolBarArea = Qt.TopToolBarArea)

#### adjustSize(self)

#### autoFillBackground(self)

#### backgroundRole(self)

#### baseSize(self)

#### blockSignals(self, bool)

#### centralWidget(self)

#### childAt(self, QPoint)
childAt(self, int, int) -> QWidget


#### children(self)

#### childrenRect(self)

#### childrenRegion(self)

#### clearFocus(self)

#### clearMask(self)

#### close(self)

#### colorCount(self)

#### contentsMargins(self)

#### contentsRect(self)

#### contextMenuEvent(self, QContextMenuEvent)

#### contextMenuPolicy(self)

#### corner(self, Qt.Corner)

#### createPopupMenu(self)

#### createWindowContainer(QWindow, parent: QWidget = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = 0)

#### cursor(self)

#### customContextMenuRequested()
customContextMenuRequested(self, QPoint) [signal]


#### deleteLater(self)

#### depth(self)

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


#### dockOptions(self)

#### dockWidgetArea(self, QDockWidget)

#### documentMode(self)

#### dumpObjectInfo(self)

#### dumpObjectTree(self)

#### dynamicPropertyNames(self)

#### effectiveWinId(self)

#### ensurePolished(self)

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


#### focusPolicy(self)

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

#### iconSize(self)

#### iconSizeChanged()
iconSizeChanged(self, QSize) [signal]


#### inherits(self, str)

#### inputMethodHints(self)

#### inputMethodQuery(self, Qt.InputMethodQuery)

#### DockablePlotWindow.insertAction(self, QAction, QAction)()

#### insertActions(self, QAction, Iterable[QAction])

#### DockablePlotWindow.insertToolBar(self, QToolBar, QToolBar)()

#### insertToolBarBreak(self, QToolBar)

#### installEventFilter(self, QObject)

#### isActiveWindow(self)

#### isAncestorOf(self, QWidget)

#### isAnimated(self)

#### isDockNestingEnabled(self)

#### isEnabled(self)

#### isEnabledTo(self, QWidget)

#### isFullScreen(self)

#### isHidden(self)

#### isLeftToRight(self)

#### isMaximized(self)

#### isMinimized(self)

#### isModal(self)

#### isRightToLeft(self)

#### isSeparator(self, QPoint)

#### isVisible(self)

#### isVisibleTo(self, QWidget)

#### isWidgetType(self)

#### isWindow(self)

#### isWindowModified(self)

#### isWindowType(self)

#### keyboardGrabber()

#### killTimer(self, int)

#### layout(self)

#### layoutDirection(self)

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

#### menuBar(self)

#### menuWidget(self)

#### metaObject(self)

#### minimumHeight(self)

#### minimumSize(self)

#### minimumSizeHint(self)

#### minimumWidth(self)

#### mouseGrabber()

#### move(self, QPoint)
move(self, int, int)


#### moveToThread(self, QThread)

#### nativeParentWidget(self)

#### nextInFocusChain(self)

#### normalGeometry(self)

#### objectName(self)

#### objectNameChanged()
objectNameChanged(self, str) [signal]


#### overrideWindowFlags(self, Union[Qt.WindowFlags, Qt.WindowType])

#### overrideWindowState(self, Union[Qt.WindowStates, Qt.WindowState])

#### paintEngine(self)

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

#### removeDockWidget(self, QDockWidget)

#### removeEventFilter(self, QObject)

#### removeToolBar(self, QToolBar)

#### removeToolBarBreak(self, QToolBar)

#### render(self, QPaintDevice, targetOffset: QPoint = QPoint(), sourceRegion: QRegion = QRegion(), flags: Union[QWidget.RenderFlags, QWidget.RenderFlag] = QWidget.RenderFlags(QWidget.RenderFlag.DrawWindowBackground | QWidget.RenderFlag.DrawChildren))
render(self, QPainter, targetOffset: QPoint = QPoint(), sourceRegion: QRegion = QRegion(), flags: Union[QWidget.RenderFlags, QWidget.RenderFlag] = QWidget.RenderFlags(QWidget.RenderFlag.DrawWindowBackground|QWidget.RenderFlag.DrawChildren))


#### repaint(self)
repaint(self, int, int, int, int)
repaint(self, QRect)
repaint(self, QRegion)


#### resize(self, QSize)
resize(self, int, int)


#### resizeDocks(self, Iterable[QDockWidget], Iterable[int], Qt.Orientation)

#### restoreDockWidget(self, QDockWidget)

#### restoreGeometry(self, Union[QByteArray, bytes, bytearray])

#### restoreState(self, Union[QByteArray, bytes, bytearray], version: int = 0)

#### saveGeometry(self)

#### saveState(self, version: int = 0)

#### screen(self)

#### DockablePlotWindow.scroll(self, int, int)()
scroll(self, int, int, QRect)


#### setAcceptDrops(self, bool)

#### setAccessibleDescription(self, str)

#### setAccessibleName(self, str)

#### setAnimated(self, bool)

#### setAttribute(self, Qt.WidgetAttribute, on: bool = True)

#### setAutoFillBackground(self, bool)

#### setBackgroundRole(self, QPalette.ColorRole)

#### DockablePlotWindow.setBaseSize(self, int, int)()
setBaseSize(self, QSize)


#### setCentralWidget(self, QWidget)

#### DockablePlotWindow.setContentsMargins(self, int, int, int, int)()
setContentsMargins(self, QMargins)


#### setContextMenuPolicy(self, Qt.ContextMenuPolicy)

#### setCorner(self, Qt.Corner, Qt.DockWidgetArea)

#### setCursor(self, Union[QCursor, Qt.CursorShape])

#### setDisabled(self, bool)

#### setDockNestingEnabled(self, bool)

#### setDockOptions(self, Union[QMainWindow.DockOptions, QMainWindow.DockOption])

#### setDocumentMode(self, bool)

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

#### setIconSize(self, QSize)

#### setInputMethodHints(self, Union[Qt.InputMethodHints, Qt.InputMethodHint])

#### setLayout(self, QLayout)

#### setLayoutDirection(self, Qt.LayoutDirection)

#### setLocale(self, QLocale)

#### setMask(self, QBitmap)
setMask(self, QRegion)


#### setMaximumHeight(self, int)

#### DockablePlotWindow.setMaximumSize(self, int, int)()
setMaximumSize(self, QSize)


#### setMaximumWidth(self, int)

#### setMenuBar(self, QMenuBar)

#### setMenuWidget(self, QWidget)

#### setMinimumHeight(self, int)

#### DockablePlotWindow.setMinimumSize(self, int, int)()
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

#### DockablePlotWindow.setSizeIncrement(self, int, int)()
setSizeIncrement(self, QSize)


#### setSizePolicy(self, QSizePolicy)
setSizePolicy(self, QSizePolicy.Policy, QSizePolicy.Policy)


#### setStatusBar(self, QStatusBar)

#### setStatusTip(self, str)

#### setStyle(self, QStyle)

#### setStyleSheet(self, str)

#### DockablePlotWindow.setTabOrder(QWidget, QWidget)()

#### setTabPosition(self, Union[Qt.DockWidgetAreas, Qt.DockWidgetArea], QTabWidget.TabPosition)

#### setTabShape(self, QTabWidget.TabShape)

#### setTabletTracking(self, bool)

#### setToolButtonStyle(self, Qt.ToolButtonStyle)

#### setToolTip(self, str)

#### setToolTipDuration(self, int)

#### setUnifiedTitleAndToolBarOnMac(self, bool)

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

#### show(self)

#### showFullScreen(self)

#### showMaximized(self)

#### showMinimized(self)

#### showNormal(self)

#### signalsBlocked(self)

#### size(self)

#### sizeHint(self)

#### sizeIncrement(self)

#### sizePolicy(self)

#### splitDockWidget(self, QDockWidget, QDockWidget, Qt.Orientation)

#### stackUnder(self, QWidget)

#### startTimer(self, int, timerType: Qt.TimerType = Qt.CoarseTimer)

#### statusBar(self)

#### statusTip(self)

#### style(self)

#### styleSheet(self)

#### tabPosition(self, Qt.DockWidgetArea)

#### tabShape(self)

#### tabifiedDockWidgetActivated()
tabifiedDockWidgetActivated(self, QDockWidget) [signal]


#### tabifiedDockWidgets(self, QDockWidget)

#### DockablePlotWindow.tabifyDockWidget(self, QDockWidget, QDockWidget)()

#### takeCentralWidget(self)

#### testAttribute(self, Qt.WidgetAttribute)

#### thread(self)

#### toolBarArea(self, QToolBar)

#### toolBarBreak(self, QToolBar)

#### toolButtonStyle(self)

#### toolButtonStyleChanged()
toolButtonStyleChanged(self, Qt.ToolButtonStyle) [signal]


#### toolTip(self)

#### toolTipDuration(self)

#### tr(self, str, disambiguation: str = None, n: int = - 1)

#### underMouse(self)

#### ungrabGesture(self, Qt.GestureType)

#### unifiedTitleAndToolBarOnMac(self)

#### unsetCursor(self)

#### unsetLayoutDirection(self)

#### unsetLocale(self)

#### update(self)
update(self, QRect)
update(self, QRegion)
update(self, int, int, int, int)


#### updateGeometry(self)

#### updatesEnabled(self)

#### visibleRegion(self)

#### whatsThis(self)

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
