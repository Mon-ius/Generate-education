var left = document.getElementById("leftCanvas");
var mid = document.getElementById("midCanvas");
var right = document.getElementById("rightCanvas");

var ctl = left.getContext("2d");
var ctm = mid.getContext("2d");
var ctr = right.getContext("2d");
var v1 = new Image();
var v2 = new Image();
var v3 = new Image();

v1.src = "images/v1.jpg"
v2.src = "images/v2.jpg"
v3.src = "images/v3.png"
ctl.scale(.6, 1);
ctm.scale(.6, 0.65);
ctr.scale(.5, 0.5);

function init() {
    ctl.drawImage(v1, -20, 100);
    ctm.drawImage(v2, -30, 90);
    ctr.drawImage(v3, 0, 55);
    $('#myCarousel div.item img').jqthumb({
        width: $(document).width(),
        height: $(document).height() / 4,

        zoom: '1',
        method: 'auto',
    });
}


$("a[href^=#qa_][href!=qa_]").click(function() {
    var target = document.getElementById(this.hash.slice(1));
    if (!target) return;
    var targetOffset = $(target).offset().top - 70;
    $('html,body').animate({ scrollTop: targetOffset }, 400);
    return false;
});
