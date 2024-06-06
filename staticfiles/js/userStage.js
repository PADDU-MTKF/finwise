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
    var toolssDiv = document.querySelectorAll('.toolss');
    toolssDiv.forEach((e) => {

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
        let cardId="";
        const entry = { date, title, description ,cardId };
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




let stageEdit = false;
let initialValues = {};

function addTimelineCard(entry) {
    const nostage = document.getElementById('nostage');
    nostage.classList.add("hide");
    
    const timeline = document.getElementById('timeline');
    const card = document.createElement('div');
    card.classList.add("card");
    card.id = entry.cardId;

    const circle = document.createElement('div');
    circle.classList.add("circle");
    card.className = 'timeline-card';

    card.innerHTML = `
        <input type="text" value="${entry.date}" class="transparent stage-text-color stageInp" style="font-size: 1.17em; font-weight: bold;" readonly>
        <input type="text" value="${entry.title}" class="transparent stage-text-color stageInp" style="font-size: 1.00em; font-weight: bold;" readonly>
        <textarea class="transparent stage-text-color stagedes stageInp" style="font-size: 1.00em; resize: none;" readonly>${entry.description}</textarea>
        <button class="hide deleteBtn" onclick="deleteCard('${entry.cardId}')">Delete</button>
    `;

    card.append(circle);
    timeline.appendChild(card);

    if (currentStage == 0) {
        trackerLine(0);
    }
}

function toggleButtonsExcept(callerButtonId, disable = true) {
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function (button) {
        if (button.id !== callerButtonId && !button.classList.contains('nav-link') && !button.classList.contains('deleteBtn')) {
            button.disabled = disable;
            if (disable) {
                button.classList.add('buttons-disabled');
            } else {
                button.classList.remove('buttons-disabled');
            }
        }
    });
}

function getCardValues() {
    let values = {};
    document.querySelectorAll('.timeline-card').forEach(card => {
        let cardId = card.id;
        values[cardId] = {
            date: card.querySelector('input[type="text"]:nth-child(1)').value,
            title: card.querySelector('input[type="text"]:nth-child(2)').value,
            description: card.querySelector('textarea').value
        };
    });
    return values;
}

function deleteCard(cardId) {
    const card = document.getElementById(cardId);
    const deleteBtn = card.querySelector('.deleteBtn');
    deleteBtn.disabled = true; // Disable the delete button
    deleteBtn.classList.add("buttons-disabled") 

    showLoadingSpinner()

    const csrftoken = getCSRFToken();
    const formData = {
        projectId: proid,
        docId: cardId
    };

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/deleteStage', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            deleteBtn.disabled = false; // Enable the delete button
            deleteBtn.classList.remove("buttons-disabled") 


            if (xhr.status === 200) {
                card.remove();
                alert('Card deleted successfully.');
                hideLoadingSpinner()

            } else {
                alert('Failed to delete card.');
                hideLoadingSpinner()

            }
        }
    };

    xhr.send(JSON.stringify(formData));
}


document.getElementById('stageEdit').addEventListener('click', function () {
    var stageInp = document.querySelectorAll('.stageInp');
    var deleteBtns = document.querySelectorAll('.deleteBtn');

    if (!stageEdit) {
        initialValues = getCardValues();

        stageInp.forEach(function (element) {
            element.removeAttribute('readonly');
            element.classList.remove('transparent');
            element.classList.remove('stage-text-color');
        });

        deleteBtns.forEach(function (button) {
            button.classList.remove('hide');
        });

        toggleButtonsExcept('stageEdit', true);
        trackerLine(currentStage);
    } else {
        let newValues = getCardValues();

        stageInp.forEach(function (element) {
            element.setAttribute('readonly', 'readonly');
            element.classList.add('transparent');
            element.classList.add('stage-text-color');
        });
        deleteBtns.forEach(function (button) {
            button.classList.add('hide');
        });

        toggleButtonsExcept('stageEdit', false);
        trackerLine(currentStage);

        let changedValues = {};
        for (let id in initialValues) {
            // Check if the element exists before processing its data
            let newElement = document.getElementById(id);
            if (newElement) {
                if (JSON.stringify(initialValues[id]) !== JSON.stringify(newValues[id])) {
                    changedValues[id] = newValues[id];
                }
            }
        }

        if (Object.keys(changedValues).length > 0) {

        console.log('Changed values:', changedValues);

        // Prepare data to send
        const csrftoken = getCSRFToken();
        const formData = {
            projectId: proid,
            changedValues: changedValues // Include changed values
        };
        showLoadingSpinner()

        // Send data via AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/updateStageDetails', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request header
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    alert('Data sent successfully...');
                    hideLoadingSpinner()
                } else {
                    alert('Failed to send data.');
                    hideLoadingSpinner()

                }
            }
        };
        xhr.send(JSON.stringify(formData));
        }
    }

    stageEdit = !stageEdit;
});






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


document.addEventListener('DOMContentLoaded', function () {
    var textareas = document.querySelectorAll('.stagedes');
    textareas.forEach(function (textarea) {
        adjustHeight(textarea);
        textarea.addEventListener('input', function () {
            adjustHeight(textarea);
        });
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






//info box enabling fields
let infoOpen=false;

document.getElementById('toggleHover').addEventListener('click', function() {
    console.log("yes");
    document.getElementById('infobox').classList.toggle('hover');
     var prodetailElements = document.querySelectorAll('.prodestext');
  
    // Iterate over each element and remove the 'readonly' attribute
    if(!infoOpen){
            prodetailElements.forEach(function(element) {
                element.removeAttribute('readonly');
                element.classList.remove('transparent');
            });
        }
    else{
            let data={};
            data["projectId"]=proid;
            data["creator"]=localStorage.getItem("username");
            prodetailElements.forEach(function(element) {
                element.setAttribute('readonly','readonly');
                element.classList.add('transparent');

                var name = element.getAttribute('name');
                var value = element.value;
                data[name]=value;

            });

            
        const csrftoken = getCSRFToken();

        console.log("Aaaya");


        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/updateProDet', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Include the CSRF token in the request header
        xhr.onreadystatechange = function () {
            // if (xhr.readyState === 4 && xhr.status === 200) {
            //     alert('data sent successfully... ');
            // }
        };
        xhr.send(JSON.stringify(data));
            console.log(data);
    }
    infoOpen=!infoOpen;
  });