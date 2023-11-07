console.log("Running summarizer JS...");
let subjectButton = document.getElementById("subject-button");
subjectButton.addEventListener("click", function() {
	console.log("JS waiting...")
	setTimeout(function() {
		console.log("JS looping!")
		let branches = document.getElementsByClassName("tree-branch");
		for (let i = 0; i < branches.length; i++) {
			console.log(`brch i ${i}`);
			/** The current looped branch 
			 * @type {Element} */
			let branch = branches[i];
			console.log(`brch id ${branch.id}`);
			branch.addEventListener("keyup", function(event) {
				if (event.keyCode === 13) {
					subjectButton.click();
				}
			});
		}
	}, 2000);
});
console.log("Finished running summarizer JS!");