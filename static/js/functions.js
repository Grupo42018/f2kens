$('document').ready(function(){
    var buttons = $('a');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function(e) {
            var active = $(".nav-item.active")[0];
            active.classList.remove("active");
            e.target.parentElement.classList.add('active');
        };
    }
});