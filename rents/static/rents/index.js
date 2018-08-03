var startdate, enddate;

// datepick function
$(function() {
    var dateFormat = "mm/dd/yy",
    from = $("#from").datepicker({
        defaultDate: "+1w",
        changeMonth: false,
        minDate: 0,
        maxDate: "+1M",
        numberOfMonths: 1
    })
    .on("change", function() {
        to.datepicker("option", "minDate", getDate(this));
    }),
    to = $("#to").datepicker({
        defaultDate: "+1w",
        changeMonth: false,
        minDate: 0,
        maxDate: "+1M",
        numberOfMonths: 1
    })
    .on("change", function() {
        from.datepicker("option", "maxDate", getDate(this));
    });

    function getDate(element) {
        var date;
        try {
            date = $.datepicker.parseDate(dateFormat, element.value);
        } catch( error ) {
            date = null;
        }
    }
});

//
function chooseDate(){
    const start_date = $('#from').datepicker('getDate').toUTCString();
    const end_date = $('#to').datepicker('getDate').toUTCString();
    window.location.href = "/search/" + start_date + "/" + end_date;
}










// add a selected item into current user's cart.
function addToCart(item_type, item_name, item_price, item_size, item_pizza_topping, item_sub_topping) {
    $.ajax({
        url: '/addCart',
        data: {
            itemtype: item_type,
            itemname: item_name,
            itemprice: item_price,
            itemsize: item_size,
            itempizzatopping: item_pizza_topping,
            itemsubtopping: item_sub_topping
        },
        success: function(data){
            location.reload();
        }
    });
};

// remove an item from the cart.
function removeCart(item_id) {
    $.ajax({
        url: '/removeCart',
        data: {
            itemid: item_id,
        },
        success: function(data){
            location.reload();
        }
    });
};

// create an order and put all items in the cart in the order.
function checkoutCart(order_price){
    var float_price = parseFloat(order_price).toFixed(2);
    $.ajax({
        url: '/checkoutCart',
        data: {
            orderprice: float_price,
        },
        success: function(data){
            // alert message then redirect user to myOrders page.
            alert("Thank you for choosing Pinocchio's Pizza & Subs!");
            window.location = "/myOrders";
        }
    });
};

// When user choose regular, sicilian pizza, display modal of pizza toppings depends on situation
function addPizzaToppings(item_type, item_name, item_price, item_size, topping_size) {
    // If it is cheese pizza, just trigger addToCart function right away.
    if (topping_size == 0) {
        addToCart(item_type, item_name, item_price, item_size, '', '');
    } else {
        // For other pizza, get the modal
        var modal = document.getElementById('pizzaModal');
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];
        modal.style.display = "block";
        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
            location.reload();
        }
        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                location.reload();
            }
        }
        // Message that shows a user how many toppings are required
        const topping_message = document.createElement('h4');
        topping_message.innerHTML = "Please select " + topping_size + " toppings.";
        document.querySelector('#topping_message').append(topping_message);
        //If number of checked checkboxes are equal to the number of toppings, deny checking current checkbox
        $(document).ready(function() {
            $('input.topping_check').on('change', function(evt) {
                if ($(this).siblings(':checked').length == topping_size) {
                    this.checked = false;
                }
            });
        });
        var select_button = document.querySelector('#topping_complete');
        var total_topping_length = document.querySelector('#total_topping_length').innerHTML;
        select_button.onclick = function() {
            // Check how many toppings are actually selected
            var unchecked_length = $("input:checkbox[class=topping_check]:not(:checked)").length;
            var checked_length = total_topping_length - unchecked_length;

            if (topping_size > 0) {
                // When user selected less than required toppings, alert it.
                if (checked_length != topping_size) {
                    alert("Please select " + topping_size + " toppings.");
                } else {
                    // Get list of toppings
                    var final_toppings = new Array();
                    var checked = document.querySelector('.topping_check:checked').value;

                    $(document).ready(function() {
                        $("input:checkbox[class=topping_check]:checked").each(function(){
                            final_toppings = final_toppings + $(this).val() + ', ';
                        });
                    });
                    final_toppings = final_toppings.substring(0, final_toppings.length - 2);
                }
            } else {
                final_toppings = "";
            }
            //Trigger addToCart function
            addToCart(item_type, item_name, item_price, item_size, final_toppings, '');
        }
    };
};

