// We bring NoSleep.js in via a script tag
declare var NoSleep: any;
declare var screenfull: any;

function toggleFullScreen() {
    const doc = document as any;
    if (
        doc.fullscreenElement ||
        doc.mozFullScreenElement ||
        doc.webkitFullscreenElement
    ) {
        if (doc.cancelFullScreen) {
            doc.cancelFullScreen();
        } else {
            if (doc.mozCancelFullScreen) {
                doc.mozCancelFullScreen();
            } else {
                if (doc.webkitCancelFullScreen) {
                    doc.webkitCancelFullScreen();
                }
            }
        }
    } else {
        const _element = document.documentElement as any;
        if (_element.requestFullscreen) {
            _element.requestFullscreen();
        } else {
            if (_element.mozRequestFullScreen) {
                _element.mozRequestFullScreen();
            } else {
                if (_element.webkitRequestFullscreen) {
                    _element.webkitRequestFullscreen(
                        (Element as any).ALLOW_KEYBOARD_INPUT
                    );
                }
            }
        }
    }
}

function isEven(n: number) {
    n = Number(n);
    return n === 0 || !!(n && !(n % 2));
}

async function updateImage(index: number, urls: string[]) {
    const url = urls[index];
    console.log("Switching to image: ", url);

    // Get the image and turn it into an objectURL
    let response = await fetch(url);
    let blob = await response.blob();
    let objectURL = await URL.createObjectURL(blob);

    // Get our elements
    if (isEven(index)) {
        var activeElement = document.getElementById("even") as HTMLImageElement;
        var inActiveElement = document.getElementById("odd") as HTMLImageElement;
    } else {
        var activeElement = document.getElementById("odd") as HTMLImageElement;
        var inActiveElement = document.getElementById("even") as HTMLImageElement;
    }

    // Update the image of the active element
    await activeElement.setAttribute("src", objectURL);

    // Now that it is set in the DOM, we can release it and prevent a memory leak.
    await URL.revokeObjectURL(objectURL);

    // Let things settle
    await delay(500);
    await activeElement.classList.add("active");

    // Remove the active class from the inactive element
    await inActiveElement.classList.remove("active");
}

async function delay(milliseconds: number) {
    return new Promise<void>(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

window.onload = async function() {


    function fullscreen() {
        if (screenfull.enabled) {
            screenfull.request();
        }
    }

    // Bind image.click to toggleFullscreen
    const images = document.getElementsByTagName("img");
    for (let i = 0; i < images.length; i++) {
        console.log(images[i]);
        // images[i].onclick = toggleFullScreen;
        images[i].onclick = fullscreen;
    }

    //Bind button to toggleFullscreen
    const button = document.getElementById("button");
    if (button) {
        button.onclick = fullscreen;
    }

    // Do not dim the screen on touch devices
    if ("ontouchstart" in document.documentElement) {
        let noSleep = new NoSleep();
        noSleep.enable();
    }

    // Get the images json
    const imagesResponse = await fetch("/images");
    const imageUrls = await imagesResponse.json();

    // No need to randomize the image to start at since we get a
    // shuffled list back from the server
    let index = 0;

    // Set the first image
    await updateImage(index, imageUrls);

    while (true) {
        // Increment the index
        index = ++index % imageUrls.length;

        // Change the image
        await updateImage(index, imageUrls);

        // Hang back
        await delay(5000);
    }
};
