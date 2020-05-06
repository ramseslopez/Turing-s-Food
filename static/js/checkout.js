const $payButton = document.querySelector('#submit');
const $cardComponent = document.querySelector('#new-card');
const $paymentItems = document.querySelectorAll('.payment-item');
const $saveCardCheck = document.querySelector('#save-card');

let currentItem = null;
let newCard = false;
$payButton.disabled = true;

fetch(stripeKeyUrl)
  .then(result => result.json())
  .then(setupElements)
  .then(({ stripe, card, clientSecret }) => {
    $payButton.disabled = false;
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
  // changeLoadingState(true);
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
          redirectToSuccessUrl()
        }
      }
    });
};

function pay(stripe) {
  // changeLoadingState(true);
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
      if (data.status !== 'succeeded') {
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
              redirectToSuccessUrl()
            }
          }
        });
      } else {
        redirectToSuccessUrl()
      }
    })
}

function redirectToSuccessUrl() {
  window.location.href = successUrl + '?cola=hola';
}


function changeLoadingState(isLoading) {
  if (isLoading) {
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};


function displayErrors(event) {
  const $displayError = document.getElementById('card-errors');
  if (event.error) {
    $displayError .textContent = event.error.message;
  } else {
    $displayError .textContent = '';
  }
}

for (const paymentItem of $paymentItems) {
  paymentItem.addEventListener('click', () => {
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
  })
}

