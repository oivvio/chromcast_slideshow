"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function isEven(n) {
    n = Number(n);
    return n === 0 || !!(n && !(n % 2));
}
function updateImage(index, urls) {
    return __awaiter(this, void 0, void 0, function* () {
        const url = urls[index];
        // Does this gurantee that the image is ready for use
        let response = yield fetch(url);
        let blob = yield response.blob();
        let objectURL = yield URL.createObjectURL(blob);
        // console.log("hang back 1000ms");
        // await delay(1000);
        if (isEven(index)) {
            var activeElement = document.getElementById("even");
            var inActiveElement = document.getElementById("odd");
        }
        else {
            var activeElement = document.getElementById("odd");
            var inActiveElement = document.getElementById("even");
        }
        // Update the image of the active element
        // And add the active class
        // activeElement.src = objectURL;
        yield activeElement.setAttribute("src", objectURL);
        // Now that it is set in the DOM, we can release it and prevent a memory leak.
        yield URL.revokeObjectURL(objectURL);
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
        // Do not dim the screen
        let noSleep = new NoSleep();
        noSleep.enable();
        // Get the images json
        const imagesResponse = yield fetch("/images");
        const imageUrls = yield imagesResponse.json();
        // Randomize the image to start at.    
        let index = Math.round(Math.random() * imageUrls.length);
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
