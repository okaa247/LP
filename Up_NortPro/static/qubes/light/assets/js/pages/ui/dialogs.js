$(function () {
  $('.js-sweetalert').on('click', function () {
    var type = $(this).data('type');
    if (type === 'basic') {
      showBasicMessage();
    } else if (type === 'with-title') {
      showWithTitleMessage();
    } else if (type === 'success') {
      showSuccessMessage();
    } else if (type === 'confirm') {
      showConfirmMessage();
    } else if (type === 'cancel') {
      showCancelMessage();
    } else if (type === 'with-custom-icon') {
      showWithCustomIconMessage();
    } else if (type === 'html-message') {
      showHtmlMessage();
    } else if (type === 'autoclose-timer') {
      showAutoCloseTimerMessage();
    } else if (type === 'prompt') {
      showPromptMessage();
    } else if (type === 'unsuccessful') {
      showUnsuccessfulMessage();
    } else if (type === 'ajax-loader') {
      showAjaxLoaderMessage();
    }
  });
});

//These codes takes from http://t4t5.github.io/sweetalert/
function showBasicMessage() {
  swal("Here's a message!");
}

function showWithTitleMessage() {
  swal("Here's a message!", "It's pretty, isn't it?");
}

function showSuccessMessage() {
  const el = document.createElement('div');
  el.className = 'group-link';
  el.innerHTML =
    "Important!  <a class='official-group-link' href='https://username.t.me/'> Join Official Group</a>";
  swal({
    title: 'E-mail verified successfully!',
    content: el,
    icon: 'success',
    text: 'Note: The official group link has also been sent to your email.',
    button: 'Close',
    closeOnClickOutside: false,
  });
}

function showUnsuccessfulMessage() {
  swal({
    title: 'E-mail verified unsuccessful!',
    //   content: el,
    icon: 'error',
    text: 'You enter wrong OTP code !',
    button: 'Close',
    closeOnClickOutside: false,
  });
}

function showConfirmMessage() {
  swal(
    {
      title: 'Are you sure?',
      text: 'You will not be able to recover this imaginary file!',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      confirmButtonText: 'Yes, delete it!',
      closeOnConfirm: false,
    },
    function () {
      swal('Deleted!', 'Your imaginary file has been deleted.', 'success');
    }
  );
}

function showCancelMessage() {
  swal(
    {
      title: 'Are you sure?',
      text: 'You will not be able to recover this imaginary file!',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel plx!',
      closeOnConfirm: false,
      closeOnCancel: false,
    },
    function (isConfirm) {
      if (isConfirm) {
        swal('Deleted!', 'Your imaginary file has been deleted.', 'success');
      } else {
        swal('Cancelled', 'Your imaginary file is safe :)', 'error');
      }
    }
  );
}

function showWithCustomIconMessage() {
  swal({
    title: 'Sweet!',
    text: "Here's a custom image.",
    imageUrl: '../assets/images/sm/avatar2.jpg',
  });
}

function showHtmlMessage() {
  swal({
    title: 'HTML <small>Title</small>!',
    text: 'A custom <span style="color: #CC0000">html<span> message.',
    html: true,
  });
}

function showAutoCloseTimerMessage() {
  swal({
    title: 'Auto close alert!',
    text: 'I will close in 2 seconds.',
    timer: 2000,
    showConfirmButton: false,
  });
}

function showPromptMessage() {
  swal(
    {
      title: 'An input!',
      text: 'Write something interesting:',
      type: 'input',
      showCancelButton: true,
      closeOnConfirm: false,
      animation: 'slide-from-top',
      inputPlaceholder: 'Write something',
    },
    function (inputValue) {
      if (inputValue === false) return false;
      if (inputValue === '') {
        swal.showInputError('You need to write something!');
        return false;
      }
      swal('Nice!', 'You wrote: ' + inputValue, 'success');
    }
  );
}

function showAjaxLoaderMessage() {
  swal(
    {
      title: 'Ajax request example',
      text: 'Submit to run ajax request',
      type: 'info',
      showCancelButton: true,
      closeOnConfirm: false,
      showLoaderOnConfirm: true,
    },
    function () {
      setTimeout(function () {
        swal('Ajax request finished!');
      }, 2000);
    }
  );
}
