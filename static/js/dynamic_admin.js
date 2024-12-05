document.addEventListener('DOMContentLoaded', function () {
    const requiredFields = [
        { id: 'id_departement', labelFor: 'Departement' },
        { id: 'id_destination_address', labelFor: 'Destination address' },
        { id: 'id_room', labelFor: 'Room' },
        { id: 'id_vehicle', labelFor: 'Vehicle' },
    ];

    requiredFields.forEach((field) => {
        const element = document.querySelector(`#${field.id}`);
        if (element) {
            const label = document.querySelector(`label[for="${field.id}"]`);
            if (label && !label.innerHTML.includes('*')) {
                label.innerHTML += ' <span style="color: red;">*</span>';
            }
        }
    });
});
