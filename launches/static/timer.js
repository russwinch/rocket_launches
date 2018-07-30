
function startTime(t0) {
    now = Date.now();
    //
    // get total seconds between the times
    now = now / 1000;
    var delta = Math.abs(t0 - now);

    // calculate (and subtract) whole days
    var days = Math.floor(delta / 86400);
    delta -= days * 86400;

    // calculate (and subtract) whole hours
    var hours = Math.floor(delta / 3600) % 24;
    delta -= hours * 3600;

    // calculate (and subtract) whole minutes
    var minutes = Math.floor(delta / 60) % 60;
    delta -= minutes * 60;

    // what's left is seconds
    var seconds = Math.floor(delta);  // in theory the modulus is not required

    hours = padTime(hours);
    minutes = padTime(minutes);
    seconds = padTime(seconds);
    document.getElementById('txt').innerHTML =
        days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    var t = setTimeout(startTime, 500, t0);
}

function padTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}
