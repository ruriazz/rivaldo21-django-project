const RESOURCE_TYPES = {
    ROOM: 'Room',
    VEHICLE: 'Vehicle'
};

const getElements = () => {
    const selectors = {
        resourceType: '#id_resource_type',
        room: '.field-room',
        vehicle: '.field-vehicle',
        destinationAddress: '.field-destination_address',
        departement: '.field-departement'
    };

    const requiredSpan = document.createElement('span');
    requiredSpan.className = 'text-red';
    requiredSpan.textContent = '* ';

    return Object.entries(selectors).reduce((acc, [key, selector]) => ({
        ...acc,
        [`${key}Field`]: document.querySelector(selector),
        [`${key}Input`]: document.querySelector(`[name="${key.replace(/([A-Z])/g, '_$1').toLowerCase()}"]`)
    }), { requiredSpan });
};

const fadeTransition = (hideEl, showEl) => {
    return new Promise(resolve => {
        $(hideEl).fadeOut('fast', () => {
            if (showEl) {
                $(showEl).fadeIn('fast', resolve);
            } else {
                resolve();
            }
        });
    });
};

const handleResourceTypeChange = async (e) => {
    const elements = getElements();
    const { roomField, vehicleField, destinationAddressField } = elements;
    const resourceType = e?.target?.value;

    if (!e.init) {
        ['room', 'vehicle', 'destinationAddress'].forEach(field => {
            const input = elements[`${field}Input`];
            $(input).val(null).trigger('change');
        });
    }

    const actions = {
        [RESOURCE_TYPES.ROOM]: async () => {
            await fadeTransition(vehicleField, roomField);
            await fadeTransition(destinationAddressField);
        },
        [RESOURCE_TYPES.VEHICLE]: async () => {
            await fadeTransition(roomField);
            $(vehicleField).fadeIn('fast');
            $(destinationAddressField).fadeIn('fast');
        },
        default: () => {
            [roomField, vehicleField, destinationAddressField].forEach(field => {
                field.style.display = 'none';
            });
        }
    };

    (actions[resourceType] || actions.default)();
};

document.addEventListener('DOMContentLoaded', () => {
    const {
        resourceTypeInput: selectResourceType,
        roomField,
        vehicleField,
        departementField,
        destinationAddressField,
        requiredSpan
    } = getElements();

    if (roomField && departementField && vehicleField && destinationAddressField) {
        const fields = [roomField, vehicleField, departementField, destinationAddressField];
        fields.forEach(field => {
            const label = field.querySelector('label');
            if (label) {
                label.appendChild(requiredSpan.cloneNode(true));
            }
        });
    }

    if (selectResourceType) {
        handleResourceTypeChange({
            target: { value: $(selectResourceType).val() },
            init: true
        });
        $(selectResourceType).select2().on('change', handleResourceTypeChange);
    }
});
