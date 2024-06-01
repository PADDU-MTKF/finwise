function toggleTools() {
    var toolsDiv = document.querySelectorAll('.tools');
    toolsDiv.forEach((e) => {

        if (e.classList.contains('show')) {
            e.classList.remove('show');
            setTimeout(() => {
                e.style.display = 'none';
            }, 500); // match the transition duration
        } else {
            e.style.display = 'block';
            setTimeout(() => {
                e.classList.add('show');
            }, 10); // slight delay to trigger the animation
        }
    })
    var toolDiv = document.querySelectorAll('.tool');
    toolDiv.forEach((e) => {

        if (e.classList.contains('show')) {
            e.classList.remove('show');
            setTimeout(() => {
                e.style.display = 'none';
            }, 500); // match the transition duration
        } else {
            e.style.display = 'block';
            setTimeout(() => {
                e.classList.add('show');
            }, 10); // slight delay to trigger the animation
        }
    })
}


 // Function to get CSRF token from meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


// New script for timeline navigation

function updateCurrentStage(index) {

     // background data transfer using ajax

     const csrftoken = getCSRFToken();

     const formData = {
        docId:stageDocId,
         projectId: proid,
         currentStage: index,
     };

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/saveCurrentStage', true);
     xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
     xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request header
     xhr.onreadystatechange = function () {
         // if (xhr.readyState === 4 && xhr.status === 200) {
         //     alert('data sent successfully... ');
         // }
     };
     xhr.send(JSON.stringify(formData));


    
}

document.getElementById('next-button').addEventListener('click', () => {
    if (currentStage < document.querySelectorAll('.timeline-card').length - 1) {
    const userConfirmed = confirm('Are you sure you want to proceed to the next stage?');
    
    if (userConfirmed) {
        currentStage++;
        setTimeout(() => {
                trackerLine(currentStage);
            }, 400);
        updateCurrentStage(currentStage)
   
       
    } 
}
});

document.getElementById('prev-button').addEventListener('click', () => {
    if (currentStage > 0) {
    const userConfirmed = confirm('Are you sure you want to Move Back to the Previous stage?');
    
    if (userConfirmed) {
        currentStage--;
        setTimeout(() => {
                trackerLine(currentStage);
            }, 400);
        updateCurrentStage(currentStage)

    }
    
}
});


function openForm() {
    const formPopup = document.getElementById('formPopup');
    const overlay = document.getElementById('overlay');
    formPopup.style.display = 'block';
    overlay.style.display = 'block';
    formPopup.style.animation = 'zoomIn 0.3s forwards'; // Apply zoom-in animation
}

function closeForm() {
    const formPopup = document.getElementById('formPopup');
    const overlay = document.getElementById('overlay');
    formPopup.style.animation = 'zoomOut 0.3s forwards'; // Apply zoom-out animation
    setTimeout(() => {
        formPopup.style.display = 'none';
        overlay.style.display = 'none';
    }, 300); // Delay hiding the form to allow animation to complete
}


// document.addEventListener('DOMContentLoaded', function () {
//     loadTimeline();
// });



document.getElementById('add-button').addEventListener('click', function () {
    const date = document.getElementById('date-input').value;
    const title = document.getElementById('title-input').value;
    const description = document.getElementById('description-input').value;

    if (date && title && description) {
        const entry = { date, title, description };
        // saveToLocalStorage(entry);
        addTimelineCard(entry);

        // Clear input fields after adding
        document.getElementById('date-input').value = '';
        document.getElementById('title-input').value = '';
        document.getElementById('description-input').value = '';
        closeForm()

        // background data transfer using ajax


       
        const csrftoken = getCSRFToken();


        console.log("Aaaya");

        // const formData = {
        //     projectId: proid,
        //     timeldatine: localStorage.getItem("timelineData")
        // };

        const formData = {
            projectId: proid,
            date: date,
            title: title,
            description: description,
        };

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/saveStage', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request header
        xhr.onreadystatechange = function () {
            // if (xhr.readyState === 4 && xhr.status === 200) {
            //     alert('data sent successfully... ');
            // }
        };
        xhr.send(JSON.stringify(formData));

    } else {
        alert('Please fill in all fields.');
    }
});

