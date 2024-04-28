document.querySelectorAll('.box').forEach(function(box) {
    box.addEventListener('click', function() {

         // Get data from hidden input fields
        var boxId=box.id;
        var name = document.getElementById('nameHidden_'+boxId).value;
        var userName = document.getElementById('userNameHidden_'+boxId).value;
        var password = document.getElementById('passwordHidden_'+boxId).value;
        var jobTitle = document.getElementById('jobTitleHidden_'+boxId).value;
        var phoneNumber = document.getElementById('phoneNumberHidden_'+boxId).value;
        var isPercent = document.getElementById('isPercentHidden_'+boxId).value;
        var pay = document.getElementById('payHidden_'+boxId).value;
        var Id = document.getElementById('IDHidden_'+boxId).value;

        // Populate form fields in the popup with the retrieved data
        document.getElementById('name').value = name;
        document.getElementById('userName').value = userName;
        document.getElementById('password').value = password;
        document.getElementById('confirmPassword').value = password;
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

      closeForm();
        
        // document.getElementById('popup').style.display = 'none';
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


    const formPopup = document.getElementById('popup');
    formPopup.style.display = 'block';
  
    // visibility of the popup
    formPopup.style.animation = 'zoomIn 0.3s forwards';
    document.getElementById('saveButton').classList.remove('hide');
    deleteButton.classList.add('hide');
    document.getElementById('editCancelButton').textContent ='Cancel'

    var inputs = document.querySelectorAll('#popup input, #popup textarea');
    
    inputs.forEach(function(input) {
      input.disabled = false;
    });

   

    document.getElementById('name').value = "";
        document.getElementById('userName').value = "";
        document.getElementById('password').value = "";
        document.getElementById('confirmPassword').value = "";
        
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




  function closeForm() {
    const formPopup = document.getElementById('popup');
    formPopup.style.animation = 'zoomOut 0.3s forwards'; // Apply zoom-out animation
    setTimeout(() => {
        formPopup.style.display = 'none';
    }, 300); // Delay hiding the form to allow animation to complete
}











