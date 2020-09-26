+ function ($) {
    'use strict';

    /* Initial Cari Berkas */
    $('#formCariBerkas').validate({
        rules: {
            nomorBerkas: {
                required: true,
            },
            tahunBerkas: {
                required: true,
            }
        },
        messages: {
            nomorBerkas: {
                required: 'Nomor berkas tidak boleh kosong.',
            },
            tahunBerkas: {
                required: 'Tahun berkas tidak boleh kosong.',
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
        },
        submitHandler: function () {
            $.ajax({
                type: 'POST',
                url: '/register/compose',
                data: JSON.stringify({
                    nomor: $('#nomorBerkas').val(),
                    tahun: $('#tahunBerkas').val(),
                }),
                async: false,
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (data) {
                    console.log(data);
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
        text: 'Harap tunggu...',
        bg: 'rgba(255,255,255,0.6)',
        color: '#000'
    });
}