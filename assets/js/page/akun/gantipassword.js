+ function ($) {
    'use strict';

    $("#tmplpasswordlama").on("change", function () {
        $(this).is(":checked") ? $("#passwordlama").attr("type", "text") : $("#passwordlama").attr("type", "password");
    });

    $("#tmplpasswordbaru").on("change", function () {
        $(this).is(":checked") ? $("#passwordbaru").attr("type", "text") : $("#passwordbaru").attr("type", "password");
    });

    $("#tmplulangpasswordbaru").on("change", function () {
        $(this).is(":checked") ? $("#ulangpasswordbaru").attr("type", "text") : $("#ulangpasswordbaru").attr("type", "password");
    });

    $('#formGantiPassword').validate({
        rules: {
            passwordlama: {
                required: true,
            },
            passwordbaru: {
                required: true,
                minlength: 8,
            },
            ulangpasswordbaru: {
                required: true,
                equalTo: '[name="passwordbaru"]'
            }
        },
        messages: {
            passwordlama: {
                required: "Password lama tidak boleh kosong.",
            },
            passwordbaru: {
                required: "Password baru tidak boleh kosong.",
                minlength: "Password baru min. 8 karakter.",
            },
            ulangpasswordbaru: {
                required: "Ulang password baru tidak boleh kosong.",
                equalTo: "Password baru dan ulangi password tidak sama."
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
        }, errorPlacement: function (error, element) {
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
        submitHandler: function () {
            $.ajax({
                type: 'POST',
                url: '/akun/gantipassword',
                data: JSON.stringify({
                    passwordlama: $('#passwordlama').val(),
                    passwordbaru: $('#passwordbaru').val(),
                }),
                async: true,
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (result) {
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

                    if (result.status){
                        $('#passwordlama').val('');
                        $('#passwordbaru').val('');
                        $('#ulangpasswordbaru').val('');
                    }
                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });
        }
    });

}(jQuery);