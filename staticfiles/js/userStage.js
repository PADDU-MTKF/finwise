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


// New script for timeline navigation
let currentCardIndex = 0;

function focusOnCard(index) {
    const timelineCards = document.querySelectorAll('.timeline-card');
    if (timelineCards[index]) {
        timelineCards[index].scrollIntoView({ behavior: 'smooth' });
    }
}

document.getElementById('next-button').addEventListener('click', () => {
    const timelineCards = document.querySelectorAll('.timeline-card');
    if (currentCardIndex < timelineCards.length - 1) {
        currentCardIndex++;
        focusOnCard(currentCardIndex);
    }
});

document.getElementById('prev-button').addEventListener('click', () => {
    if (currentCardIndex > 0) {
        currentCardIndex--;
        focusOnCard(currentCardIndex);
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


document.addEventListener('DOMContentLoaded', function () {
    loadTimeline();
});

document.getElementById('add-button').addEventListener('click', function () {
    const date = document.getElementById('date-input').value;
    const title = document.getElementById('title-input').value;
    const description = document.getElementById('description-input').value;

    if (date && title && description) {
        const entry = { date, title, description };
        saveToLocalStorage(entry);
        addTimelineCard(entry);

        // Clear input fields after adding
        document.getElementById('date-input').value = '';
        document.getElementById('title-input').value = '';
        document.getElementById('description-input').value = '';
        closeForm()
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
    const timeline = document.getElementById('timeline');
    const card = document.createElement('div');
    card.classList.add("card")
    const circle = document.createElement('div');
    circle.classList.add("circle");
    card.className = 'timeline-card';
    card.innerHTML = `<h3>${entry.date}</h3><h4>${entry.title}</h4><p>${entry.description}</p>`;
    card.append(circle);
    timeline.appendChild(card);

    // Update the timeline line height
    const line = document.getElementById('timeline-line');
    setTimeout(() => {
        line.style.height = timeline.scrollHeight + 'px';
    }, 10); // Delay to ensure DOM update

    // Add click event listener to toggle the expanded class
    card.addEventListener('click', function () {
        // Collapse any expanded cards
        const expandedCards = document.querySelectorAll('.timeline-card.expanded');
        expandedCards.forEach(expCard => {
            expCard.classList.remove('expanded');
        });

        // Expand the clicked card
        card.classList.toggle('expanded');

        // Update the timeline line height to the clicked card
        if (card.classList.contains('expanded')) {
            line.style.height = card.offsetTop + card.offsetHeight + 'px';
        } else {
            line.style.height = timeline.scrollHeight + 'px';
        }
    });
}







// infobox div dropdown when hoverd

let infobox = document.querySelector(".infobox");
let h1 = document.querySelector(".infobox h2");


infobox.addEventListener("mouseover", () => {
    h1.textContent = "Info box";
})

infobox.addEventListener("mouseout", () => {
    h1.textContent = "ⓘ";
})
