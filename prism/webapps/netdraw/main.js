var SELECTED_TOOL_COLOR = "#f6bfbe";
var UNSELECTED_TOOL_COLOR = "#e1e1fc";
var DOUBLE_CLICK_DURATION = 300;

var NetDraw = {};

// Called upon page load.
function init() {
	/*
	// Make the canvas touch-sensitive
	canvasElem = document.getElementById("canvas");
	YAHOO.util.Event.addListener(canvasElem, "click", function(e) {
		canvas.mousePressed();
	});
	*/
	
	Toolbar.init();
	Canvas.init();
	
	// Initialize dialogs (and other containers) when the DOM finishes loading
	YAHOO.util.Event.onDOMReady(NetDraw.colorpicker.init, NetDraw.colorpicker, true);
}

var Toolbar = {
	tools: [
		LineTool,
		RectangleTool,
		OvalTool,
		PolygonTool/*,
		ArcTool,
		TextTool,
		PictureTool
		*/
	],
	
	curTool: null,
	
	init: function() {
		/* Add toolbar buttons, and set each tool's 'ui' field */
		tools = document.getElementById("tools");
		for (var i=0; i<Toolbar.tools.length; i++) {
			var curTool = Toolbar.tools[i];
			
			var img = document.createElement("img");
			img.id = curTool.name;
			img.src = "images/tools/" + img.id + ".png";
			img.width = "22";
			img.height = "22";
			img.style.marginLeft = "4px";
			// XXX: may introduce circular reference into UI
			img.tool = curTool;
			
			//img.onclick = "Toolbar.select(this.id);"
			img.onclick = function(e) {
				// NOTE: The contents/presence of 'e' are browser specific!
				//       Use YUI's 'YAHOO.util.Event.addListener' method to make this
				//       work in all browsers.
				Toolbar.select(e.target.tool);
				
				/*
				// Bring up the Firebug debugger
				debugger;
				*/
			};
			
			var li = document.createElement("li");
			li.appendChild(img);
			
			tools.appendChild(li);
			
			// Set the 'ui' field of the tool
			// XXX: may introduce circular reference into UI
			curTool.ui = img;
		}
		
		// Select the first tool
		Toolbar.select(Toolbar.tools[0]);
	},
	
	select: function(newTool) {
		var oldTool = Toolbar.curTool;
		
		// Update selected tool in the toolbar
		if (oldTool != null) {
			oldTool.toolDeactivated();
			oldTool.ui.style.backgroundColor = UNSELECTED_TOOL_COLOR;
		}
		newTool.ui.style.backgroundColor = SELECTED_TOOL_COLOR;
		newTool.toolActivated();
		
		Toolbar.curTool = newTool;
		
		// Update the cursor to be displayed by the canvas
		Canvas.getElement().style.cursor = newTool.cursor;
	}
};

var OptionBar = {
	getCurrentFillMode: function() {
		return document.getElementById("filled").checked;
	},
	
	curColor_hex: "#000000",
	
	getCurrentColor: function() {
		return OptionBar.curColor_hex;
		
		// TODO: return the background color in the correct format
		//return "#000000";
		//return document.getElementById("colorwell").style.backgroundColor;
	},
	
	setCurrentColor: function(newColor) {
		OptionBar.curColor_hex = newColor;
		document.getElementById("colorwell").style.backgroundColor = newColor;
	}
};

