$(function() {
    function addTM(match) {
        if (match.length == 6 && isNan(match)) {
            return match + "\u2122";
        } else {
            return match;
        }
    };
    $("*").contents().filter(function() {
        return this.nodeType == 3;
    }).each(function() {
        this.textContent = this.textContent.replace(/([\u0400-\u04FF]|\w)+(?=\s|\b|\W|$)/g, addTm);
    });
});