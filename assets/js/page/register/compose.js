+ function ($) {
    'use strict';

    // NOTE: Cari Berkas
    $('#formCariBerkas').validate({
        rules: {
            nomor: {
                required: true,
                digits: true
            },
            tahun: {
                required: true,
                digits: true
            }
        },
        messages: {
            nomor: {
                required: 'Nomor berkas wajib diisi.',
            },
            tahun: {
                required: 'Tahun berkas wajib diisi.',
            }
        },
        errorElement: "small",
        highlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').addClass('has-error');
        },
        unhighlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').removeClass('has-error');
        },errorPlacement: function (error, element) {
            if (element.parent('.input-group').length) {
                error.insertAfter(element.parent());
            }
            else if (element.prop('type') === 'radio' && element.parent('.radio-inline').length) {
                error.insertAfter(element.parent().parent());
            }
            else if (element.prop('type') === 'checkbox' || element.prop('type') === 'radio') {
                error.appendTo(element.parent().parent());
            }
            else {
                error.insertAfter(element);
            }
        }, 
        invalidHandler: function(){
        },
        submitHandler: function () {
            run_wait('.content');
            $.ajax({
                type: 'POST',
                url: '/register/compose',
                data: JSON.stringify({
                    nomor: $('#nomor').val(),
                    tahun: $('#tahun').val(),
                }),
                async: false,
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (result) {
                    if (result.status){
                        $('#berkasView').load('/register/berkas/detail/berkasid=' + result.data[0].berkasid, function () {
                            $('.content').waitMe("hide");
                        });
                    }else{
                        
                        $.notify({
                            title: result.title,
                            message: result.msg,
                        }, {
                            type: result.type,
                            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                                '<span data-notify="title">{1}</span>' +
                                '<span data-notify="message">{2}</span>' +
                                '</div>',
                            animate: {
                                enter: 'animated fadeInRight',
                                exit: 'animated fadeOutRight'
                            }
                        });

                        $('#berkasView').load('/node/error/400', function () {
                            $('.content').waitMe("hide");
                        });
                    }

                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                }) 

            });
        }
    });

}(jQuery);

/* Initial Loading */
function run_wait(element) {
    $(element).waitMe({
        effect: 'bounce',
        text: '<b>Sedang proses...</b> <br> harap tunggu',
        bg: 'rgba(255,255,255,0.6)',
        color: '#000'
    });
}