document.addEventListener('DOMContentLoaded', function () {
    const resourceTypeField = document.querySelector('#id_resource_type');
    const roomField = document.querySelector('.field-room');
    const vehicleField = document.querySelector('.field-vehicle');

    function toggleFields() {
        const selectedType = resourceTypeField.value;

        if (selectedType === 'Room') {
            roomField.style.display = '';
            vehicleField.style.display = 'none';
        } else if (selectedType === 'Vehicle') {
            roomField.style.display = 'none';
            vehicleField.style.display = '';
        } else {
            roomField.style.display = 'none';
            vehicleField.style.display = 'none';
        }
    }

    toggleFields();

    if (resourceTypeField) {
        resourceTypeField.addEventListener('change', toggleFields);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const departementSelect = document.getElementById('departement');
    if (departementSelect) {
        departementSelect.addEventListener('change', () => {
            console.log('Selected Departement:', departementSelect.value);
        });
    }
});
