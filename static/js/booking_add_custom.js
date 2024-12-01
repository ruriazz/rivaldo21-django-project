const elements = () => ({
    resourceTypeField: document.querySelector('#id_resource_type'),
    roomField: document.querySelector('.field-room'),
    vehicleField: document.querySelector('.field-vehicle'),

    selectResourceType: document.querySelector('select[name="resource_type"]'),
    selectRoom: document.querySelector('select[name="room"]'),
    selectVehicle: document.querySelector('select[name="vehicle"]'),
});

const handleChangeResourceType = function (e) {
    const { roomField, vehicleField, selectRoom, selectVehicle } = elements();

    if (!e.init) {
        $(selectRoom).val(null).trigger('change');
        $(selectVehicle).val(null).trigger('change');
    }

    switch (e?.target?.value) {
        case 'Room':
            $(vehicleField).fadeOut('fast', () => $(roomField).fadeIn('fast'));
            break;

        case 'Vehicle':
            $(roomField).fadeOut('fast', () => $(vehicleField).fadeIn('fast'));
            break;

        default:
            roomField.style.display = 'none';
            vehicleField.style.display = 'none';
            break;
    }
};

document.addEventListener('DOMContentLoaded', function () {
    const { selectResourceType } = elements();

    if (selectResourceType) {
        handleChangeResourceType({ target: { value: $(selectResourceType).val() }, init: true });
        $(selectResourceType).select2().on('change', handleChangeResourceType);
    }
});
