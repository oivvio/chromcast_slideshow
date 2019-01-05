function isEven(n: number) {
    n = Number(n);
    return n === 0 || !!(n && !(n % 2));
}

function isOdd(n: number) {
    return isEven(Number(n) + 1);
}

function updateImage(index: number, urls: string[]) {
    const url = urls[index];

    if (isEven(index)) {
        var activeElement = document.getElementById("even") as HTMLImageElement;
        var inActiveElement = document.getElementById("odd") as HTMLImageElement;

    } else {
        var activeElement = document.getElementById("odd") as HTMLImageElement;
        var inActiveElement = document.getElementById("even") as HTMLImageElement;
    }

    // Update the image of the active element
    // And add the active class
    activeElement.src = url;
    activeElement.classList.add("active");

    // Remove the active class from the inactive element
    inActiveElement.classList.remove("active");


    return true;
}


window.onload = function() {
    console.log("set!");

    // Get the images json
    fetch("/images")
        .then(function(response) {
            return response.json();
        })
        .then(function(image_urls) {
            // Randomize the image to start at.
            var index = Math.round(Math.random() * image_urls.length);

            // Set the first image
            updateImage(index, image_urls);

            // Start an infinite loop
            var imageUpdateloop = setInterval(function() {
                // Increment the index
                index = ++index % image_urls.length;

                // Update the image
                updateImage(index, image_urls);
            }, 5000);

            var timeUpdateLoop = setInterval(function() {
                var now = new Date();
                var timeString = now.getHours() + ":" + now.getMinutes();

                console.log(timeString);
                // Increment the index
                // index = ++index % image_urls.length;

                // Update the image
                // updateImage(index, image_urls);
            }, 100);

        });
};
