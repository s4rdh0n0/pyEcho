+ function ($) {
    'use strict';


    $('#formFilter').validate({
        rules: {},
        messages: {},
        errorElement: "small",
        highlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').addClass('has-error');
        },
        unhighlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').removeClass('has-error');
        },
        submitHandler: function (form) {
            $('#tablePegawai').DataTable().ajax.reload();
        }
    });


    $('#formAddPegawai').validate({
        rules: {
            username: {
                required: true,
            }
        },
        messages: {
            username: {
                required: 'Username tidak boleh kosong.',
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
        submitHandler: function (form) {
            $.ajax({
                type: 'PUT',
                url: '/administrator/daftarpegawai',
                data: JSON.stringify({ username: $('#username').val() }),
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (result) {
                    if (result.status) {

                        // NOTE : 
                        $(".kkplog").show();
                        $(".kkplog_finder").hide();
                        $(".kkplog_alert").hide();

                        // NOTE :
                        $("#pegawaiid_kkplog").val(result.data.result.pegawaiid);
                        $("#username_kkplog").val($("#username").val());     
                        $("#name_kkplog").val(result.data.result.nama);
                        $("#phone_kkplog").val(result.data.result.phone);

                    } else {
                        $(".kkplog_alert").show();
                        $(".kkplog_alert").html('<h4><i class="icon fa fa-warning"></i>Warning!</h4>' + result.msg)
                    }
                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });
        }
    });

    // NOTE: modal-add hide
    $('#modal-add').on('hide.bs.modal', function () {
        $(".kkplog_alert").hide();
        $(".kkplog").hide();
        $(".kkplog_finder").show();
        $("#username").val("");
    });

    // NOTE: modal-add click button(batalregisterpegawai)
    $('#batalregisterpegawai').on('click', function () {
        $(".kkplog_alert").hide();
        $(".kkplog").hide();
        $(".kkplog_finder").show();
        $("#username").val("");
        $("#username").focus();
    });

    $('#registerpegawai').on('click', function(){
        $.ajax({
            type: 'POST',
            url: '/administrator/daftarpegawai/detail',
            data: JSON.stringify({ username: $('#username_kkplog').val() }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (result) {
                $('#modal-add').modal('hide')
                $.notify({
                    title: '<strong><i class="fa fa-info-circle" aria-hidden="true"></i> Info</strong> <br>',
                    message: result.msg,
                }, {
                    type: result.type,
                    animate: {
                        enter: 'animated fadeInRight',
                        exit: 'animated fadeOutRight'
                    }
                });

                if (result.status) {
                    $('#tablePegawai').DataTable().ajax.reload();
                }

            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            })
        })
    });

    // Info Pegawai
    $('#tablePegawai tbody').on('click', '#info', function () {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tablePegawai.row(selected_row).data()[0] != "") {
            run_wait('#detail');
            $('#detail').load('/administrator/daftarpegawai/detail/userid=' + tablePegawai.row(selected_row).data()['_id']);
            $('.nav-tabs a[href="#detail"]').tab('show');
        }
    });

}(jQuery);

function run_wait(element) {
    $(element).waitMe({
        effect: 'bounce',
        text: 'Harap tunggu...',
        bg: 'rgba(255,255,255,0.6)',
        color: '#000'
    });
}

/* Initial Table Pegawai */
var tablePegawai = $('#tablePegawai').DataTable({
    'processing': true,
    'serverSide': true,
    'ajax': function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/administrator/daftarpegawai',
            data: JSON.stringify({
                page: $('#tablePegawai').DataTable().page.info()['page'],
                start: $('#tablePegawai').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tablePegawai').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tablePegawai').dataTable().fnSettings().iDraw,
                pegawaiid: $('#pegawaiid').val(),
            }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                // NOTE: print data
                console.log(data)
                
                // NOTE: callback response ajax
                if (data.status){
                    callback(data);
                }else{
                    $('#tablePegawai').DataTable();
                }
            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            })
        })
    },
    'columns': [
        {
            "targets": [0],
            "visible": false,
            "data": '_id',
        },
        {
            "targets": [1],
            "width": "3%",
            "render": function () {
                return '<i class="fa fa-user-o" aria-hidden="true"></i>';
            },
        },
        {
            "targets": [2],
            "width": "20%",
            "data": 'pegawaiid',
            "className": "dt-center"
        },
        {
            "targets": [3],
            "width": "74%",
            "data": 'nama',
            "className": "dt-center"
        },
        {
            "targets": [4],
            "width": "3%",
            "render": function () {
                return '<a id="info" class="btn btn-primary btn-flat"><i class="fa fa-info-circle" aria-hidden="true"></i></a>';
            }
        }
    ],
    'responsive': true,
    'paging': true,
    'pagingType': 'simple_numbers',
    'lengthChange': false,
    'pageLength': 20,
    'ordering': false,
    'searching': false,
    'info': true
});