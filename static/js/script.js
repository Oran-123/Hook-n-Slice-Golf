$(document).ready(function () {
    $('#calendar').fullCalendar({
    });
});


function submitLoginFormAndRedirect() {
    document.querySelector('form.login').submit(); // Submit the form

    // Redirect the user to the desired page
    if (userIsAdmin) {
        window.location.href = "{% url 'manage_bookings' %}";  // Redirect to the admin page
    } else {
        window.location.href = "{% url 'user_profile' %}";  // Redirect to the user profile page
    }
}