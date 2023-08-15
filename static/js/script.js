// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }


// Scroll to element
function scrollToElement(targetElement, scrollView) {
  const scrollViewRect = scrollView.getBoundingClientRect();
  const targetElementRect = targetElement.getBoundingClientRect();
  if (targetElementRect.top < scrollViewRect.top || targetElementRect.bottom > scrollViewRect.bottom) {
    // scrollview отображает контент относительно родительского контейнера,
    // поэтому нужно учесть положение scrollview относительно родителя и вычесть его из положения целевого элемента
    scrollView.scrollTop = targetElement.offsetTop - scrollView.offsetTop;
  }
}

// Highlight animation
function highlight(element, highlightClass, timeInterval = 1000) {
  element.classList.add(highlightClass);

  setTimeout(function () {
    element.classList.remove(highlightClass);
  }, timeInterval);
}

// Clear form
// function clearForm(myFormElement) {

//   var elements = myFormElement.elements;

//   // myFormElement.reset();

//   for (i = 0; i < elements.length; i++) {

//     field_type = elements[i].type.toLowerCase();

//     switch (field_type) {

//       case "text":
//       case "password":
//       case "textarea":
//       case "hidden":

//         elements[i].value = "";
//         break;

//       case "radio":
//       case "checkbox":
//         if (elements[i].checked) {
//           elements[i].checked = false;
//         }
//         break;

//       case "select-one":
//       case "select-multi":
//         elements[i].selectedIndex = -1;
//         break;

//       default:
//         break;
//     }
//   }
// }


// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to bottom
const conversationThread = document.querySelector(".threads");
if (conversationThread) conversationThread.scrollBottom = conversationThread.scrollHeight;

// Clear button
class ClearButton {
  #clearButton;
  constructor(tag = 'span', html_class = 'clear-button', innerHTML = '&#10006;', field, onClearButton, ...args) {
    // console.log(`tag=`);
    this.#clearButton = document.createElement(tag);
    this.#clearButton.className = html_class;
    this.#clearButton.innerHTML = innerHTML;

    field.parentNode.insertBefore(this.#clearButton, field.nextSibling);

    this.#clearButton.addEventListener('click', () => onClearButton.apply(this, args));
  }

  get clearButton() {
    return this.clearButton;
  }
}

const headerSearchField = document.querySelector('header > div > form.header__search > label input');
const headerSearchFieldClearButton = new ClearButton(undefined, undefined, undefined, headerSearchField, () => {
  headerSearchField.value = '';
})
// console.log(headerSearchField);

//Message reply
const messageForm = document.querySelector('.room__message form');

if (messageForm) {

  const messageContainer = document.querySelector('.room__conversation');
  const messageReplyIdField = messageForm.querySelector('#message_reply_id');
  const messageEditIdField = messageForm.querySelector('#message_edit_id');
  const messageField = messageForm.querySelector('#message_field');

  messageReplyIdField.style = 'display:none';
  messageEditIdField.style = 'display:none';

  function clearMessageForm(placeholder = "Write your message...") {
    messageField.value = "";
    messageReplyIdField.value = "";
    messageEditIdField.value = "";
    messageField.placeholder = placeholder;
  }

  allMessages = messageContainer.querySelectorAll('.thread');

  allMessages.forEach(function (message) {
    // Scroll messages to replying after click on replied to ...
    const linkToRepliedMessage = message.querySelector('.message_link__reply_to');

    if (linkToRepliedMessage)
      linkToRepliedMessage.addEventListener('click', function (event) {

        const repliedMessageId = linkToRepliedMessage.getAttribute('data-message-reply-to-id');
        const repliedMessage = messageContainer.querySelector(
          `[data-message-id="${repliedMessageId}"]`
        ).closest('.thread');

        scrollToElement(targetElement = repliedMessage, scrollView = conversationThread);

        highlight(repliedMessage, 'highlight');
      });

    const messageReplyButton = message.querySelector('.thread__reply');
    const messageEditButton = message.querySelector('.thread__edit');
    const messageId = message.getAttribute('data-message-id');

    if (messageReplyButton)
      messageReplyButton.addEventListener('click', function (event) {

        clearMessageForm(placeholder = "");

        highlight(message, 'highlight');

        messageReplyIdField.value = messageId;

        const messageUserInfo = message.querySelector('.thread__author');
        messageField.placeholder = `Write your message to ${messageUserInfo.querySelector('a span').innerText}, posted ${messageUserInfo.querySelector('.thread__date').innerText}`;
      });


    if (messageEditButton)
      messageEditButton.addEventListener('click', function (event) {
        // clearForm(messageForm);

        clearMessageForm(placeholder = "");

        highlight(message, 'highlight');

        messageEditIdField.value = messageId;

        messageField.value = message.querySelector('.thread__details').innerText;
      })
  })

  let messageFieldClearButton = new ClearButton(undefined, undefined, undefined, messageField, clearMessageForm, undefined);

  // let clearButton = document.createElement('span');
  // clearButton.className = 'clear-button';
  // clearButton.innerHTML = '&#10006;';

  // // Добавляем крестик внутри поля ввода
  // messageField.parentNode.insertBefore(clearButton, messageField.nextSibling);

  // // Добавляем обработчик события клика на крестик
  // clearButton.addEventListener('click', clearMessageForm);



  // Add event listener to the input field
  messageField.addEventListener('keydown', function (event) {
    if (event.keyCode === 13) { // 13 is the key code for the Enter button
      event.preventDefault(); // Prevent the default form submission
      // You can perform any additional actions or validation here
      // For example, you can access the form and submit it
      messageForm.submit();
      // messageField.focus();
    }
  });

}