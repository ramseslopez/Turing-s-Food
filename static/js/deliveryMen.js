const $removeForm = document.querySelector('#remove-form');
const $deletedItemInput = document.querySelector('#deleted-delivery-man');
const $deleteButtons = document.querySelectorAll('.delete-button');

const $emailInput = document.querySelector('#email');
const $addForm = document.querySelector('#add-form');

for (const deleteButton of $deleteButtons) {
  deleteButton.addEventListener('click', () => {
    $deletedItemInput.value = deleteButton.dataset.id;
    $removeForm.submit();
  });
}

$addForm.addEventListener('submit', e => {
  e.preventDefault();

  const csrftoken = Cookies.get('csrftoken');
  const data = new FormData();
  data.append('email', $emailInput.value);
  fetch(addDeliveryManUrl, {
      method: 'POST',
      body: data,
      headers: {
        'X-CSRFToken': csrftoken,
      }
    }
  )
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
        toastr.success(data.message);
      } else {
        toastr.error(data.message);
      }
    })
})