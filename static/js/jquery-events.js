// when html document is ready
$(document).ready(function () {
    // put into variable element with id notification(django notifications)
    var notification = $('#notification');
    // make it disappear after 7 seconds
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // show cart modal window after click on cart icon
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // hide cart window after click on button
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // shipping method radiobutton
    $("input[name='requires_delivery']").change(function() {
        var selectedValue = $(this).val();
        // show/hide shipping address input
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

});