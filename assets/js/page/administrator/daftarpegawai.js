+ function ($) {
    'use strict';

    $('#inputPegawaiid').keypress(function (e) {
        if (e.which == 13) {
            $('#tablePegawai').DataTable().ajax.reload(null, false);
            return false;    //<---- Add this line
        }
    });

    $("#btnFilterPegawaiid").click(function () {
        $('#tablePegawai').DataTable().ajax.reload(null, false);
    });

    $("#btnResetFilter").click(function () {
        $('#inputPegawaiid').val("")
        $('#tablePegawai').DataTable().ajax.reload(null, false);
    });

    // NOTE: Form Activation Pegawai
    $('#formActivation').validate({
        rules: {
            inputUsername: {
                required: true,
            }
        },
        messages: {
            inputUsername: {
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
                type: 'PUT',
                url: '/administrator/daftarpegawai/pegawai',
                data: JSON.stringify({
                    username: $('#inputUsername').val(),
                }),
                async: true,   
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                beforeSend: function () {
                    $('#userView').empty();
                },
                success: (function (data) {

                    if (data.status) {
                        $('#userView').load('/administrator/daftarpegawai/pegawai/view/username=' + data.username);
                    } else {
                        $('#modal-activation').modal('hide');
                        $.notify({
                            title: '<strong>Perhatian</strong> <br>',
                            message: data.msg,
                        }, {
                            type: data.type,
                            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                                '<span data-notify="title">{1}</span>' +
                                '<span data-notify="message">{2}</span>' +
                                '</div>',
                            animate: {
                                enter: 'animated fadeInRight',
                                exit: 'animated fadeOutRight'
                            }
                        });
                    }

                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });

            return false
        }

    });

    // NOTE: modal-activation show
    $('#modal-activation').on('show.bs.modal', function () {
        $('#userView').empty();
    });

    // NOTE: modal-activation hide
    $('#modal-activation').on('hide.bs.modal', function () {
        $('#inputUsername').val("");
        $('#userView').empty();
        $('#tablePegawai').DataTable().ajax.reload(null, false);
    });

    // NOTE: modal-role hide
    $('#modal-role').on('hide.bs.modal', function () {
        $('#userRole').empty();
        $('#tablePegawai').DataTable().ajax.reload(null, false);
    });

    // Role Pegawai
    $('#tablePegawai tbody').on('click', '#btnRolePegawai', function () {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tablePegawai.row(selected_row).data()[0] != "") { 
            $('#userRole').load('/administrator/daftarpegawai/role/view/userid=' + tablePegawai.row(selected_row).data()['_id'], function () {

                $("#typeRole").select2({
                    placeholder: "Pilih role..",
                    theme: "bootstrap"
                });

                // Add Role Pegawai
                $("#formAddRole").submit(function () {
                    $.ajax({
                        type: 'PUT',
                        url: '/administrator/daftarpegawai/role/add',
                        data: JSON.stringify({
                            userid: tablePegawai.row(selected_row).data()['_id'],
                            key: $('#typeRole').val(),
                        }),
                        async: true,   
                        headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                        success: (function (result) {
                            $('#tableRole').DataTable().ajax.reload();
                        }),
                        error: (function (XMLHttpRequest, textStatus, errorThrown) {
                            alert("Error: " + errorThrown);
                        })
                    });

                    return false
                });

                // Delete Role Pegawai
                $('#tableRole tbody').on('click', '#btnDeleteRole', function (event) {
                    var selected_row = $(this).parents('tr');
                    if (selected_row.hasClass('child')) {
                        selected_row = selected_row.prev();
                    }

                    if (tableRole.row(selected_row).data()[0] != "") {
                        event.preventDefault();
                        $.ajax({
                            type: 'DELETE',
                            url: '/administrator/daftarpegawai/role/delete',
                            data: JSON.stringify({
                                userid: $('input[name=userid]').val(),
                                key: tableRole.row(selected_row).data()['key']
                            }),
                            async: true,   
                            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                            success: (function (data) {
                                if (data.status) {
                                    tableRole.row(selected_row).remove().draw();
                                } else {
                                    tableRole.ajax.reload(false, null);
                                }
                            }),
                            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                                alert("Error: " + errorThrown);
                            })
                        });
                    }
                });

                /* Initial Table Role */
                var tableRole = $('#tableRole').DataTable({
                    'processing': true,
                    'serverSide': true,
                    'ajax': function (data, callback) {
                        $.ajax({
                            type: 'POST',
                            url: '/administrator/daftarpegawai/role',
                            data: JSON.stringify({
                                userid: tablePegawai.row(selected_row).data()['_id'],
                            }),
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
                    "oLanguage": {
                        "sProcessing": "<b>Sedang proses...</b> <br> harap tunggu"
                    },
                    'columns': [
                        {
                            "targets": [0],
                            "visible": false,
                            "data": 'key',
                        }, {
                            "targets": [1],
                            "width": "5%",
                            "className": "dt-center text-center",
                            "render": function (data, type, row, meta) {
                                return meta.row + meta.settings._iDisplayStart + 1;
                            }
                        }, {
                            "targets": [2],
                            "width": "70%",
                            "data": 'description',
                            "className": "dt-center text-center",
                        }, {
                            "targets": [3],
                            "width": "20%",
                            "data": 'startdate',
                            "className": "dt-center text-center",
                            "render": function (data) {
                                var date = new Date(data.$date);
                                var month = date.getUTCMonth() + 1;
                                return (date.getUTCDate().toString().length > 1 ? date.getUTCDate() : "0" + date.getUTCDate()) + "/" + (month.toString().length > 1 ? month : "0" + month) + "/" + date.getUTCFullYear() + "  " + (date.getUTCHours().toString().length > 1 ? date.getUTCHours() : "0" + date.getUTCHours()) + ":" + (date.getUTCMinutes().toString().length > 1 ? date.getUTCMinutes() : "0" + date.getUTCMinutes()) + ":" + (date.getUTCSeconds().toString().length > 1 ? date.getUTCSeconds() : "0" + date.getUTCSeconds());
                            }
                        }, {
                            "targets": [4],
                            "width": "5%",
                            "className": "dt-center text-center",
                            "render": function () {
                                return '<a id="btnDeleteRole" class="btn btn-danger btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                            }
                        }
                    ],
                    'responsive': true,
                    'paging': false,
                    'autoWidth': true,
                    'pagingType': 'simple_numbers',
                    'lengthChange': false,
                    'ordering': false,
                    'searching': false,
                    'info': true
                });
            });           
            $('#modal-role').modal('show');
        }
    });

    // NOTE: Deactivation Pegawai
    $('#tablePegawai tbody').on('click', '#btnDeactivation', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }
        
        if (tablePegawai.row(selected_row).data()[0] != "") {
            var pesan
            if (tablePegawai.row(selected_row).data()['actived']){
                pesan = "AKAN DINONAKTIFKAN.....?"
            }else{
                pesan = "AKAN DIAKTIFKAN.....?"
            }
            var answer = window.confirm(tablePegawai.row(selected_row).data()['nama'].toUpperCase() + pesan );
            if (answer) {
                $.ajax({
                    type: 'PUT',
                    url: '/administrator/daftarpegawai/pegawai/status',
                    data: JSON.stringify({
                        userid: tablePegawai.row(selected_row).data()['_id'],
                    }),
                    async: true,
                    headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                    error: (function (XMLHttpRequest, textStatus, errorThrown) {
                        alert("Error: " + errorThrown);
                    })
                });
                $('#tablePegawai').DataTable().ajax.reload(null, false);
            }
        }

        return false
    });

}(jQuery);

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
                pegawaiid: $('#inputPegawaiid').val(),
            }),
            async: true,
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                if (typeof (data.data) == "string"){
                    data.data = JSON.parse(data.data)
                    callback(data)
                }else{
                    callback(data)
                }
            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            })
        })
    }, 'createdRow': function (row, data, dataIndex) {
        if (data['actived']) {
            $(row).removeClass('bg-red disabled color-palette');
        }else{
            $(row).addClass('bg-red disabled color-palette');
        }
    },
    'columns': [
        {
            "targets": [0],
            "visible": false,
            "data": '_id',
        },{
            "targets": [1],
            "width": "5%",
            "className": "dt-center text-center",
            "render": function (data, type, row, meta) {
                return meta.row + meta.settings._iDisplayStart + 1 ;
            }
        },{
            "targets": [2],
            "width": "20%",
            "data": 'pegawaiid',
            "className": "dt-center text-center"
        },{
            "targets": [3],
            "width": "51%",
            "data": 'nama',
            "className": "dt-center text-center",
            "render": function (data) {
                return data.toUpperCase();
            }
        },{
            "targets": [4],
            "width": "15%",
            "data": 'createdate',
            "className": "dt-center text-center",
            "render": function (data) {
                var date = new Date(data.$date);
                var month = date.getUTCMonth() + 1;
                return (date.getUTCDate().toString().length > 1 ? date.getUTCDate() : "0" + date.getUTCDate()) + "/" + (month.toString().length > 1 ? month : "0" + month) + "/" + date.getUTCFullYear() + "  " + (date.getUTCHours().toString().length > 1 ? date.getUTCHours() : "0" + date.getUTCHours()) + ":" + (date.getUTCMinutes().toString().length > 1 ? date.getUTCMinutes() : "0" + date.getUTCMinutes()) + ":" + (date.getUTCSeconds().toString().length > 1 ? date.getUTCSeconds() : "0" + date.getUTCSeconds());
            }
        },{
            "targets": [5],
            "width": "5%",
            "data": 'actived',
            "className": "dt-center text-center",
            "render": function (data) {
                if (data) {
                    return '<a id="btnRolePegawai" class="btn btn-primary btn-flat"><i class="fa fa-check-square-o" aria-hidden="true"></i></a>'
                }else{
                    return ''
                }
            }
        }, {
            "targets": [6],
            "width": "4%",
            "className": "dt-center text-center",
            "render": function (data, type, row) {
                if (row.actived){
                    return '<a id="btnDeactivation" class="btn btn-danger btn-flat btn-small"><i class="fa fa-unlock-alt" aria-hidden="true"></i></a>'
                }else{
                    return '<a id="btnDeactivation" class="btn btn-warning btn-flat btn-small"><i class="fa fa-unlock" aria-hidden="true"></i></a>'
                }
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