document.addEventListener('DOMContentLoaded', function () {
    // Ambil elemen Resource type dan field Room/Vehicle
    const resourceTypeField = document.querySelector('#id_resource_type');
    const roomField = document.querySelector('.field-room');
    const vehicleField = document.querySelector('.field-vehicle');

    // Fungsi untuk menampilkan/menghilangkan field
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

    // Jalankan saat halaman dimuat pertama kali
    toggleFields();

    // Tambahkan event listener untuk perubahan pada Resource type
    if (resourceTypeField) {
        resourceTypeField.addEventListener('change', toggleFields);
    }
});
