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

// Pass location, start date, end date information.
function chooseDate() {
    const start_date = $('#from').datepicker('getDate').toUTCString();
    const end_date = $('#to').datepicker('getDate').toUTCString();
    const location = document.querySelector('#location_item').value;

    window.location.href = "/search/" + start_date + "/" + end_date + "/" + location + "/price_desc";
};

// Set default value of sort by dropdown item depends on sort value.
$(function() {
    const sort = document.querySelector('#given_sort_value').innerHTML;
    $('.sort_item').val(sort);
});

// Pass sort value to sort the search result.
function sortBy(sort_value) {
    const start_date = document.querySelector('#given_start_date_value').innerHTML;
    const end_date = document.querySelector('#given_end_date_value').innerHTML;
    const location = document.querySelector('#given_location_value').innerHTML;

    window.location.href = "/search/" + start_date + "/" + end_date + "/" + location + "/" + sort_value;
};

// Select a deal to direct to detail views
function viewDeal(car_id, start_date, end_date) {
    window.location.href = "/reservation/" + car_id + "/" + start_date + "/" + end_date;
};

//
function book(start_date, end_date, total_price) {
    const car_id = document.querySelector('#book_car_id').innerHTML;

    $.ajax({
        url: '/bookCar',
        data: {
            carid: car_id,
            startdate: start_date,
            enddate: end_date,
            totalprice: total_price
        },
        success: function(data){
            alert("hey");
        }
    });
};