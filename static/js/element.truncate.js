Element.implement({
  /**
	truncates elements text based on pixel length. handles font styling, size padding and margin issues.
	  len (int) pixel value for the max width of the the element text content
	  end (bool) defaults false. True = cuts string at end, False = cuts string in middle
	  str (string) truncation string default : '...'
	**/
  truncate: function (end, str) {
    str = str || "...";
    var style = this.style;
    var originalStyles = {
      overflow: style.overflow,
      "white-space": style.whiteSpace,
      padding: style.padding,
    };
    this.setStyles({ overflow: "hidden", "white-space": "nowrap", padding: 0 });
    var width = this.clientWidth;
    var txt = this.get("text");
    if (end) {
      var rside = txt.length;
      while (this.scrollWidth > width) {
        rside--;
        this.set("text", txt.slice(0, rside) + str);
      }
    } else {
      var mid = (lside = Math.floor(txt.length / 2));
      var rside = lside + 1;
      while (this.scrollWidth > width) {
        mid - lside < rside - mid ? lside-- : rside++;
        this.set("text", txt.slice(0, lside) + str + txt.slice(rside));
      }
    }
    return this.setStyles(originalStyles);
  },
});
