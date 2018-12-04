$('document').ready(function(){

    var loc = window.location.toString().split("#")

    if (loc.length == 2){
        $('.tab-pane').toArray().forEach((item) => {
            if (item.id == loc[1]){
                $(".tab-pane.active")[0].classList.remove('active')
                item.classList.add('active')
            }
        })
    }

    $("#f2Form").find("#subF2").on('click', (e) => {
        var form = $('#f2Form')
        $.ajax({
            url: '/f2kens/create_f2/',
            method: 'POST',
            data: getFormData(form)
        }).then((data) => {
            location.reload()
        }).catch((e) => {
            for (var key in e.responseJSON){
                $('#'+key)[0].classList.add('is-invalid')
                $("#error"+key)[0].innerHTML = e.responseJSON[key][0]
            }
        })
    })

    $('#qrScan').on('shown.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var parent = button.data("parent")
        var modal = $(this)

        modal.find(".modal-title").text(button.data("parentname"))
        startQr(parent);
    })

    $('#qrScan').on('hidden.bs.modal', function (event) {
        var modal = $(this)
        modal.find("#qrTitle").empty()
        modal.find("#parent-cards").empty()
        if(global.scanner){
            global.scanner.stop()
        }
    })
});

function getFormData(form) {
    var rawJson = form.serializeArray();
    var model = {};

    $.map(rawJson, function (n, i) {
        model[n['name']] = n['value'];
    });

    return model;
}

function startQr(item){
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
            if (!location.toString().endsWith('#students')){
                location += "#students"
            }
            location.reload()
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
