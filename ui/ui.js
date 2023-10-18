/**
 * Connect to Gradio to share Python variables and vice versa.
 */
async function communicateWithPython() {
	// let gradio = await import("@gradio/client");
	// let client = gradio.client;
	// const app = await client(LISTEN_HOST);
}

window.superStorySummarizer = {};
/**
 * Global module values to communicate between client JavaScript and server Python.
**/
let summarizerValues = window.superStorySummarizer;

summarizerValues.test = "THIS IS A TEST. CAN PYTHON READ THIS?"

console.log("Running summarizer JS...");
let tabs = document.getElementsByClassName("tab-nav");
for (let i = 0; i < tabs.length; i++) {
	let tabButtons = tabs[i].getElementsByTagName("*");
	/** @type {Button} */
	let summarizerTab;
	for (let j = 0; j < tabButtons.length; j++) {
		let tabButton = tabButtons[i];
		if (tabButton && (tabButton.innerHTML == "Summarizer")) {
			tabButton.addEventListener("click", function() {
				
			});
		}
	};
	console.log(`${tabs[i].getElementsByTagName("*")} | ${tabs[i].firstChild.textContent}`);
	console.log(tabs[i].firstChild);
};
console.log("Finished running summarizer JS!");

communicateWithPython();