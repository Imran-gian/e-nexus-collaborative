let websites = [];
let bnames = [];
let MAX_PAGES, email, email_app_pass, db_url, start_b;


/*
 In the current tab, inject the find.js script. The find.js script is responsible for finding businesses and their websites in a given area and exporting them to a JSON file. 
*/
function injectTheScript() {
    // Gets all tabs that have the specified properties, or all tabs if no properties are specified (in our case we choose current active tab)
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Injects JavaScript code into a page
        chrome.tabs.executeScript(tabs[0].id, {file: "find.js"});
    });
}


chrome.browserAction.onClicked.addListener(function(tab) { start();});


/*
 Start the extension's main function.
*/
function start(){
injectTheScript();

}
