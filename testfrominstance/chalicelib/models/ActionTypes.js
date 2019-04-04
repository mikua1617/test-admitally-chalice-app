// Appointment status depending upon the events in the videosession
// default: PENDING

export const NOT_CONECTED = 'PENDING';
export const CONNECTED = 'CONNECTED';  //When there is atlest one participant connected to the room
export const COMPLETED = 'COMPLETED';  //When no one is left in the room
    