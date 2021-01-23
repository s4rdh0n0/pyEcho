+ function ($) {
    'use strict';

    $('#formCariBerkas').validate({
        rules: {
            nomorBerkas: {
                digits: true
            },
            tahunBerkas: {
                digits: true
            }
        },
        messages: {
            nomorBerkas: {
                digits: 'Nomor berkas wajib angka'
            },
            tahunBerkas: {
                digits: 'Tahun berkas wajib angka'
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
            $('#tableBerkas').DataTable().ajax.reload(null, false);
        }
    });

    $("#btnResetFilter").click(function () {
        $('#nomorBerkas').val("");
        $('#tahunBerkas').val("");
        $('#tableBerkas').DataTable().ajax.reload(null, false);
    });

    // NOTE: Info Berkas
    $('#tableBerkas tbody').on('click', '#btnInfo', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tableBerkas.row(selected_row).data()[0] != "") {
            run_wait('#tabDetail');
            $('.nav-tabs a[href="#tabDetail"]').tab('show');
            $('#berkasView').load('/register/compose/berkasid=' + tableBerkas.row(selected_row).data()['_id'] + '&type=INFO', function () {
                $('#tabDetail').waitMe("hide");
            });
        }

        return false
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

/* Initial Table Berkas */
var tableBerkas = $('#tableBerkas').DataTable({
    'processing': true,
    'serverSide': true,
    'ajax': function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/register/compose/list',
            data: JSON.stringify({
                // NOTE: Query table berkas
                nomor: $('#nomorBerkas').val(),
                tahun: $('#tahunBerkas').val(),
                page: $('#tableBerkas').DataTable().page.info()['page'],
                start: $('#tableBerkas').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tableBerkas').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tableBerkas').dataTable().fnSettings().iDraw,
            }),
            async: true,
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                if (typeof (data.data) == "string") {
                    data.data = JSON.parse(data.data)
                    callback(data)
                } else {
                    callback(data)
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
        }, {
            "targets": [1],
            "width": "3%",
            "data": 'nomorregister',
            "className": "dt-center text-center"
        },{
            "targets": [2],
            "width": "5%",
            "data": 'userregisterindate',
            "className": "dt-center text-center",
            "render": function (data) {
                var date = new Date(data.$date);
                var month = date.getUTCMonth() + 1;
                return (date.getUTCDate().toString().length > 1 ? date.getUTCDate() : "0" + date.getUTCDate()) + "/" + (month.toString().length > 1 ? month : "0" + month) + "/" + date.getUTCFullYear() + "  " + (date.getUTCHours().toString().length > 1 ? date.getUTCHours() : "0" + date.getUTCHours()) + ":" + (date.getUTCMinutes().toString().length > 1 ? date.getUTCMinutes() : "0" + date.getUTCMinutes()) + ":" + (date.getUTCSeconds().toString().length > 1 ? date.getUTCSeconds() : "0" + date.getUTCSeconds());
            }
        }, {
            "targets": [3],
            "width": "10%",
            "data": 'userregisterinname',
            "className": "dt-center text-center"
        }, {
            "targets": [4],
            "width": "5%",
            "data": 'nomorberkas',
            "className": "dt-center text-center"
        }, {
            "targets": [5],
            "width": "5%",
            "data": 'tahunberkas',
            "className": "dt-center text-center"
        },{
            "targets": [6],
            "width": "10%",
            "data": 'kegiatan',
            "className": "dt-center text-center"
        }, {
            "targets": [7],
            "width": "20%",
            "data": 'prosedur',
            "className": "dt-center text-center"
        }, {
            "targets": [8],
            "width": "3%",
            "data": 'status',
            "className": "dt-center text-center"
        },{
            "targets": [9],
            "width": "3%",
            "data": 'status',
            "className": "dt-center text-center",
            "render": function (data) {
                return '<a id="btnInfo" class="btn btn-default btn-flat"><i class="fa fa-info-circle" aria-hidden="true"></i></a>'
            }
        }
    ],
    dom: 'Bfrtip',
    buttons: [
        {
            extend: 'csv',
            text: 'Export CSV',
            className: 'btn-space',
            exportOptions: {
                orthogonal: null
            }
        }
    ],
    "oLanguage": {
        "sProcessing": "<b>Sedang proses...</b> <br> harap tunggu"
    },
    'responsive': true,
    'paging': true,
    'autoWidth': true,
    'pagingType': 'simple_numbers',
    'lengthChange': false,
    'pageLength': 20,
    'ordering': false,
    'searching': false,
    'info': true
});