var Canvas = {
	dragInProgress: false,
	g: null,
	
	// ### INIT ###
	
	init: function() {
		Canvas.g = new jsGraphics(Canvas.getElement());
		Canvas.g.setColor("#000000");
	},
	
	// ### OPERATIONS ###
	
	print: function() {
		// Rerender the canvas in slow printable mode
		Canvas.g.setPrintable(true);
		Canvas.repaint();
		
		// Open the print dialog
		window.print();
		
		// Reconfigure the canvas back to faster non-printable mode
		Canvas.g.setPrintable(false);
	},
	
	// ### EVENTS ###
	
	mousePressed: function(evt) {
		Canvas.dragInProgress = true;
		
		Toolbar.curTool.mousePressed(createMouseEvent(evt));
	},
	
	lastMouseReleaseTimestamp: 0,
	
	mouseReleased: function(evt) {
		if (Canvas.dragInProgress) {	// needed in case 'mouseExited' sets this to false
			Canvas.dragInProgress = false;
			
			var mouseEvt = createMouseEvent(evt);
			Toolbar.curTool.mouseReleased(mouseEvt);
			
			// Determine whether a double-click occurred
			var curMouseReleaseTimestamp = evt.timeStamp;
			var timeSinceLastMouseRelease = curMouseReleaseTimestamp - Canvas.lastMouseReleaseTimestamp;
			if (timeSinceLastMouseRelease < DOUBLE_CLICK_DURATION) {
				// XXX: Only detects double-clicks - i.e. no triple or more clicks
				mouseEvt.clickCount = 2;
				//console.log("Double-click");
			}
			//console.log(timeSinceLastMouseRelease);
			
			Toolbar.curTool.mouseClicked(mouseEvt);
			
			Canvas.lastMouseReleaseTimestamp = curMouseReleaseTimestamp;
		}
	},
	
	mouseMoved: function(evt) {
		if (Canvas.dragInProgress) {
			Canvas.mouseDragged(evt);
		} else {
			// PERF: Avoid creating a mouse-event if the tool doesn't actually handle this
			Toolbar.curTool.mouseMoved(createMouseEvent(evt));
		}
	},
	mouseDragged: function(evt) {
		Toolbar.curTool.mouseDragged(createMouseEvent(evt));
	},
	
	mouseExited: function(evt) {
		// TODO: Doesn't work because the vector graphics library's pixels
		//       cause this to be called immediately upon drawing a primitive
		//       under the cursor.
		/*
		if (Canvas.dragInProgress) {
			// Simulate a mouse-released
			Canvas.mouseReleased(evt);
		}
		*/
	},
	
	// ### PRIMITIVES ###
	
	scratchLayer: [],
	
	// Adds a primitive to the scratch layer.
	addScratchPrimitive: function(prim) {
		Canvas.scratchLayer.push(prim);
		Canvas.updatePrimitive(prim);
	},
	
	// Removes a primitive from the scratch layer.
	removeScratchPrimitive: function(prim) {
		var sl = Canvas.scratchLayer;
		sl.splice(sl.indexOf(prim), 1);	// sl.remove(prim);
		Canvas.updatePrimitive(prim);
	},
	
	// Notified when the appearance of a primitive on the canvas has changed.
	updatePrimitive: function(prim) {
		// PERF: Consider optimizing to only repaint
		//       the region of the canvas that is affected
		Canvas.repaint();
	},
	
	// Moves the specified primitive from the scratch layer to the pending layer.
	// Eventually the primitive will migrate from there to the confirmed layer.
	makeScratchPrimitiveFinal: function(prim) {
		// TODO: implement this once we get the canvas server up and running
		
		/*
		// Remove the primitive from the scratch layer
		var sl = Canvas.scratchLayer;
		sl.splice(sl.indexOf(prim), 1);	// sl.remove(prim);
		
		// TODO: add 'prim' to 'pendingLayer'
		// TODO: asynchronously send 'prim' to the canvas server
		*/
	},
	
	// ### PAINTING ###
	
	repaint: function() {
		var g = Canvas.g;
		
		g.clear();
		var layer = Canvas.scratchLayer;
		for (var i=0; i<layer.length; i++) {
			layer[i].paint(g);
		}
		g.paint();
	},
	
	// ### UTILITY ###
	
	getElement: function() {
		return document.getElementById("canvas");
	}
};

NetDraw.colorpicker = {
	//In our initialization function, we'll create the dialog;
	//in its render event, we'll create our Color Picker instance.
	init: function() {

		// Instantiate the Dialog
		this.dialog = new YAHOO.widget.Dialog("yui-picker-panel", { 
			width : "500px",
			close: true,
			//fixedcenter : true,
			// XXX: use more intelligent positioning
			xy: [416, 4],
			visible : false, 
			constraintoviewport : true,
			buttons : [ { text:"Choose", handler:this.handleSubmit, isDefault:true },
						{ text:"Cancel", handler:this.handleCancel } ]
		});

		// Once the Dialog renders, we want to create our Color Picker instance.
		this.dialog.renderEvent.subscribe(function() {
			//make sure that we haven't already created our Color Picker
			if (this.picker) return;
			
			this.picker = new YAHOO.widget.ColorPicker("yui-picker", {
				container: this.dialog,
				images: {
					PICKER_THUMB: "extern/colorpicker/picker_thumb.png",
					HUE_THUMB: "extern/colorpicker/hue_thumb.png"
				},
				//Here are some other configurations we could use for our Picker:
				//showcontrols: false,  // default is true, false hides the entire set of controls
				showhexcontrols: true, // default is false
				showhsvcontrols: true  // default is false
			});

			// Listen for changes to the picker's current RGB value
			this.picker.on("rgbChange", function(o) {
				//alert("DEBUG: rgbChange");
			});
		});	
		
		// If we wanted to do form validation on our Dialog, this
		// is where we'd do it.  Remember to return true if validation
		// passes; otherwise, your Dialog's submit method won't submit.
		this.dialog.validate = function() {
			return true;
		};
		
		// We're all set up with our Dialog's configurations;
		// now, render the Dialog
		this.dialog.render();
	},
	
	handleSubmit: function() {
		var me = NetDraw.colorpicker;
		
		var rgb = "#" +
			document.getElementById("yui-picker-rhex").textContent +
			document.getElementById("yui-picker-ghex").textContent +
			document.getElementById("yui-picker-bhex").textContent;
		OptionBar.setCurrentColor(rgb);
		
		me.dialog.hide();
	},

	handleCancel: function() {
		this.cancel();
	},
	
	toggleVisibility: function() {
		if (this.dialog.cfg.getProperty("visible")) {
			this.dialog.hide();
		} else {
			this.dialog.show();
		}
	}
};

// ### UTILITY ###

function createMouseEvent(evt) {
	me = {
		p: {
			// XXX: Returns absolute coordinates instead of relative coordinates
			//      because 'jsGraphics' doesn't seem to deal with relative coordinates correctly
			x: evt.clientX /*- evt.target.offsetLeft*/,
			y: evt.clientY /*- evt.target.offsetTop*/,
			
			toString: function() {
				return me.x + "," + me.y;
			}
		},
		// XXX: sometimes overridden by 'createMouseEvent'
		clickCount: 1
	};
	return me;
}