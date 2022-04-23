document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send_email_button').addEventListener('click', () => send_email());

  // By default, load the inbox
  load_mailbox('inbox');

  //mailbox functions

  function send_email(){
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });
    load_mailbox('sent');
    alert('Your email has been sent.')

  }
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#sent_mailbox').innerHTML='';
  document.querySelector('#sent_mailbox').style.display='none';
  document.querySelector('#view_sent').innerHTML='';
  document.querySelector('#inbox_mailbox').innerHTML='';
  document.querySelector('#inbox_mailbox').style.display='none';
  document.querySelector('#view_inbox').innerHTML='';
  document.querySelector('#archive_mailbox').innerHTML='';
  document.querySelector('#archive_mailbox').style.display='none';
  document.querySelector('#view_archive').innerHTML='';
}

function rev_load_inb(){
  location.reload()
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 id='mailbox_name'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (document.querySelector('#mailbox_name').innerHTML === 'Inbox'){
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(email => {
      console.log(email)
      email.forEach(email => {
        const email_item = document.createElement('div');
        const sendr = document.createElement('h5');
        sendr.innerHTML= email.sender;
        const subj = document.createElement('h6');
        subj.innerHTML= email.subject;
        const timsp = document.createElement('p');
        const id = email.id
        timsp.innerHTML= email.timestamp;
        email_item.append(sendr);
        email_item.append(subj);
        email_item.append(timsp);
        email_item.style.border='1px solid black'
        email_item.style.margin='8px'
        email_item.style.padding='4px'
        if (email.read === true){
          email_item.style.background='#d6d6d6';
        }
        document.querySelector('#inbox_mailbox').append(email_item);
        email_item.addEventListener('click', function(){
          document.querySelector('#inbox_mailbox').style.display='none';
          document.querySelector('#view_inbox').style.display='block';
          document.querySelector('#view_inbox').innerHTML='';
          fetch('/emails/'+id)
          .then(response => response.json())
          .then(email => {
            const sendrv = document.createElement('h5').innerHTML=email.sender;
            const recpv = document.createElement('h5').innerHTML=email.recipients;
            const subjv = document.createElement('h6').innerHTML=email.subject;
            const bodyv = document.createElement('p').innerHTML=email.body;
            const timspv = document.createElement('p').innerHTML=email.timestamp;
            const nextline=document.createElement('br')
            const nextline1=document.createElement('br')
            const nextline2=document.createElement('br')
            const nextline3=document.createElement('br')
            const nextline4=document.createElement('br')
            const line=document.createElement('hr')
            const line2=document.createElement('br')
            document.querySelector('#view_inbox').append(`From: ${sendrv}`);
            document.querySelector('#view_inbox').append(nextline)
            document.querySelector('#view_inbox').append(`To: ${recpv}`);
            document.querySelector('#view_inbox').append(nextline1)
            document.querySelector('#view_inbox').append(`Subject: ${subjv}`);
            document.querySelector('#view_inbox').append(line)
            document.querySelector('#view_inbox').append(nextline2)
            document.querySelector('#view_inbox').append(bodyv);
            document.querySelector('#view_inbox').append(nextline3)
            document.querySelector('#view_inbox').append(line2);
            document.querySelector('#view_inbox').append(`Dated: ${timspv}`);
            document.querySelector('#view_inbox').append(nextline4)
            const reply_button = document.createElement('button');
            reply_button.textContent='Reply';
            reply_button.style.margin='6px;';
            reply_button.addEventListener('click', function(){
              document.querySelector('#view_inbox').style.display='none';
              compose_email()
              document.querySelector('#compose-recipients').value=email.sender;
              document.querySelector('#compose-subject').value=`Re: ${email.subject}`;
              const check_value=document.querySelector('#compose-recipients').value
              check = check_value.includes('Re:',1)
              if (check == true){
                document.querySelector('#compose-subject').value=email.subject;
              }
              document.querySelector('#compose-body').value=`On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
            });
              document.querySelector('#view_inbox').append(reply_button)
            if (email.archived === false){
              const archive_button = document.createElement('button');
              archive_button.textContent='Archive';
              archive_button.style.margin='6px;';
              archive_button.addEventListener('click', function(){
                  fetch('/emails/'+id, {
                    method: 'PUT',
                    body: JSON.stringify({
                      archived: true
                    })
                  });
                  rev_load_inb()
              });
              document.querySelector('#view_inbox').append(archive_button)
            }else{
            const unarchive_button = document.createElement('button')
            unarchive_button.textContent='Unarchive'
            unarchive_button.style.margin='6px;'
            unarchive_button.addEventListener('click', function(){
                fetch('/emails/'+id, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                });
                rev_load_inb()
            });
            document.querySelector('#view_inbox').append(unarchive_button)
          }
          });
          fetch('/emails/'+id, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });
        });
      });
    });
    document.querySelector('#sent_mailbox').style.display='none';
    document.querySelector('#sent_mailbox').innerHTML='';
    document.querySelector('#view_sent').innerHTML='';
    document.querySelector('#inbox_mailbox').innerHTML='';
    document.querySelector('#inbox_mailbox').style.display='block';
    document.querySelector('#view_inbox').innerHTML='';
    document.querySelector('#archive_mailbox').style.display='none';
    document.querySelector('#archive_mailbox').innerHTML='';
    document.querySelector('#view_archive').innerHTML='';
  }
  if (document.querySelector('#mailbox_name').innerHTML === 'Sent'){
    fetch('/emails/sent')
    .then(response => response.json())
    .then(email => {
      console.log(email)
      document.querySelector('#sent_mailbox').append('If an email you just immediately sent does not appear here, kindly reload this sent mailbox by clicking on Sent.')
      email.forEach(email => {
        const email_item = document.createElement('div');
        const recp = document.createElement('h5');
        recp.innerHTML= email.recipients;
        const subj = document.createElement('h6');
        subj.innerHTML= email.subject;
        const timsp = document.createElement('p');
        const id = email.id
        timsp.innerHTML= email.timestamp;
        email_item.append(recp);
        email_item.append(subj);
        email_item.append(timsp);
        email_item.style.border='1px solid black'
        email_item.style.margin='8px'
        email_item.style.padding='4px'
        if (email.read === true){
          email_item.style.background='#d6d6d6';
        }
        document.querySelector('#sent_mailbox').append(email_item);
        email_item.addEventListener('click', function(){
          document.querySelector('#sent_mailbox').style.display='none';
          document.querySelector('#view_sent').style.display='block';
          document.querySelector('#view_sent').innerHTML='';
          fetch('/emails/'+id)
          .then(response => response.json())
          .then(email => {
            const sendrv = document.createElement('h5').innerHTML=email.sender;
            const recpv = document.createElement('h5').innerHTML=email.recipients;
            const subjv = document.createElement('h6').innerHTML=email.subject;
            const bodyv = document.createElement('p').innerHTML=email.body;
            const timspv = document.createElement('p').innerHTML=email.timestamp;
            const nextline=document.createElement('br')
            const nextline1=document.createElement('br')
            const nextline2=document.createElement('br')
            const nextline3=document.createElement('br')
            const nextline4=document.createElement('br')
            const line=document.createElement('hr')
            const line2=document.createElement('br')
            document.querySelector('#view_sent').append(`From: ${sendrv}`);
            document.querySelector('#view_sent').append(nextline)
            document.querySelector('#view_sent').append(`To: ${recpv}`);
            document.querySelector('#view_sent').append(nextline1)
            document.querySelector('#view_sent').append(`Subject: ${subjv}`);
            document.querySelector('#view_sent').append(line)
            document.querySelector('#view_sent').append(nextline2)
            document.querySelector('#view_sent').append(bodyv);
            document.querySelector('#view_sent').append(nextline3)
            document.querySelector('#view_sent').append(line2);
            document.querySelector('#view_sent').append(`Dated: ${timspv}`);
            document.querySelector('#view_sent').append(nextline4)
          });
          fetch('/emails/'+id, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });
        });
        email_item.onclick='view_sent_email'
      });
    });
    document.querySelector('#sent_mailbox').innerHTML='';
    document.querySelector('#sent_mailbox').style.display='block';
    document.querySelector('#view_sent').innerHTML='';
    document.querySelector('#inbox_mailbox').innerHTML='';
    document.querySelector('#inbox_mailbox').style.display='none';
    document.querySelector('#view_inbox').innerHTML='';
    document.querySelector('#archive_mailbox').style.display='none';
    document.querySelector('#archive_mailbox').innerHTML='';
    document.querySelector('#view_archive').innerHTML='';
  }
  if (document.querySelector('#mailbox_name').innerHTML === 'Archive'){
    fetch('/emails/archive')
    .then(response => response.json())
    .then(email => {
      console.log(email)
      email.forEach(email => {
        const email_item = document.createElement('div');
        const sendr = document.createElement('h5');
        sendr.innerHTML= email.sender;
        const subj = document.createElement('h6');
        subj.innerHTML= email.subject;
        const timsp = document.createElement('p');
        const id = email.id
        timsp.innerHTML= email.timestamp;
        email_item.append(sendr);
        email_item.append(subj);
        email_item.append(timsp);
        email_item.style.border='1px solid black'
        email_item.style.margin='8px'
        email_item.style.padding='4px'
        if (email.read === true){
          email_item.style.background='#d6d6d6';
        }
        document.querySelector('#archive_mailbox').append(email_item);
        email_item.addEventListener('click', function(){
          document.querySelector('#archive_mailbox').style.display='none';
          document.querySelector('#view_archive').style.display='block';
          document.querySelector('#view_archive').innerHTML='';
          fetch('/emails/'+id)
          .then(response => response.json())
          .then(email => {
            const sendrv = document.createElement('h5').innerHTML=email.sender;
            const recpv = document.createElement('h5').innerHTML=email.recipients;
            const subjv = document.createElement('h6').innerHTML=email.subject;
            const bodyv = document.createElement('p').innerHTML=email.body;
            const timspv = document.createElement('p').innerHTML=email.timestamp;
            const nextline=document.createElement('br')
            const nextline1=document.createElement('br')
            const nextline2=document.createElement('br')
            const nextline3=document.createElement('br')
            const nextline4=document.createElement('br')
            const line=document.createElement('hr')
            const line2=document.createElement('br')
            document.querySelector('#view_archive').append(`From: ${sendrv}`);
            document.querySelector('#view_archive').append(nextline)
            document.querySelector('#view_archive').append(`To: ${recpv}`);
            document.querySelector('#view_archive').append(nextline1)
            document.querySelector('#view_archive').append(`Subject: ${subjv}`);
            document.querySelector('#view_archive').append(line)
            document.querySelector('#view_archive').append(nextline2)
            document.querySelector('#view_archive').append(bodyv);
            document.querySelector('#view_archive').append(nextline3)
            document.querySelector('#view_archive').append(line2);
            document.querySelector('#view_archive').append(`Dated: ${timspv}`);
            document.querySelector('#view_archive').append(nextline4)
            if (email.archived === false){
              const archive_button = document.createElement('button');
              archive_button.textContent='Archive';
              archive_button.style.margin='6px;';
              archive_button.addEventListener('click', function(){
                  fetch('/emails/'+id, {
                    method: 'PUT',
                    body: JSON.stringify({
                      archived: true
                    })
                  });
                  rev_load_inb()
              });
              document.querySelector('#view_archive').append(archive_button)
            }else{
            const unarchive_button = document.createElement('button')
            unarchive_button.textContent='Unarchive'
            unarchive_button.style.margin='6px;'
            unarchive_button.addEventListener('click', function(){
                fetch('/emails/'+id, {
                  method: 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                });
                rev_load_inb()
            });
            document.querySelector('#view_archive').append(unarchive_button)
          }
          });
          fetch('/emails/'+id, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });
        });
      });
    });
    document.querySelector('#sent_mailbox').innerHTML='';
    document.querySelector('#sent_mailbox').style.display='none';
    document.querySelector('#view_sent').innerHTML='';
    document.querySelector('#inbox_mailbox').innerHTML='';
    document.querySelector('#inbox_mailbox').style.display='none';
    document.querySelector('#view_inbox').innerHTML='';
    document.querySelector('#archive_mailbox').innerHTML='';
    document.querySelector('#archive_mailbox').style.display='block';
    document.querySelector('#view_archive').innerHTML='';
  }
}
  //load_mailbox_content
