const $cardComponent = document.querySelector('#new-card');
const $payButton = document.querySelector('#submit');
const $saveCardCheck = document.querySelector('#save-card');
const $addressItems = document.querySelectorAll('.address-item');
const $paymentItems = document.querySelectorAll('.payment-item');

let loading = false
let currentItem = null;
let currentAddress = null;
let newCard = false;
$payButton.disabled = true;

fetch(stripeKeyUrl)
  .then(result => result.json())
  .then(setupElements)
  .then(({ stripe, card, clientSecret }) => {
    checkPayButton()
    $payButton.addEventListener('click', () => {
      if (currentItem) {
        if (newCard) {
          payWithNewCard(stripe, card, clientSecret);
        } else {
          pay(stripe)
        }
      }
    });
  });

function setupElements(data) {
  const stripe = Stripe(publishableKey);
  const elements = stripe.elements();
  const style = {
    base: {
      color: "#32325d",
      fontFamily: 'Nunito, "Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4"
      }
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545"
    }
  };

  const card = elements.create('card', { style: style });
  card.mount('#card-element');
  card.addEventListener('change', displayErrors);

  return {
    stripe: stripe,
    card: card,
    clientSecret: data.clientSecret
  };
};


function payWithNewCard(stripe, card, clientSecret) {
  changeLoadingState(true);
  const paymentSettings = {
    payment_method: {
      card: card,
      billing_details: {
        name
      }
    }
  }

  if ($saveCardCheck.checked) {
    paymentSettings.setup_future_usage = 'off_session';
  }

  stripe.confirmCardPayment(clientSecret, paymentSettings)
    .then(function(result) {
      if (result.error) {
        Swal.fire({
          title: 'Lo sentimos...',
          text: result.error.message,
          icon: 'error',
          confirmButtonText: 'Entendido'
        })
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          submitForm(result.paymentIntent.id)
        }
      }
    });
};

function pay(stripe) {
  changeLoadingState(true);
  const paymentId = currentItem.dataset.paymentId;
  const csrftoken = Cookies.get('csrftoken'); 
  const data = new FormData();
  data.append('paymentId', paymentId);
  fetch(payUrl, {
      method: 'POST',
      body: data,
      headers: {
        'X-CSRFToken': csrftoken,
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'succeeded') {
        submitForm(data.id)
      } else {
        stripe.confirmCardPayment(data.client_secret, {
          payment_method: paymentId
        }).then(function(result) {
          if (result.error) {
            Swal.fire({
              title: 'Lo sentimos...',
              text: result.error.message,
              icon: 'error',
              confirmButtonText: 'Entendido'
            })
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              submitForm(result.paymentIntent.id)
            }
          }
        });
      }
    })
}

function submitForm(intentId) {
  document.querySelector('#address_id').value = currentAddress.dataset.addressId;
  document.querySelector('#intent_id').value = intentId;
  const $form = document.querySelector('#form');
  $form.submit()
}


function changeLoadingState(isLoading) {
  if (isLoading) {
    $payButton.disabled = true;
    document.querySelector("#spinner").classList.remove("d-none");
    document.querySelector("#button-text").classList.add("d-none");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("d-none");
    document.querySelector("#button-text").classList.remove("d-none");
  }
};


function displayErrors(event) {
  const $displayError = document.getElementById('card-errors');
  if (event.error) {
    $displayError.textContent = event.error.message;
  } else {
    $displayError.textContent = '';
  }
}

function checkPayButton() {
  if (currentItem && currentAddress) {
    $payButton.disabled = false;
  } else {
    $payButton.disabled = true;
  }
}

for (const paymentItem of $paymentItems) {
  paymentItem.addEventListener('click', () => {
    if (!loading) {
      if (currentItem !== paymentItem) {
        if (currentItem) currentItem.classList.remove('active');
        paymentItem.classList.add('active');
        currentItem = paymentItem;
        if (paymentItem.classList.contains('new-card-item')) {
          newCard = true
          $cardComponent.classList.remove('d-none');
        } else {
          newCard = false
          $cardComponent.classList.add('d-none');
        }
      } else {
        currentItem = null
        $cardComponent.classList.add('d-none');
        paymentItem.classList.remove('active');
      }
      checkPayButton()
    }
  })
}

const urlParams = new URLSearchParams(window.location.search);
const urlAddressId = urlParams.get('address');

for (const addressItem of $addressItems) {
  const addressId = addressItem.dataset.addressId
  if (urlAddressId === addressId) {
    addressItem.classList.add('active');
    currentAddress = addressItem
  }
  addressItem.addEventListener('click', () => {
    if (!loading) {
      if (addressItem !== currentAddress) {
        if (currentAddress) currentAddress.classList.remove('active');
        addressItem.classList.add('active')
        currentAddress = addressItem;
      } else {
        currentAddress = null
        addressItem.classList.remove('active');
      }
      checkPayButton()
    }
  });
}

