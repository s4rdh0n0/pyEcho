+ function ($) {
    'use strict';

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
                url: '/administrator/daftarpegawai/kkp/username=' + $('#username').val(),
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (data) {
                    if (data.status) {
                        console.log(data.data)
                    } else {
                        console.log('Bukan pegawai kantor ini.')
                    }
                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            })
        }
    });

}(jQuery);


/* Initial Table Pegawai */
var tablePegawai = $('#tablePegawai').DataTable({
    'processing': true,
    "serverSide": true,
    "ajax": function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/administrator/daftarpegawai',
            data: JSON.stringify({
                page: $('#tablePegawai').DataTable().page.info()['page'],
                start: $('#tablePegawai').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tablePegawai').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tablePegawai').dataTable().fnSettings().iDraw,
            }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                // NOTE: print data
                console.log(data)
                
                // NOTE: callback response ajax
                if (data.status){
                    callback(data);
                }else{
                    alert("Error: " + data.msg)
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
            "data": 'pegawaiid',
            "className": "dt-center"
        },
        {
            "targets": [3],
            "visible": false,
            "data": 'username'
        },
        {
            "targets": [4],
            "data": 'nama',
            "className": "dt-center"
        },
        {
            "targets": [5],
            "width": "3%",
            "render": function () {
                return '<a id="lihat" class="btn btn-primary btn-flat"><i class="fa fa-info-circle" aria-hidden="true"></i></a>';
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