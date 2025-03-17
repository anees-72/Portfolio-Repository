document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archived'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-opened').style.display = 'none';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = send_email;
}
 //function to load mailbox by name of the mailbox
function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-opened').style.display = 'none';


  document.querySelector('#email-opened').innerHTML = '';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  //fetches mailbox using api calls to the server
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      document.querySelector('#emails-view').innerHTML += emails.map(email => `
        <div class="email-item" style="background-color: ${email.read ? 'gray' : 'white'};" data-id="${email.id}">
          <span class="email-sender">${email.sender}</span>
          <span class="email-subject">${email.subject}</span>
          <span class="email-timestamp">${email.timestamp}</span>
        </div>
      `).join('');


      document.querySelectorAll('.email-item').forEach(mail => {
        mail.addEventListener('click', function () {
          view_email(mail.dataset.id);
        });
      });
    })
    .catch(error => console.error('Error loading emails:', error));
}

function view_email(email_id) {
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-opened').style.display = 'block';
      //fetch current user to check whether the sender is the user and to check whether this is sent mailbox
      fetch("current_user")
        .then(response => response.json())
        .then(data => {
          console.log("Current User:", data.username);
          console.log("Email Sender:", email.sender);
          //this button would be used to dispaly the buttons such as archive,unarchive and reply
          let buttonHTML = "";
          if (data.username !== email.sender) {
            buttonHTML = `
              <button class="btn btn-primary" id="archiveButton">
                ${email.archived ? "Unarchive" : "Archive"}
              </button>
              <button class="btn btn-secondary ml-2" id="replyButton">
                Reply
              </button>
            `;
          }

          document.querySelector('#email-opened').innerHTML = `
            <p><strong>From:</strong> ${email.sender}</p>
            <p><strong>Recipients:</strong> ${email.recipients.join(", ")}</p>
            <p><strong>Time:</strong> ${email.timestamp}</p>
            <p><strong>Subject:</strong> ${email.subject}</p>
            <hr>
            <p>${email.body}</p>
            <hr>
            ${buttonHTML}
          `;
          
          setTimeout(() => {
            if (document.querySelector("#archiveButton")) {
              document.querySelector("#archiveButton").addEventListener("click", function () {
                fetch(`/emails/${email_id}`, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ archived: !email.archived })
                })
                  .then(() => load_mailbox('inbox'))
                  .catch(error => console.error("Error updating archive status:", error));
              });
            }

            if (document.querySelector("#replyButton")) {
              document.querySelector("#replyButton").addEventListener("click", function () {
                document.querySelector('#emails-view').style.display = 'none';
                document.querySelector('#compose-view').style.display = 'block';
                document.querySelector('#email-opened').style.display = 'none';

                document.querySelector('#compose-recipients').value = email.sender;
                document.querySelector('#compose-subject').value = email.subject.startsWith("Re:") ? email.subject : `Re: ${email.subject}`;
                document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;

                document.querySelector('#compose-form').onsubmit = send_email;
              });
            }
          }, 100);
        })
        .catch(error => console.error("Error fetching current user:", error));
    })
    .catch(error => console.error("Error loading email:", error));


  fetch(`/emails/${email_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ read: true })
  });
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipients, subject, body }),
  })
    .then(response => response.json())
    .then(result => {
      load_mailbox('sent');
    });
}
