@18.5069065,73.8787829,17z


for(var i =0;i<5;i++){
var xpath = "//div[@class='section-result-text-content']"; 
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}

var xpath = "//span[text()='Website']";
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click())}

var xpath = "//span[text()='Back to results']";
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}

var xpath = "//button[contains(@id,'section-pagination-button-next')]"; 
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}
}
//18.5127529,73.8743946,16z
var websites = [];
var bnames = [];
for(var i =0;i<5;i++){
// sleep time expects milliseconds
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
var WAIT_S = 500;

sleep(WAIT_S).then(() => {
    // Do something after the sleep!
   
    var xpath = "//button[contains(@id,'section-pagination-button-next')]"; 
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}


var xpath = "//div[@class='section-result-text-content']"; 
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}
sleep(WAIT_S).then(() => {
    // Do something after the sleep!
    



	    var xpath_bname = "//div[contains(@class, '__text-content')]";
	    var xpath_site = "//div[@data-tooltip]";

	var matchingElement = document.evaluate(xpath_bname, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){



	var matchingElement = f.nextSibling.evaluate(xpath_site, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(g = matchingElement.iterateNext())
	{
	console.log(bnames.push({'bname':f.innerText}));
	console.log(websites.push({'website':g.getAttribute('data-tooltip')}));

	//httpGet('http://localhost:5003/?website="'+g.getAttribute('data-tooltip')+'"&bname="'+f.innerText+'"&country="'+'your country'+'"&lat='+'lat'+'&long='+'lng');


	}




}




sleep(WAIT_S).then(() => {
    // Do something after the sleep!
   var xpath = "//span[text()='Back to results']";
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}
    sleep(WAIT_S).then(() => {
    // Do something after the sleep!
   
    var xpath = "//button[contains(@id,'section-pagination-button-next')]"; 
var matchingElement = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);while(f = matchingElement.iterateNext()){console.log(f.click());break;}
});
});
    
});



});



}


for(w in websites){
let site = websites[w];

httpGet('http://localhost:5003/?website="'+site+'"&bname="'+'bname'+'"&country="'+'your country'+'"&lat='+'lat'+'&long='+'lng');

}
function logTabsForWindows(windowInfoArray) {
  for (windowInfo of windowInfoArray) {
    console.log(`Window: ${windowInfo.id}`);
    console.log(windowInfo.tabs.map(tab => tab.url));
  }
}

function onError(error) {
  console.log(`Error: ${error}`);
}

browser.browserAction.onClicked.addListener((tab) => {
  var getting = browser.windows.getAll({
    populate: true,
    windowTypes: ["normal"]
  });
  getting.then(logTabsForWindows, onError);
});