function saveToLocalStorage(entry) {
    let timelineData = JSON.parse(localStorage.getItem('timelineData')) || [];
    timelineData.push(entry);
    localStorage.setItem('timelineData', JSON.stringify(timelineData));
}

function loadTimeline() {
    let timelineData = JSON.parse(localStorage.getItem('timelineData')) || [];
    timelineData.forEach(entry => {
        addTimelineCard(entry);
    });
}

function addTimelineCard(entry) {
    // console.log("entry");

    const nostage = document.getElementById('nostage');
    nostage.classList.add("hide")
    
    const timeline = document.getElementById('timeline');
    const card = document.createElement('div');
    card.classList.add("card")
    const circle = document.createElement('div');
    circle.classList.add("circle");
    card.className = 'timeline-card';
    card.innerHTML = `<h3>${entry.date}</h3><h4>${entry.title}</h4><p>${entry.description}</p>`;
    card.append(circle);
    timeline.appendChild(card);

    if (currentStage==0){
        trackerLine(0)
    }

    
}


function trackerLine(index) {
    // Collapse any expanded cards
    // console.log(index);
    const expandedCards = document.querySelectorAll('.timeline-card.expanded');
    expandedCards.forEach(expCard => {
        expCard.classList.remove('expanded');
    });
    let i;
    if(index<document.querySelectorAll('.timeline-card').length){
        i=index;
    }
    else{
        i=0;
    }
    const card=document.querySelectorAll('.timeline-card')[i];
    const line = document.getElementById('timeline-line');
    
    // Expand the clicked card
    card.classList.toggle('expanded');

    // Update the timeline line height to the clicked card
    if (card.classList.contains('expanded')) {
        line.style.height = card.offsetTop + card.offsetHeight + 'px';
    } else {
        line.style.height = timeline.scrollHeight + 'px';
    }
}




// Function to adjust the height of the textarea
function adjustHeight(textarea) {
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = textarea.scrollHeight + 8 + 'px'; // Set new height based on scroll height
}

// Initialize the textarea height on page load and on input
document.addEventListener('DOMContentLoaded', function () {
    var textarea = document.getElementById('prodes');
    adjustHeight(textarea);
    textarea.addEventListener('input', function () {
        adjustHeight(textarea);
    });
});





// infobox div dropdown when hoverd

let infobox = document.querySelector(".infobox");
// let h1 = document.querySelector(".infobox h2");


// infobox.addEventListener("mouseover", () => {
//     h1.textContent = "Info box";
// })

infobox.addEventListener("mouseleave", () => {
    infobox.scrollTop = 0;
    // document.querySelector("hr").style.display="none";
})


// $(document).ready(function() {
//     // loadMessages();

//     $('#chatInput').keypress(function(event) {
//         if (event.which == 13) {
//             sendMessage();
//         }
//     });
// });
$(document).ready(function() {
    scrollToBottom();
});

function sendMessage() {
    const input = $('#chatInput');
    const message = input.val().trim();

    if (message) {
        appendMessage(message);

        input.val('');
        const messagesContainer = $('#chatboxMessages');
        messagesContainer.scrollTop(messagesContainer[0].scrollHeight);

        // background data transfer using ajax


        const csrftoken = getCSRFToken();

        console.log("Aaaya");

        const formData = {
            projectId: proid,
            msg: message
        };

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/saveMsg', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request header
        xhr.onreadystatechange = function () {
            // if (xhr.readyState === 4 && xhr.status === 200) {
            //     alert('data sent successfully... ');
            // }
        };
        xhr.send(JSON.stringify(formData));

    }
}

function appendMessage(message) {
    const messageBubble = $('<div class="message"></div>').text(message);
    const messagesContainer = $('#chatboxMessages');
    messagesContainer.append(messageBubble);
}

function scrollToBottom() {
    const messagesContainer = $('#chatboxMessages');
    setTimeout(() => {
        messagesContainer.scrollTop(messagesContainer[0].scrollHeight);
    }, 0);
}



function onloadlocal(){
// sara stage local mai dal do
}

onloadlocal()


//info box enabling fields

