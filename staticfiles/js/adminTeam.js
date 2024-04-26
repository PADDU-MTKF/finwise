document.querySelectorAll('.box').forEach(function(box) {
    box.addEventListener('click', function() {

         // Get data from hidden input fields
        var boxId=box.id;
        var name = document.getElementById('nameHidden_'+boxId).value;
        var userName = document.getElementById('userNameHidden_'+boxId).value;
        var jobTitle = document.getElementById('jobTitleHidden_'+boxId).value;
        var phoneNumber = document.getElementById('phoneNumberHidden_'+boxId).value;
        var isPercent = document.getElementById('isPercentHidden_'+boxId).value;
        var pay = document.getElementById('payHidden_'+boxId).value;
        var Id = document.getElementById('IDHidden_'+boxId).value;

        // Populate form fields in the popup with the retrieved data
        document.getElementById('name').value = name;
        document.getElementById('userName').value = userName;
        document.getElementById('jobTitle').value = jobTitle;
        document.getElementById('phoneNumber').value = phoneNumber;
        document.getElementById('isPercent').checked = isPercent === 'True'; // Convert string to boolean
        document.getElementById('pay').value = pay;
        document.getElementById('ID').value = Id;

        document.getElementById('popup').style.display = 'block';
        document.getElementById('saveButton').classList.add('hide');
        document.getElementById('saveButton').name="edit";
        document.getElementById('saveButton').textContent="Save";
        document.querySelector('#popup [name="delete"]').classList.remove('hide');
        togglePayLabelAndValidation();


    });
  });

  document.querySelector('#editCancelButton').addEventListener('click', function(event) {
    event.preventDefault();
    var editCancelButton = document.getElementById('editCancelButton');
    var editMode = editCancelButton.textContent === 'Edit';
    var inputs = document.querySelectorAll('#popup input, #popup textarea');
    
    inputs.forEach(function(input) {
      input.disabled = !editMode;
    });
    
    editCancelButton.textContent = editMode ? 'Cancel' : 'Edit';

    if (!editMode) {
        
        document.getElementById('popup').style.display = 'none';
    }
    
    document.getElementById('saveButton').classList.remove('hide');


  });


  function confirmDelete() {
    // Prompt the user for confirmation
    var result = confirm("Are you sure you want to delete?");

    // If user confirms, proceed with form submission
    if (result) {
      return true;
    } else {
      // If user cancels, prevent the form submission
      return false;
    }
  }

  function checkPassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (password != confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}

function togglePayLabelAndValidation() {
  var isPercentCheckbox = document.getElementById("isPercent");
  var payLabel = document.getElementById("payLabel");
  var payInput = document.getElementById("pay");

  if (isPercentCheckbox.checked) {
      payLabel.innerText = "Pay in Percentage:";
      payInput.placeholder = "Enter percentage (0.1 - 100)";
      payInput.removeAttribute("max");
      payInput.removeAttribute("step");
      payInput.setAttribute("min", "0.1");
      payInput.setAttribute("max", "100");
      payInput.setAttribute("step", "0.1");
  } else {
      payLabel.innerText = "Pay in Amount:";
      payInput.placeholder = "Enter amount";
      payInput.removeAttribute("min");
      payInput.removeAttribute("max");
      payInput.removeAttribute("step");
  }
}


  document.getElementById('add_float').addEventListener('click', function() {
    var saveButton = document.getElementById('saveButton');
    var deleteButton = document.querySelector('#popup [name="delete"]');
  
    // visibility of the popup
    document.getElementById('popup').style.display = 'block';
    document.getElementById('saveButton').classList.remove('hide');
    deleteButton.classList.add('hide');
    document.getElementById('editCancelButton').textContent ='Cancel'

    var inputs = document.querySelectorAll('#popup input, #popup textarea');
    
    inputs.forEach(function(input) {
      input.disabled = false;
    });


    document.getElementById('name').value = "";
        document.getElementById('userName').value = "";
        document.getElementById('jobTitle').value = "";
        document.getElementById('phoneNumber').value = "";
        document.getElementById('isPercent').checked = false; // Convert string to boolean
        document.getElementById('pay').value = "";
        document.getElementById('ID').value = "";


  
    // Change the text of the save button to "Add" or "Save" based on current visibility
    saveButton.name="add";
    saveButton.textContent = (popup.style.display === 'none') ? 'Save' : 'Add';
    togglePayLabelAndValidation();
  
   
  });















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