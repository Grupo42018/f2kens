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
