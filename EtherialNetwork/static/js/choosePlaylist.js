function choosePlaylist() {

    //  Identify which button was clicked
    var button = event.target;
    var artist = button.id;

    //  Create switch statements for all artists
    switch (artist) {
        case "drake":
            var playlist = "spotify:playlist:0xusFOostuuUb0esNzTbbO";
            console.log(playlist)
            break;
        case "wayne":
            var playlist = "spotify:playlist:5z4CU5tS0uB5gG7KyCL5JZ";
            break;
        case "ye":
            var playlist = "spotify:playlist:7orczKKXJdOUwt1UroSZza";
            break;
        case "uzi":
            var playlist = "spotify:playlist:08FBP3J3z517LBCxBKbZjY";
            break;
    }
    
    
            
}