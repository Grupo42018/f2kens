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
    load_f2()

    $('#parentsModal').on('shown.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var student = button.data("stud")
        var modal = $(this)

        modal.find(".modal-title").text(button.data("name"))
        load_parent(student, modal);
    })

    $('#parentsModal').on('hidden.bs.modal', function (event) {
        var modal = $(this)
        modal.find("#parent-cards").empty()
        if(global.scanner){
            global.scanner.stop()
        }
    })
});


function load_f2(){
    $.ajax({
        url:"/f2kens/get_f2s/",
    }).done(function(data){
        for (i of data){
            add_f2_card(i);
        }
    });
}

function add_f2_card(f2){
    var list = $("#f2list")[0];

    var stateColor = "primary"
    switch (f2['state']){
        case "Aprobado":
            stateColor = "success";
            break;
        case "Rechazado":
            stateColor = "danger";
            break;
    }

    var card_template = "<div class=col-md-3 col-sm-10>\
                          <div class='card text-white bg-"+stateColor+"' style='margin-bottom:20px'>\
                            <div class='card-header'>"+f2["state"]+"</div>\
                            <div class='card-body'>\
                              <h5 class='card-title'>"+ f2["student"]["last_name"]+", "+ f2["student"]["first_name"] +"</h5>\
                              <p class='card-text'>\
                              "+ f2["motivo"] +"\
                              </p>\
                              <ul class='list-group list-group-flush'>\
                                <li class='list-group-item bg-dark'>"+ f2["time"] +"</li>\
                              </ul>\
                            </div>\
                          </div>\
                        </div>";

    list.innerHTML += card_template;

              
}

function load_years(){
    $.ajax({
        url:"/f2kens/get_years/",
    }).done(function(data){
        for (var i = 0; i<data.length; i++){
            add_year_cb(data[i], i);
        }
    });
}

function add_year_cb(year, first=false){
    var list = $('#yearlist')[0];

    var divInfo = {
        'class': "col-sm-6 col-md-4 col-lg-3"
    }
    var inputInfo = {
        id: "year-f2"+year['id'],
        value: year['id'],
        type: "radio",
        name: "year"
    }
    var labelInfo = {
        for: "year-f2"+year['id'],
        html: year["year_number"]+"-"+year['division']
    }

    if (!first){
        inputInfo["checked"]=""
    }

    var div = $('<div />', divInfo)[0]
    var input = $("<input />", inputInfo)[0]
    var label = $('<label />', labelInfo)[0]

    div.append(input)
    div.append(label)

    list.append(div)
}

function load_parent(student, modal) {
    $.ajax({
        url:"/f2kens/get_parents/"+student
    }).done((resp) => {
        resp.forEach((item) =>{
            modal.find("#parent-cards").append("\
            <div class='col-md-5 col-sm-10 mx-auto'>\
              <div class='card text-white bg-info'>\
                <div class='card-header'>"+item.last_name+", "+item.first_name+"</div>\
                <div class='card-body' style='display:flex'>\
                  <div id='qrReplace-"+item.id+"' class='qr bg-dark'>\
                  <center class='my-auto'>\
                    <button class='btn btn-default' onClick='startQr("+item.id+")'>Link Device</button>\
                  </center>\
                  </div>\
                </div>\
              </div>\
            </div>")
        })
    })
}

function startQr(item){
    if(global.scanner){
        global.scanner.stop()
        var last = $("#qrReplace-"+global.scanner.scanId)
        last.empty()
        last.append("\
            <center class='my-auto'>\
              <button class='btn btn-default' onClick='startQr("+global.scanner.scanId+")'>Link Device</button>\
            </center>");
    }

    var qr = $("#qrReplace-"+item)

    qr.empty()
    qr.append("<video id='qrVideo'></video>")

    global.scanner = new Instascan.Scanner({ video: document.getElementById("qrVideo") });
    global.scanner.scanId=item;

    global.scanner.addListener('scan', function (content) {
        $.ajax({
            url: "/f2kens/lnk_device/",
            method:'POST',
            data: {
                parent:item,
                device:content
            }
        }).done((resp) => {
            console.log(resp)
        })
        global.scanner.stop()
      });


    Instascan.Camera.getCameras().then(function (cameras) {
        if (cameras.length > 0) {
          global.scanner.start(cameras[0]);
        } else {
          console.error('No cameras found.');
        }
      }).catch(function (e) {
        console.error(e);
      });
}