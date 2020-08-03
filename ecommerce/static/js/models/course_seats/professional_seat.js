define([
    'underscore',
    'models/course_seats/course_seat'
],
    function(_,
             CourseSeat) {
        'use strict';
        return CourseSeat.extend({
            defaults: _.extend({}, CourseSeat.prototype.defaults,
                {
                    certificate_type: 'professional',
                    // [COLARAZ_CUSTOM]
                    // Set the default value of is verification required radio button.
                    id_verification_required: true,
                    price: 1000
                }
            )
        }, {seatType: 'professional'});
    }
);
