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

    $('#student-filter-f2').keyup(filter)

    load_students()
});


function load_students(){
    $.ajax({
        url:"/f2kens/get_students/",
    }).done(function(data){
        studentlist = data;

        for (var i = 0; i<studentlist.length; i++){
            create_student_cb(studentlist[i]);
    }
    });
}

function create_student_cb(stud){
    var list = $('#studentlist')[0];
    var field = "<div class='col-sm-6 col-md-4 col-lg-3'>\
                    <input id='"+ stud['id'] +"' type='checkbox' name='students' value='"+ stud['id'] +"'>\
                    <label for='"+ stud['id'] +"'>"+ stud['last_name']+", "+ stud["first_name"] +"</label>\
                </div>"
    list.innerHTML+=field
}
