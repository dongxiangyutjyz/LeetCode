
var tweetText = [];
var tweetCreatedAt = [];
var userName = [];
var tweetLocation = [];
var tweetID = [];
var tweetUserDisplay = [];

function removeElement(elementId) {
    // Removes an element from the document
    var myNode = document.getElementById(elementId);
	while (myNode.firstChild) {
   		myNode.removeChild(myNode.firstChild);
	}

}

function updateFeed(tweetText, tweetCreatedAt, tweetUserDisplay, tweetLocation, tweetID, userName){
	for (var i = 0; i < 5; i++){
	    var feed = document.getElementById("feed");

	    var a = document.createElement("a");
	    a.setAttribute('id', tweetID[i]+ " " + userName[i]);
	    a.setAttribute('class',"list-group-item list-group-item-action flex-column align-items-start active");


	    var div = document.createElement("div");
	    div.setAttribute('id',tweetID[i] + " " + userName[i]);
	    div.setAttribute('class',"d-flex w-100 justify-content-between");
	    div.setAttribute('style',"height: 50px");
	    a.appendChild(div);

	    var h5 = document.createElement("h5");
	    h5.setAttribute('id',tweetID[i]+ " " + userName[i]);
	    h5.setAttribute('class',"mb-1");

	    var newContent = document.createTextNode(tweetUserDisplay[i]); 
	  	h5.appendChild(newContent); 
	  	div.appendChild(h5);

	  	var small = document.createElement("small");
	  	var createAt = document.createTextNode(tweetCreatedAt[i]); 
	  	small.appendChild(createAt);  
	  	div.appendChild(small);

	  	var p = document.createElement("p");
	    p.setAttribute('id', tweetID[i]+ " " + userName[i]);
	    p.setAttribute('class',"m-0");
	    
	    var tweettext = document.createTextNode(tweetText[i]); 
	  	p.appendChild(tweettext);  
	    a.appendChild(p);

	   	var small = document.createElement("small");
	  	var location = document.createTextNode(tweetLocation[i]); 
	  	small.appendChild(location);  
	  	a.appendChild(small);

	  	feed.appendChild(a);
	}
}

function getFeed(){
	let xhr = new XMLHttpRequest();
	
	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200){
			let data = JSON.parse(this.responseText);
			tweetText = data['tweetText'];
			tweetCreatedAt = data['tweetCreatedAt'];
			userName = data["userName"];
			tweetLocation = data['tweetLocation'];
			tweetID = data['tweetID'];
			tweetUserDisplay = data['tweetUserDisplay'];
			removeElement("feed");
			updateFeed(tweetText, tweetCreatedAt, tweetUserDisplay, tweetLocation, tweetID, userName);
		}
	};
	
	xhr.open("GET", "/feed/", true);
	xhr.send();
}


