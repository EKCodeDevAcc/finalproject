// datepick function
var start_date, end_date;

$(function() {

    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();
    if(dd<10){ dd='0'+dd }
    if(mm<10){ mm='0'+mm }
    var today = mm+'/'+dd+'/'+yyyy;

    $('input[name="daterange"]').daterangepicker({
        opens: 'left',
        minDate: today
    }, function(start, end, label) {
        const start_string = start.format('YYYY-MM-DD');
        const end_string = end.format('YYYY-MM-DD');
        var start_obj = new Date(start_string);
        var end_obj = new Date(end_string);
        start_date = start_obj.toUTCString();
        end_date = end_obj.toUTCString();
    });
});

// Pass location, start date, end date information.
function chooseDate() {
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