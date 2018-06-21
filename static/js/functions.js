$('document').ready(function(){
    var studentlist = {};
    
    var buttons = $('a');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function(e) {
            var active = $(".nav-item.active")[0];
            active.classList.remove("active");
            e.target.parentElement.classList.add('active');
        };
    }

    load_years()
});


function load_years(){
    $.ajax({
        url:"/f2kens/get_years/",
    }).done(function(data){
        studentlist = data;

        for (var i = 0; i<studentlist.length; i++){
            create_year_cb(studentlist[i]);
    }
    });
}

function create_year_cb(year){
    var list = $('#yearlist')[0];
    var field = "<div class='col-sm-6 col-md-4 col-lg-3'>\
                    <input id='"+ year['id'] +"' type='radio' name='year' value='"+ year['id'] +"'>\
                    <label for='"+ year['id'] +"'>"+ year['year_number']+", "+ year["division"] +"</label>\
                </div>"
    list.innerHTML+=field
}


