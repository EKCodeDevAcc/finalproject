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
    const age = document.querySelector('#age_item').value;

    window.location.href = "/search/" + start_date + "/" + end_date + "/" + location + "/" + age + "/price_desc";
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
    const age = document.querySelector('#given_age_value').innerHTML;

    window.location.href = "/search/" + start_date + "/" + end_date + "/" + location + "/" + age + "/" + sort_value;
};

// Select a deal to direct to detail views
function viewDeal(car_id, start_date, end_date, age) {
    window.location.href = "/reservation/" + car_id + "/" + start_date + "/" + end_date + "/" + age;
};


// Only display when a user is under 25 so there is young renter fee
$(function() {
    const young_fee = document.querySelector('#young_fee_item').innerHTML;
    var young_fee_tr = document.querySelector('#young_fee_tr');

    if (young_fee == 0){
        young_fee_tr.style.display = "none";
    }
});

var protection_status = 'No';

$(function() {
    $('input[type="radio"]').change(function(){
        const young_fee = document.querySelector('#young_fee_item').innerHTML;
        const date_num = document.querySelector('#given_date_diff').innerHTML;
        var protection_price_div = document.querySelector('#protection_price_div');

        if ($(this).val() == 'No') {
            protection_price_div.style.display = "none";
            protection_status = 'No';
        } else {
            protection_price_div.style.display = "unset";
            document.querySelector('#protection_item').innerHTML = date_num * 10
            protection_status = 'Yes';
        }
    });
});

//
function book(start_date, end_date, total_price) {
    const car_id = document.querySelector('#book_car_id').innerHTML;
    const date_num = document.querySelector('#given_date_diff').innerHTML;

    var final_price;

    if (protection_status == 'No') {
        final_price = parseFloat(total_price).toFixed(2);
    } else {
        final_price = +(parseFloat(total_price).toFixed(2)) + +(date_num * 10);
    }

    $.ajax({
        url: '/bookCar',
        data: {
            carid: car_id,
            startdate: start_date,
            enddate: end_date,
            totalprice: final_price,
            protection: protection_status
        },
        success: function(data){
            alert("hey");
        }
    });
};