function addSubsToppings(item_type, item_name, item_price, item_size, topping_size) {
    // Get list of toppings and their checkboxes
    var mushrooms = document.getElementById('Mushrooms');
    var pmushrooms = document.getElementById('p_Mushrooms');
    var green_peppers = document.getElementById('Green Peppers');
    var pgreen_peppers = document.getElementById('p_Green Peppers');
    var onions = document.getElementById('Onions');
    var ponions = document.getElementById('p_Onions');
    // If a choosen sub is not steak & cheese, do not display mushroom, green peppers, and onions
    if (item_name != 'Steak + Cheese'){
        mushrooms.style.display = "none";
        pmushrooms.style.display = "none";
        green_peppers.style.display = "none";
        pgreen_peppers.style.display = "none";
        onions.style.display = "none";
        ponions.style.display = "none";
    }
    var modal = document.getElementById('subsModal');
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = "block";
    span.onclick = function() {
        modal.style.display = "none";
        location.reload();
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            location.reload();
        }
    }
    var select_button = document.querySelector('#sub_topping_complete');
    var total_topping_length = document.querySelector('#sub_topping_length').innerHTML;
    select_button.onclick = function() {
        var unchecked_length = $("input:checkbox[class=sub_topping_check]:not(:checked)").length;
        var checked_length = total_topping_length - unchecked_length;

        if (checked_length == 0) {
            final_toppings = "";
        } else {
            var final_toppings = new Array();
            var checked = document.querySelector('.sub_topping_check:checked').value;

            $(document).ready(function() {
                $("input:checkbox[class=sub_topping_check]:checked").each(function(){
                    final_toppings = final_toppings + $(this).val() + ', ';
                });
            });
            final_toppings = final_toppings.substring(0, final_toppings.length - 2);
            // Get number of toppoings and add extra toppings cost to its item price.
            var extra = checked_length * .5;
            var float_item = parseFloat(item_price);
            item_price = float_item + extra;
        }
        addToCart(item_type, item_name, item_price, item_size, '', final_toppings);
    }
};

function changeOrderStatus(order_status, order_length) {
    var unchecked_length = $("input:checkbox[class=change_order_status]:not(:checked)").length;
    var checked_length = order_length - unchecked_length;
    // If admin selected more than equal to 1 order, change status of choosen orders
    if (checked_length > 0) {
        var final_orders = new Array();
        var checked = document.querySelector('.change_order_status:checked').value;

        $(document).ready(function() {
            $("input:checkbox[class=change_order_status]:checked").each(function(){
                final_orders = final_orders + $(this).val() + ', ';
            });
        });
        final_orders = final_orders.substring(0, final_orders.length - 2);

        $.ajax({
            url: '/changeOrderStatus',
            data: {
                orderstatus: order_status,
                finalorders: final_orders
            },
            success: function(data){
                location.reload();
            }
        });
    } else {
        alert("Please select at least one item to change its status!");
    }
}

function selectOrderDetails(order_id) {
    $.ajax({
        url: '/orderDetails',
        data: {
            orderid: order_id
        },
        success: function(data) {
            var modal = document.getElementById('orderModal');
            var span = document.getElementsByClassName("close")[0];
            modal.style.display = "block";
            span.onclick = function() {
                modal.style.display = "none";
                location.reload();
            }
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                    location.reload();
                }
            }
            var total_price = 0;
            // Get numer of items of choosen order
            for (var i=0; i<data.length; i++) {
                // Create new table elements that will contain item type, name, size, toppings, price, and its status for number of items
                const details = Object.values(data[i])
                const newTr = document.createElement('tr');
                const menu_type = document.createElement('td');
                menu_type.innerHTML = details[2].item_type;
                newTr.append(menu_type);
                const menu_name = document.createElement('td');
                menu_name.innerHTML = details[2].item_menu_name;
                newTr.append(menu_name);
                const menu_size = document.createElement('td');
                menu_size.innerHTML = details[2].item_size;
                newTr.append(menu_size);
                const menu_topping = document.createElement('td');
                if (details[2].topping_pizza != '') {
                    menu_topping.innerHTML = details[2].topping_pizza;
                } else if (details[2].topping_sub != '') {
                    menu_topping.innerHTML = details[2].topping_sub;
                } else {
                    menu_topping.innerHTML = '';
                }
                newTr.append(menu_topping);

                const menu_price = document.createElement('td');
                menu_price.innerHTML = '$ ' + details[2].item_price;
                newTr.append(menu_price);
                const menu_status = document.createElement('td');
                menu_status.innerHTML = details[2].item_status;
                newTr.append(menu_status);
                document.querySelector('#order_details').append(newTr);

                total_price = total_price + details[2].item_price;
            }
            // Create elemnts for total price text
            const costDiv = document.createElement('h4');
            costDiv.innerHTML = 'Total Price: $ ' + total_price;
            costDiv.className = 'total_cost'
            document.querySelector('#order_total_price').append(costDiv);
        }
    });
}