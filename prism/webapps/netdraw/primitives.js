function Primitive() {
	var me = {};
	
	me.paint = function(g) {};
	
	return me;
}

function LinePrimitive(p1, p2, color) {
	var me = Primitive();
	me.p1 = p1;
	me.p2 = p2;
	me.color = color;
	
	me.paint = function(g) {
		g.setColor(me.color);
		g.drawLine(me.p1.x, me.p1.y, me.p2.x, me.p2.y);
	};
	
	return me;
}

function RectanglePrimitive(p1, p2, color, filled) {
	var me = Primitive();
	me.p1 = p1;
	me.p2 = p2;
	me.color = color;
	me.filled = filled;
	
	me.paint = function(g) {
		var p1 = me.p1;
		var p2 = me.p2;
		
		var x1 = min(p1.x, p2.x);
		var x2 = max(p1.x, p2.x);
		var w = x2-x1+1;
		
		var y1 = min(p1.y, p2.y);
		var y2 = max(p1.y, p2.y);
		var h = y2-y1+1;
		
		g.setColor(me.color);
		if (me.filled) {
			g.fillRect(x1, y1, w, h);
		} else {
			g.drawRect(x1, y1, w, h);
		}
	};
	
	return me;
}

function OvalPrimitive(p1, p2, color, filled) {
	var me = Primitive();
	me.p1 = p1;
	me.p2 = p2;
	me.color = color;
	me.filled = filled;
	
	me.paint = function(g) {
		var p1 = me.p1;
		var p2 = me.p2;
		
		var x1 = min(p1.x, p2.x);
		var x2 = max(p1.x, p2.x);
		var w = x2-x1+1;
		
		var y1 = min(p1.y, p2.y);
		var y2 = max(p1.y, p2.y);
		var h = y2-y1+1;
		
		g.setColor(me.color);
		if (me.filled) {
			g.fillOval(x1, y1, w, h);
		} else {
			g.drawOval(x1, y1, w, h);
		}
	};
	
	return me;
}

function PolygonPrimitive(color, filled) {
	var me = Primitive();
	me.xs = [];
	me.ys = [];
	me.color = color;
	me.filled = filled;
	
	me.paint = function(g) {
		g.setColor(me.color);
		if (me.filled) {
			g.fillPolygon(me.xs, me.ys);
		} else {
			g.drawPolygon(me.xs, me.ys);
		}
	};
	
	me.addPoint = function(p) {
		me.xs.push(p.x);
		me.ys.push(p.y);
	};
	
	me.updateLastPoint = function(p) {
		me.xs.pop(); me.xs.push(p.x);
		me.ys.pop(); me.ys.push(p.y);
	};
	
	return me;
}

function min(n1, n2) {
	return n1<n2 ? n1 : n2;
}

function max(n1, n2) {
	return n1>n2 ? n1 : n2;
}