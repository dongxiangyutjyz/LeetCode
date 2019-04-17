var fill = d3.interpolateSinebow(Math.random());

window.makeWordCloud = function(data, parent_elem, svgscale, svg_class, font, rotate_word, my_colors){

      function draw(words) {
        d3.select(parent_elem).append("svg")
            .attr("width", "100%")
            .attr("height", 550)
            //.attr("viewBox", "0 0 50 50")
            //.attr("preserveAspectRatio", "none")
            .attr("class", svg_class)
          .append("g")
            .attr("transform", "translate(" + svgscale / 2 + "," + svgscale / 2 + ")")
          .selectAll("text")
            .data(words)
          .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", font)
            .style("fill", function(d, i) { if(my_colors){ return my_colors(i); }else{ return fill(i); } })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
      }

      if(svg_class){ d3.select("." + svg_class).remove() }
      else{ d3.select("svg").remove() }

      var data_max =  d3.max(data, function(d){ return d.value } );
      var sizeScale = d3.scaleLinear().domain([0, data_max]).range([0, 1])

      data = data.map(function(d) {
        return {text: d.word, size: 10 + sizeScale(d.value) * 90};
      })

      var layout = d3.layout.cloud().size([svgscale, svgscale])
        .words(data)
        .padding(5)
        .fontSize(function(d) { return d.size; })

      if(!rotate_word){ layout.rotate(function() { return ~~(Math.random() * 2) * 90; }) }

      layout
        .on("end", draw)
        .start();
  }