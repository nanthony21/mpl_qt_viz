# mpl_qt_viz.roiSelection

Useful classes for interacting with Matplotlib plots. Mostly for the purpose of drawing ROIs.

## ROI Creators

| `EllipseCreator`(axMan, image[, onselect])

 | Allows the user to select an elliptical region.

 |
| `LassoCreator`(axMan, image[, onselect])

   | Allows the user to select a region with freehand drawing.

 |
| `RegionalPaintCreator`(axMan, im[, onselect])

 | A widget allowing the user to select a rectangular region with a bright region in it such as a fluorescent nucleus.

 |
| `PointCreator`(axMan, image[, onselect, …])

   | 

                                                                                                                    |
| `FullImPaintCreator`(axMan, im[, onselect])

   | Uses adaptive thresholding in an attempt to highlight all bright selectable regions in a fluorescence image.

        |
| `WaterShedPaintCreator`(axMan, im[, onselect])

 | Uses Watershed technique in an attempt to highlight all bright selectable regions in a fluorescence image.

          |
## Utility

| `AdjustableSelector`(axManager, image, …[, …])

 | This class manages an roi selector.

                                                                                 |
| `PolygonModifier`(axMan[, onselect, onCancelled])

 | A polygon editor. [https://matplotlib.org/gallery/event_handling/poly_editor.html](https://matplotlib.org/gallery/event_handling/poly_editor.html) Key-bindings:     ‘d’ delete the vertex under point     ‘i’ insert a vertex at point. You must be within epsilon of the         line connecting two existing vertices.

 |
| `AxManager`(ax)

                                   | An object to manage multiple selector tools on a single axes.

                                                                                                                                                                                           |
