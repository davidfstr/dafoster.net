function Tool(name) {
	var me = {};
	me.name = name;
	me.cursor = "crosshair";
	// initialized by 'Toolbar.init()'
	me.ui = null;
	
	me.prim = null;
	me.toolActivated = function() {
		me.prim = null;
	};
	me.toolDeactivated = function() {
		if (me.prim != null) {
			Canvas.removeScratchPrimitive(me.prim);
			me.prim = null;
		}
	};
	
	me.toolDeactivated = function() {};
	me.mousePressed = function(mouseEvt) {};
	me.mouseReleased = function(mouseEvt) {};
	me.mouseClicked = function(mouseEvt) {};
	me.mouseDragged = function(mouseEvt) {};
	me.mouseMoved = function(mouseEvt) {};
	
	return me;
}

var LineTool = function() {			// singleton
	var me = Tool("line");			// superclass
	
	me.mousePressed = function(mouseEvt) {
		// Define startpoint
		me.prim = LinePrimitive(mouseEvt.p, mouseEvt.p, OptionBar.getCurrentColor());
		Canvas.addScratchPrimitive(me.prim);
	};
	
	me.mouseDragged = function(mouseEvt) {
		// Update endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
	};
	
	me.mouseReleased = function(mouseEvt) {
		// Finalize endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
		
		// Make the primitive final
		Canvas.makeScratchPrimitiveFinal(me.prim);
		
		// Cleanup
		me.prim = null;
	};
	
	return me;
}();

var RectangleTool = function() {	// singleton
	var me = Tool("rectangle");		// superclass
	
	me.mousePressed = function(mouseEvt) {
		// Define startpoint
		me.prim = RectanglePrimitive(mouseEvt.p, mouseEvt.p, OptionBar.getCurrentColor(), OptionBar.getCurrentFillMode());
		Canvas.addScratchPrimitive(me.prim);
	};
	
	me.mouseDragged = function(mouseEvt) {
		// Update endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
	};
	
	me.mouseReleased = function(mouseEvt) {
		// Finalize endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
		
		// Make the primitive final
		Canvas.makeScratchPrimitiveFinal(me.prim);
		
		// Cleanup
		me.prim = null;
	};
	
	return me;
}();

var OvalTool = function() {			// singleton
	var me = Tool("oval");			// superclass
	
	me.mousePressed = function(mouseEvt) {
		// Define startpoint
		me.prim = OvalPrimitive(mouseEvt.p, mouseEvt.p, OptionBar.getCurrentColor(), OptionBar.getCurrentFillMode());
		Canvas.addScratchPrimitive(me.prim);
	};
	
	me.mouseDragged = function(mouseEvt) {
		// Update endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
	};
	
	me.mouseReleased = function(mouseEvt) {
		// Finalize endpoint
		me.prim.p2 = mouseEvt.p;
		Canvas.updatePrimitive(me.prim);
		
		// Make the primitive final
		Canvas.makeScratchPrimitiveFinal(me.prim);
		
		// Cleanup
		me.prim = null;
	};
	
	return me;
}();

var PolygonTool = function() {		// singleton
	var me = Tool("polygon");		// superclass
	
	me.mouseClicked = function(mouseEvt) {
		if (me.prim == null) {
			// If this is a new polygon
			me.prim = new PolygonPrimitive(OptionBar.getCurrentColor(), OptionBar.getCurrentFillMode());
			me.prim.addPoint(mouseEvt.p);
			me.prim.addPoint(mouseEvt.p);
			Canvas.addScratchPrimitive(me.prim);
		} else if (mouseEvt.clickCount == 1) {
			// If this is just another point
			me.prim.addPoint(mouseEvt.p);
			Canvas.updatePrimitive(me.prim);
		} else if (mouseEvt.clickCount == 2) {
			// If this is just the end of the polygon
			me.prim.addPoint(mouseEvt.p);
			Canvas.updatePrimitive(me.prim);
			Canvas.makeScratchPrimitiveFinal(me.prim);
			me.prim = null;
		}
	};
	
	me.mouseMoved = function(mouseEvt) {
		// Update endpoint
		if (me.prim != null) {
			me.prim.updateLastPoint(mouseEvt.p);
			Canvas.updatePrimitive(me.prim);
		}
	};
	
	return me;
}();

var ArcTool = function() {			// singleton
	var me = Tool("arc");			// superclass
	return me;
}();

var TextTool = function() {			// singleton
	var me = Tool("text");			// superclass
	me.cursor = "text";
	
	return me;
}();

var PictureTool = function() {		// singleton
	var me = Tool("picture");		// superclass
	return me;
}();