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


function chooseDate() {
    const start_date = $('#from').datepicker('getDate').toUTCString();
    const end_date = $('#to').datepicker('getDate').toUTCString();

    const location = document.querySelector('#location_item').value;
    if (location == 'All') {
        window.location.href = "/search/" + start_date + "/" + end_date;
    } else {
        window.location.href = "/search/" + start_date + "/" + end_date + "/" + location;
    }
}

function viewDeal(){
    window.location.href = "/";
}