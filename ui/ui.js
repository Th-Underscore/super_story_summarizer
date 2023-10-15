console.log("Running summarizer JS...");
let subjectButton = document.getElementById("subject-button");
subjectButton.addEventListener("click", function() {
    console.log("JS waiting...")
    setTimeout(function() {
        console.log("JS looping!")
        let toggler = document.getElementsByClassName("tree-branch");
        for (let i = 0; i < toggler.length; i++) {
            console.log(`i ${i}`);
            /** {Element} */
            currentElement = toggler[i];
            console.log(`id ${currentElement.id}`);
            currentElement.addEventListener("keyup", function(event) {
                if (event.keyCode === 13) {
                    subjectButton.click();
                }
            });
        }
    }, 2000);
});
console.log("Finished running summarizer JS!");