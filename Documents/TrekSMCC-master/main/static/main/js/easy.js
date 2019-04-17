var cloudText = [];

function getWordCloud(){
    let xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            let data = JSON.parse(this.responseText);
            cloudText = data['cloudText'];
            updateCloud(cloudText);
        }
    };
    
    xhr.open("GET", "/cloudText/", true);
    xhr.send();
}


function updateCloud(){

    // you can use own color converting function if you want
    var my_color = d3.scaleSequential()
    .domain([0, 100])
    .interpolator(d3.interpolatePlasma);

    // makeWordCloud(data, css selector that you wanna insert in, scale of svg, class name of svg, font-family, rotate or not, your color converting function)
    window.makeWordCloud(cloudText, "#cloud", 550, "my_svg", "Impact", true, my_color)

    // [ svg class, font-family, rotate words or not, color function ] are optional.
    // the simplest way => window.makeWordCloud(data, "body", 500)

}