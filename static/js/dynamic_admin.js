document.addEventListener("DOMContentLoaded", function () {
    const requiredFields = [
        { id: "departement", label: "Departement" },
        { id: "id_room", label: "Room" },
        { id: "id_vehicle", label: "Vehicle" },
        { id: "id_destination_address", label: "Destination address" },
    ];

    requiredFields.forEach(field => {
        const label = document.querySelector(`label[for="${field.id}"]`);
        if (label && !label.innerHTML.includes('*')) {
            label.innerHTML += ' <span style="color: red;">*</span>';
        }
    });
});