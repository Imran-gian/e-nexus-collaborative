let websites = [];
let bnames = [];
let MAX_PAGES, email, email_app_pass, db_url, start_b;

function injectTheScript() {
    // Gets all tabs that have the specified properties, or all tabs if no properties are specified (in our case we choose current active tab)
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Injects JavaScript code into a page
        chrome.tabs.executeScript(tabs[0].id, {file: "find.js"});
    });
}





//start_b = document.getElementById('start_b').value;
//console.log(start_b);
//start_b.onclick = function(){start();};
chrome.browserAction.onClicked.addListener(function(tab) { start();});

function start(){
injectTheScript();

}
