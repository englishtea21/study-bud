// Scroll to element
function scrollToElement(targetElement, scrollView) {
  const scrollViewRect = scrollView.getBoundingClientRect();
  const targetElementRect = targetElement.getBoundingClientRect();
  if (targetElementRect.top < scrollViewRect.top || targetElementRect.bottom > scrollViewRect.bottom) {
    // scrollview отображает контент относительно родительского контейнера,
    // поэтому нужно учесть положение scrollview относительно родителя и вычесть его из положения целевого элемента
    // scrollView.scrollTop = targetElement.offsetTop - scrollView.offsetTop;
    scrollView.scroll({
      top: targetElement.offsetTop - scrollView.offsetTop,
      behavior: "smooth"
    });
  }
}


// Cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// Highlight animation
function highlight(element, highlightClass, timeInterval = 1000) {
  element.classList.add(highlightClass);

  setTimeout(function () {
    element.classList.remove(highlightClass);
  }, timeInterval);
}


// Element activity state
function ActivityStateOn(element, attribute) {
  if (element.getAttribute(attribute) == 'true') {
    element.classList.remove('non-active');
    element.setAttribute('data-vote-active-status', 'false');
  }
}

function toggleActivityState(element, attribute) {
  if (element.getAttribute(attribute) == 'true') {
    element.classList.remove('non-active');
    element.setAttribute('data-vote-active-status', 'false');
  }
  else {
    element.classList.add('non-active');
    element.setAttribute('data-vote-active-status', 'true');
  }
}


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

// Rooms votes
const roomVotes = document.querySelectorAll('.roomListRoom__votes');

roomVotes.forEach(roomVote => {
  const roomUpvote = roomVote.querySelector('.upvote-arrow');
  const roomDownvote = roomVote.querySelector('.downvote-arrow');

  if (roomUpvote) {
    toggleActivityState(roomUpvote, 'data-vote-active-status')
    roomUpvote.addEventListener('click', () => voteClickProcessing(roomVote, 'upvote'));
  }
  if (roomDownvote) {
    toggleActivityState(roomDownvote, 'data-vote-active-status')
    roomDownvote.addEventListener('click', () => voteClickProcessing(roomVote, 'downvote'));
  }
})

async function voteClickProcessing(voteSection, voteType) {
  const roomId = voteSection.getAttribute('data-room-id');
  voteButton = voteSection.querySelector(`.${voteType}-arrow`);

  if (voteType == 'upvote')
    anotherButtonType = 'downvote';
  else
    anotherButtonType = 'upvote';

  // Saving votes
  let xhrVoting = new XMLHttpRequest();
  xhrVoting.onload = function () {
    if (this.status === 200) {
      ActivityStateOn(voteSection.querySelector(`.${anotherButtonType}-arrow`), 'data-vote-active-status');
      toggleActivityState(voteButton, 'data-vote-active-status');

      // Recounting votes
      let xhrVotescounting = new XMLHttpRequest();
      xhrVotescounting.onload = function () {
        if (this.status === 200) {
          voteSection.querySelector('.votes-count').innerHTML = JSON.parse(this.response).votes_count;
        }
      }
      xhrVotescounting.open('GET', `api/rooms/${roomId}/votes_count/`);
      xhrVotescounting.send();
    }
  }
  xhrVoting.open('GET', `api/rooms/${roomId}/${voteType}_room/`);
  xhrVoting.send();
}


// infinite pagination
const fetchPage = async (url) => {
  return fetch(url,
    {
      method: 'GET',
      credentials: 'same-origin',
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        // "X-CSRFToken": getCookie("csrftoken"),
        // "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        'Content-Type': 'text/html',
      },
    }
    // headers
  )
}

document.addEventListener("DOMContentLoaded", () => {
  let sentinel = document.getElementById("sentinel");
  // let previousSentinel = document.getElementsByClassName('previous-sentinel');
  let scrollElement = document.getElementById("feed-infinite-container");
  let counter = 2;
  let end = false;

  let sentinelObserver = new IntersectionObserver(async (entries) => {
    entry = entries[0];
    if (entry.intersectionRatio > 0 && !end) {
      let url = `/?page=${counter}`;
      let req = await fetchPage(url);
      if (req.ok) {
        let body = await req.text();
        // Be careful of XSS if you do this. Make sure
        // you remove all possible sources of XSS.
        // console.log(body)
        counter++;
        scrollElement.innerHTML += body;
      } else {
        // If it returns a 404, stop requesting new items
        end = true;
      }
    }
  })
  sentinelObserver.observe(sentinel);

  // let previousSentinelObserver = new IntersectionObserver(async(entries)=>{
  //   entry = entries[0];

  // })
})