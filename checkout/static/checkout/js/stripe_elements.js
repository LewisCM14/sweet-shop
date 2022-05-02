/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-card-payments?platform=web&ui=elements
*/

// Collect the stripePublicKey and ClientSecret from the checkout template.
// Slice off the quotation marks and collect the text
// Using the stripe.js in the base template and the public key,
// create an instance of stripe elements and mount to the specified div.

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#333333',
        fontFamily: "'Chivo', sans-serif",
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#747d84'
        }
    },
    invalid: {
        color: '#B30012',
        iconColor: '#B30012'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
// listener on the card element detects the change event.
// Every time it changes, check to see if there are any errors.
// Displaying them in the card errors div.

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
// Collects the form element from the template and places an event listener on the submit button.
// Once triggered disables the submit button and stripe card element, preventing multiple submissions.
// Then calls the stripe ConfirmCardPayment method with the clientSecret. Passing it the payment_method.
// Then on the result of this function either displays the error message and re-enables the submit button and element,
// or sets the paymentIntent status of the order to 'succeeded' and submits the form.

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});