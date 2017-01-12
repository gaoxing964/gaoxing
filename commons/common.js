/**让IE8兼容这些函数的补丁**/
if(!('bind' in Function.prototype)) {
	Function.prototype.bind = function(owner) {
		var that = this;
		if(arguments.length <= 1) {
			return function() {
				return that.apply(owner, arguments);
			};
		} else {
			var args = Array.prototype.slice.call(arguments, 1);
			return function() {
				return that.apply(owner, arguments.length === 0 ? args : args.concat(Array.prototype.slice.call(arguments)));
			};
		}
	};
}

// Add ECMA262-5 string trim if not supported natively
//
if(!('trim' in String.prototype)) {
	String.prototype.trim = function() {
		return this.replace(/^\s+/, '').replace(/\s+$/, '');
	};
}

// Add ECMA262-5 Array methods if not supported natively
//
if(!('indexOf' in Array.prototype)) {
	Array.prototype.indexOf = function(find, i /*opt*/ ) {
		if(i === undefined) i = 0;
		if(i < 0) i += this.length;
		if(i < 0) i = 0;
		for(var n = this.length; i < n; i++)
			if(i in this && this[i] === find)
				return i;
		return -1;
	};
}
if(!('lastIndexOf' in Array.prototype)) {
	Array.prototype.lastIndexOf = function(find, i /*opt*/ ) {
		if(i === undefined) i = this.length - 1;
		if(i < 0) i += this.length;
		if(i > this.length - 1) i = this.length - 1;
		for(i++; i-- > 0;) /* i++ because from-argument is sadly inclusive */
			if(i in this && this[i] === find)
				return i;
		return -1;
	};
}
if(!('forEach' in Array.prototype)) {
	Array.prototype.forEach = function(action, that /*opt*/ ) {
		for(var i = 0, n = this.length; i < n; i++)
			if(i in this)
				action.call(that, this[i], i, this);
	};
}
if(!('map' in Array.prototype)) {
	Array.prototype.map = function(mapper, that /*opt*/ ) {
		var other = new Array(this.length);
		for(var i = 0, n = this.length; i < n; i++)
			if(i in this)
				other[i] = mapper.call(that, this[i], i, this);
		return other;
	};
}
if(!('filter' in Array.prototype)) {
	Array.prototype.filter = function(filter, that /*opt*/ ) {
		var other = [],
			v;
		for(var i = 0, n = this.length; i < n; i++)
			if(i in this && filter.call(that, v = this[i], i, this))
				other.push(v);
		return other;
	};
}
if(!('every' in Array.prototype)) {
	Array.prototype.every = function(tester, that /*opt*/ ) {
		for(var i = 0, n = this.length; i < n; i++)
			if(i in this && !tester.call(that, this[i], i, this))
				return false;
		return true;
	};
}
if(!('some' in Array.prototype)) {
	Array.prototype.some = function(tester, that /*opt*/ ) {
		for(var i = 0, n = this.length; i < n; i++)
			if(i in this && tester.call(that, this[i], i, this))
				return true;
		return false;
	};
}

/**装饰器模式要用到的代码**/
Function.prototype.after = function(afterfn) {
	var _self = this;
	return function() {
		var ret = _self.apply(this, arguments);
		afterfn.apply(this, arguments);
		return ret;
	}
}

var after = function(_self, afterfn) {
		return function() {
			var ret = _self.apply(this, arguments);
			afterfn.apply(this, arguments);
			return ret;
		}
	}
	/**复制javascript对象的方法 **/
function clone(obj) {
	var copy;

	// Handle the 3 simple types, and null or undefined
	if(null == obj || "object" != typeof obj) return obj;

	// Handle Date
	if(obj instanceof Date) {
		copy = new Date();
		copy.setTime(obj.getTime());
		return copy;
	}

	// Handle Array
	if(obj instanceof Array) {
		copy = [];
		for(var i = 0, len = obj.length; i < len; i++) {
			copy[i] = clone(obj[i]);
		}
		return copy;
	}

	// Handle Object
	if(obj instanceof Object) {
		copy = {};
		for(var attr in obj) {
			if(obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
		}
		return copy;
	}
}
/**从location上面取值的公共函数 **/
function getParam(key) {
	var paramsStr = window.location.href.split('?')[1];
	if(!paramsStr) {
		return '';
	}
	var params = paramsStr.split('&');
	var param = parms.filter(function(item) {
		var t = item.split('=');
		if(t[0] == key) {
			return true;
		}
	});
	if(param.lenth == 0) {
		return ''
	}
	var t = param[0].split('=');
	if(t[0] == key) {
		return t[1];
	}
}

//定时任务管理器
window.timeManager = (function() {

	var timeCount = 249;
	var funcaches = [];
	return {
		process: function() {
			// 执行定时任务  
			setInterval(function() {
				for(var i = 0; i < funcaches.length; i++) {
					funcaches[i]();
				}
			}, timeCount);
		},
		pushFun: function(fn) {
			/** 要执行哪些定时任务  push到里面就好了  **/
			funcaches.push(fn);
		}
	}

})();
//根据value分割成date
function getTheDate(dateStr , splitBar) {
	times = dateStr.split(splitBar);
	var year = parseInt(times[0]);
	var month = parseInt(times[1]);
	var day = parseInt(times[2]);
	var t = new Date();
	t.setYear(year);
	t.setMonth(month - 1);
	t.setDate(day);
	return t;
}