const $pickupButton = document.querySelector('#pickup-button');

$pickupButton.addEventListener('click', () => {
  fetch(pickupUrl)
    .then(response => response.json())
    .then(data => {
      toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-bottom-full-width",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
      };
      if (data.success) {
        location.reload();
      } else {
        toastr.error(data.message);
      }
    })
});
