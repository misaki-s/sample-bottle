/*
* ハイライト
*/
var HighlightWord = (function () {
  function HighlightWord(words, colorCode) {
    this.words = words;
    this.colorCode = colorCode;
  }
  return HighlightWord;
}());

var TextHighlighter = (function () {

  function TextHighlighter(prohibition, highlightWords) {
    this.prohibition = prohibition;
    this.leftProhibition = " " + this.prohibition;
    this.rightProhibition = this.prohibition + " ";
    this.highlightWords = highlightWords;
  }

  TextHighlighter.prototype.text2HighlightHTML = function (text) {
    var _this = this;
    if (-1 !== text.indexOf(this.prohibition)) {
      return this.sanitize(text);
    }
    var replaced = text;
    var replacedNum = 0;
    var replaces = {};
    for (var i = 0; i < this.highlightWords.length; i++) {
      var highlightWord = this.highlightWords[i];
      for (var j = 0; j < highlightWord.words.length; j++) {
        var word = highlightWord.words[j];
        var reg = new RegExp("(" + word.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&') + ")", 'g');
        var changed = replaced.replace(reg, function (match, group1, offset, s) {
          if (0 < offset && s[offset - 1] === _this.prohibition) {
            return match;
          }
          return _this.leftProhibition + String(replacedNum) + _this.rightProhibition;
        });
        if (changed !== replaced) {
          replaced = changed;
          replaces[replacedNum] = { word: word, color_code: highlightWord.colorCode };
          replacedNum++;
        }
      }
    }
    for (var i = 0; i < replacedNum; i++) {
      var reg = new RegExp(this.leftProhibition + String(i) + this.rightProhibition, 'g');
      var word = this.sanitize(replaces[i]["word"]);
      replaced = replaced.replace(reg, "<span style=\"font-weight: bold; background-color: #" + replaces[i]["color_code"] + "\">" + word + "</span>");
    }
    return replaced;
  };

  TextHighlighter.prototype.sanitize = function (s) {
    return s.replace(/[&'`"<>]/g, function (match) {
      return {
        '&': '&amp;',
        "'": '&#x27;',
        '`': '&#x60;',
        '"': '&quot;',
        '<': '&lt;',
        '>': '&gt;',
      }[match];
    });
  };
  return TextHighlighter;
}());
