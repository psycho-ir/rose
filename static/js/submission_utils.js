/**
 * Created by soroosh on 6/22/14.
 */


function initialize_form_validation(settings) {
    after_request = settings.afterRquest;
    ajax_loader_src = settings.ajaxLoaderSource;
    afterSuccess = settings.afterSuccess;
    $('#submit_forms form').find('input,select,textarea').not('[type=submit]').jqBootstrapValidation({
        autoAdd: {helpBlocks: false},
        submitSuccess: function ($form, event) {
            var form_id = $form.attr('id');
            var form_common = form_id.substr(0, form_id.lastIndexOf('_form'));
            var loader_id = form_common + '_loader';
            var state_id = form_common + '_state';
            $('#' + loader_id).html("<img src=\'" + ajax_loader_src + "' />");
            var form = $form;
            $.post(form.attr('action'), form.serialize(),
                function (data, state) {
                    if (state == 'success') {
                        console.log(data);
                        obj = JSON.parse(data);
                        if (obj.status == true) {

                            $('#' + state_id + ' #failed').hide();
                            $('#' + state_id + ' #ok').show();
                            $('#' + state_id).parent().parent().removeClass('pending').addClass('completed')
                            afterSuccess();
                        }
                        else {
                            if (obj.error_message) {
                                alertBar(obj.error_message);
                            }
                            $('#' + state_id + ' #failed').show();
                            $('#' + state_id + ' #ok').hide();
                        }
                        console.log(after_request);
                        if (after_request) {
                            after_request();
                        }
                    } else {
                        alertBar('خطا در برقراری ارتباط با سرور. لطفا مجددا تلاش کنید');
                    }
                    $('#' + loader_id).empty();
                });


            event.preventDefault();
        }

    });
}
