() => {
	console.log("JS looping!");
	let gradioBranches = document.getElementsByClassName("gradio-branch");
	for (let i = 0; i < gradioBranches.length; i++) {
		
	}

	let divs = document.getElementsByClassName("tree-div");
	for (let i = 0; i < divs.length; i++) {
		console.log(`brch i ${i}`);
		/** The current looped div 
		 * @type {Element} */
		let div = divs[i];
		console.log(`div id ${div.id}`);
		/** The current looped Gradio textbox parent div
		 * @type {Element} */
		let branch = document.getElementById(`textbox-${div.id}`);
		if (branch) {
			console.log(`textbox id ${branch.id}`);
			div.appendChild(branch)

			console.log(`${i} branch ${branch.id} | classList ${branch.classList}`);
			branch.classList.remove("padded");
			console.log(true, `new classList ${branch.classList}`);
			/** The current textbox parent label
			 * @type {Element} */
			let label = branch.children[0];
			console.log(`${i} label ${label.id}`);
			label.classList.add("tree-branch");
			console.log(true);
			/** The current textbox
			 * @type {Element} */
			let textbox = label.children[1];
			console.log(`${i} textbox ${textbox.id}`);
			textbox.classList.add("tree-branch", "branch-text");
			console.log(true);
		}
	}
}