$(document).ready(function () {
    $('#calendar').fullCalendar({
    });
});

function setBookingId(bookingId) {
    document.getElementById("bookingIdInput").value = bookingId;
}