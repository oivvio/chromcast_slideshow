"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function toggleFullScreen() {
    const doc = document;
    if (doc.fullscreenElement ||
        doc.mozFullScreenElement ||
        doc.webkitFullscreenElement) {
        if (doc.cancelFullScreen) {
            doc.cancelFullScreen();
        }
        else {
            if (doc.mozCancelFullScreen) {
                doc.mozCancelFullScreen();
            }
            else {
                if (doc.webkitCancelFullScreen) {
                    doc.webkitCancelFullScreen();
                }
            }
        }
    }
    else {
        const _element = document.documentElement;
        if (_element.requestFullscreen) {
            _element.requestFullscreen();
        }
        else {
            if (_element.mozRequestFullScreen) {
                _element.mozRequestFullScreen();
            }
            else {
                if (_element.webkitRequestFullscreen) {
                    _element.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                }
            }
        }
    }
}
function isEven(n) {
    n = Number(n);
    return n === 0 || !!(n && !(n % 2));
}
function updateImage(index, urls) {
    return __awaiter(this, void 0, void 0, function* () {
        const url = urls[index];
        console.log("Switching to image: ", url);
        // Get the image and turn it into an objectURL
        let response = yield fetch(url);
        let blob = yield response.blob();
        let objectURL = yield URL.createObjectURL(blob);
        // Get our elements
        if (isEven(index)) {
            var activeElement = document.getElementById("even");
            var inActiveElement = document.getElementById("odd");
        }
        else {
            var activeElement = document.getElementById("odd");
            var inActiveElement = document.getElementById("even");
        }
        // Update the image of the active element
        yield activeElement.setAttribute("src", objectURL);
        // Now that it is set in the DOM, we can release it and prevent a memory leak.
        yield URL.revokeObjectURL(objectURL);
        // Let things settle
        yield delay(500);
        yield activeElement.classList.add("active");
        // Remove the active class from the inactive element
        yield inActiveElement.classList.remove("active");
    });
}
function delay(milliseconds) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise(resolve => {
            setTimeout(resolve, milliseconds);
        });
    });
}
window.onload = function () {
    return __awaiter(this, void 0, void 0, function* () {
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
        const imagesResponse = yield fetch("/images");
        const imageUrls = yield imagesResponse.json();
        // No need to randomize the image to start at since we get a
        // shuffled list back from the server
        let index = 0;
        // Set the first image
        yield updateImage(index, imageUrls);
        while (true) {
            // Increment the index
            index = ++index % imageUrls.length;
            // Change the image
            yield updateImage(index, imageUrls);
            // Hang back
            yield delay(5000);
        }
    });
};
