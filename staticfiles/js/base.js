const MIN_SPEED = 1.5;
const MAX_SPEED = 2.5;

function randomNumber(min, max) {
  return Math.random() * (max - min) + min;
}

class Blob {
  constructor(el) {
    this.el = el;
    const boundingRect = this.el.getBoundingClientRect();
    this.size = boundingRect.width;
    this.initialX = randomNumber(0, window.innerWidth - this.size);
    this.initialY = randomNumber(0, window.innerHeight - this.size);
    this.el.style.top = `${this.initialY}px`;
    this.el.style.left = `${this.initialX}px`;
    this.vx = randomNumber(MIN_SPEED, MAX_SPEED) * (Math.random() > 0.5 ? 1 : -1);
    this.vy = randomNumber(MIN_SPEED, MAX_SPEED) * (Math.random() > 0.5 ? 1 : -1);
    this.x = this.initialX;
    this.y = this.initialY;
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x >= window.innerWidth - this.size) {
      this.x = window.innerWidth - this.size;
      this.vx *= -1;
    }
    if (this.y >= window.innerHeight - this.size) {
      this.y = window.innerHeight - this.size;
      this.vy *= -1;
    }
    if (this.x <= 0) {
      this.x = 0;
      this.vx *= -1;
    }
    if (this.y <= 0) {
      this.y = 0;
      this.vy *= -1;
    }
  }

  move() {
    this.el.style.transform = `translate(${this.x}px, ${this.y}px)`;
  }
}

function initBlobs() {
  const blobEls = document.querySelectorAll('.bouncing-blob');
  const blobs = Array.from(blobEls).map((blobEl) => new Blob(blobEl));

  function update() {
    requestAnimationFrame(update);
    blobs.forEach((blob) => {
      blob.update();
      blob.move();
    });
  }

  requestAnimationFrame(update);
}

initBlobs();




function confirmLogOut() {
    // Prompt the user for confirmation
    var result = confirm("Are you sure you want to Log Out?");

    // If user confirms, proceed with form submission
    if (result) {
      navigateToUrl("logout");
    } else {
      // If user cancels, prevent the form submission
      return false;
    }
  }


  function navigateToUrl(url) {
    window.location.href = url;
}

const search = document.querySelector('.input-group input'),
table_rows = document.querySelectorAll('tbody tr'),
table_headings = document.querySelectorAll('thead th');

// 1. Searching for specific data of HTML table
search.addEventListener('input', searchTable);

function searchTable() {
  table_rows.forEach((row, i) => {
      let table_data = row.textContent.toLowerCase(),
          search_data = search.value.toLowerCase();

      row.classList.toggle('hide', table_data.indexOf(search_data) < 0);
      row.style.setProperty('--delay', i / 25 + 's');
  })

  document.querySelectorAll('tbody tr:not(.hide)').forEach((visible_row, i) => {
      visible_row.style.backgroundColor = (i % 2 == 0) ? 'transparent' : '#0000000b';
  });
}

// 2. Sorting | Ordering data of HTML table

table_headings.forEach((head, i) => {
  let sort_asc = true;
  head.onclick = () => {
      table_headings.forEach(head => head.classList.remove('active'));
      head.classList.add('active');

      document.querySelectorAll('td').forEach(td => td.classList.remove('active'));
      table_rows.forEach(row => {
          row.querySelectorAll('td')[i].classList.add('active');
      })

      head.classList.toggle('asc', sort_asc);
      sort_asc = head.classList.contains('asc') ? false : true;

      sortTable(i, sort_asc);
  }
})


function sortTable(column, sort_asc) {
  [...table_rows].sort((a, b) => {
      let first_row = a.querySelectorAll('td')[column].textContent.toLowerCase(),
          second_row = b.querySelectorAll('td')[column].textContent.toLowerCase();

      return sort_asc ? (first_row < second_row ? 1 : -1) : (first_row < second_row ? -1 : 1);
  })
      .map(sorted_row => document.querySelector('tbody').appendChild(sorted_row));
}