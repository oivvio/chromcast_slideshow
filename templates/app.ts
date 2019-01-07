// We bring NoSleep.js in via a script tag
declare var NoSleep: any;

function isEven(n: number) {
    n = Number(n);
    return n === 0 || !!(n && !(n % 2));
}

async function updateImage(index: number, urls: string[]) {
    const url = urls[index];

    // Does this gurantee that the image is ready for use
    let response = await fetch(url);
    let blob = await response.blob();
    let objectURL = await URL.createObjectURL(blob);

    // console.log("hang back 1000ms");
    // await delay(1000);

    if (isEven(index)) {
        var activeElement = document.getElementById("even") as HTMLImageElement;
        var inActiveElement = document.getElementById("odd") as HTMLImageElement;

    } else {
        var activeElement = document.getElementById("odd") as HTMLImageElement;
        var inActiveElement = document.getElementById("even") as HTMLImageElement;
    }

    // Update the image of the active element
    // And add the active class
    // activeElement.src = objectURL;
    await activeElement.setAttribute("src", objectURL);

    // Now that it is set in the DOM, we can release it and prevent a memory leak.
    // await URL.revokeObjectURL(objectURL);

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

    // Do not dim the screen

    let noSleep = new NoSleep();
    noSleep.enable();

    // Get the images json
    const imagesResponse = await fetch("/images");
    const imageUrls = await imagesResponse.json();

    // Randomize the image to start at.    
    let index = Math.round(Math.random() * imageUrls.length);

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
