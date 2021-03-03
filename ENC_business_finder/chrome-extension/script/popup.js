//var header = new Headers()
//header["Access-Control-Allow-Origin"]=  "*";

function gonxt(count_) {
  if(count_> MAX_PAGES){
    save_all();
    return;
  }
  // sleep time expects milliseconds
  function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, true); // false for synchronous request
    xmlHttp.setRequestHeader('Access-Control-Allow-Origin','*');
    xmlHttp.send(null);
    return xmlHttp.responseText;
  }
  var WAIT_S = 2000;

  sleep(WAIT_S).then(() => {
    // Do something after the sleep!

    var xpath = "//button[contains(@id,'section-pagination-button-next')]";
    var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
    while (f = matchingElement.iterateNext()) {
      console.log(f.click());
      break;
    }


    var xpath = "//div[@class='section-result-text-content']";
    var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
    while (f = matchingElement.iterateNext()) {
      console.log(f.click());
      break;
    }
    sleep(WAIT_S).then(() => {
      // Do something after the sleep!




      var xpath_bname = "//div[contains(@class, '__text-content')]";
      var xpath_site = "//div[@data-tooltip]";

      var matchingElement = document.evaluate(xpath_site, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
        while (g = matchingElement.iterateNext()) {
          var bname = g.parentNode.parentNode.parentNode.innerText;
          var website = g.getAttribute('data-tooltip');
          try{
          console.log(bnames.push(bname));
          }
          catch(e){console.log(bnames.push("g.previousSibling.innerText"));}
          console.log(websites.push(website));
          console.log(g.parentNode.parentNode.parentNode.innerText);
         
         httpGet(db_url+'?website="'+website+'"&bname="'+bname+'"&country="'+'your country'+'"&lat='+'lat'+'&long='+'lng');


        }




      sleep(WAIT_S).then(() => {
        // Do something after the sleep!
        var xpath = "//span[text()='Back to results']";
        var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
        while (f = matchingElement.iterateNext()) {
          console.log(f.click());
          break;
        }
        sleep(WAIT_S).then(() => {
          // Do something after the sleep!

          var xpath = "//button[contains(@id,'section-pagination-button-next')]";
          var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
          while (f = matchingElement.iterateNext()) {
            console.log(f.click());
            break;
          }
          sleep(WAIT_S).then(() => {
            count_+=1;
            gonxt(count_);
          
        });
        });
      });

    });



  });



}
function saveTextAsFile(fileNameToSaveAs, textToWrite)
{
    //var textToWrite = document.getElementById("inputTextToSave").value;
    var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
    //var fileNameToSaveAs = document.getElementById("inputFileNameToSaveAs").value;
      var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
    downloadLink.innerHTML = "Download File";
    if (window.webkitURL != null)
    {
        // Chrome allows the link to be clicked
        // without actually adding it to the DOM.
        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    }
    else
    {
        // Firefox requires the link to be added to the DOM
        // before it can be clicked.
        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }

    downloadLink.click();
}
function save_all()
{
  f_site = "sb_sites.txt";
  txt_site = []; 
    f_bname = "sb_bnames.txt";
  txt_bname = []; 



  for(w in websites){
    txt_site.push({'website':websites[w], 'bname':bnames[w]});

  }
    saveTextAsFile(f_site, JSON.stringify(txt_site));
  //saveTextAsFile(f_bname, SON.stringify(txt_bname));
}
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
