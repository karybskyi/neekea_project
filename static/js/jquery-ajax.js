// When html document is ready(rendered)
$(document).ready(function () {
    // Put into variable dom-element with id jq-notification(ajax notifications)
    var successMessage = $("#jq-notification");

    // Catch "click on 'add to cart' button" event
    $(document).on("click", ".add-to-cart", function (e) {
        // Block it's default action
        e.preventDefault();

        // Get number of products in cart via counter element in 'cart button'
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get product id via additional attribute (data-product-id) of add_to_cart button
        var product_id = $(this).data("product-id");

        // Get django-view url from 'href' attribute
        var add_to_cart_url = $(this).attr("href");

        // Send POST request via ajax with no page reload
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Show message
                successMessage.html(data.message);
                successMessage.css({ display: "block", opacity: 0 }).animate({ opacity: 1 }, { duration: 400, queue: false });
                // Hide message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Increase number of products in cart(render within template)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Change cart content on response from django(new render of markup for cart block)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Adding item to cart error");
            },
        });
    });

    // Catch "click on 'remove from cart' button" event
    $(document).on("click", ".remove-from-cart", function (e) {
        // Block it's default action
        e.preventDefault();

        // Get number of products in cart via counter element in 'cart button'
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Get cart id via additional attribute (data-cart-id) of remove_from_cart button
        var cart_id = $(this).data("cart-id");
        // Get django-view url from 'href' attribute
        var remove_from_cart_url = $(this).attr("href");

        // Send POST request via ajax with no page reload
        $.ajax({

            type: "POST",
            url: remove_from_cart_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Show message
                successMessage.html(data.message);
                successMessage.css({ display: "block", opacity: 0 }).animate({ opacity: 1 }, { duration: 400, queue: false });
                // Hide message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Decrease number of products in cart(render within template)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Change cart content on response from django(new render of markup for cart block)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Removing item from cart error");
            },
        });
    });

    // INcreasing and DEcreasing number of products 

    // DEcreasing number of products event listener
    $(document).on("click", ".decrement", function () {
        // Get django-view url from 'cart-change-url' attribute
        var url = $(this).data("cart-change-url");
        // Get cart id via additional attribute (data-cart-id) of remove_from_cart button
        var cartID = $(this).data("cart-id");
        // Get closest input for quantity
        var $input = $(this).closest('.input-group').find('.number');
        // Get value of products quantity  
        var currentValue = parseInt($input.val());
        // Do '-1' only if quantity > 1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Run updateCart function with next arguments
            // (id of cart, new quantity, INcrease/DEcrease, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // INcreasing number of products event listener
    $(document).on("click", ".increment", function () {
        // Get django-view url from 'cart-change-url' attribute
        var url = $(this).data("cart-change-url");
        // Get cart id via additional attribute (data-cart-id) of remove_from_cart button
        var cartID = $(this).data("cart-id");
        // Get closest input for quantity
        var $input = $(this).closest('.input-group').find('.number');
        // Get value of products quantity  
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Run updateCart function with next arguments
        // (id of cart, new quantity, INcrease/DEcrease, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Show message
                successMessage.html(data.message);
                successMessage.css({ display: "block", opacity: 0 }).animate({ opacity: 1 }, { duration: 400, queue: false });
                // Hide message after 7 seconds
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                //Change products quantity in cart
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Change cart content
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Cart updating error");
            },
        });
    }

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
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // show/hide shipping address input
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });
});