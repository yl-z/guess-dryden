// Grab data from the static JSON file
var eng = english;
var lat = latin;  //remember to put these labels in if reloading the data

function get_col(data, col){
  let lines = [];
  for (let row in data){
    lines.push(data[row][col]);
  }
  return lines;
}

var groupData = [get_col(lat, "line"), get_col(eng, "line")]

const svg = d3.select("svg");

const g = svg.selectAll("g")
            .data([1,2])
            .enter()
            .append("g");

const g1 = g.select("g").selectAll("text")
              .data(groupData[0])
              .enter()
              .append("text")
              .attr("x", (d,i)=>10 )
              .attr("y", (d,i)=>20*i + 20)
              .text((d,i) => d);

const g2 = g.selectAll("text")
              .data(groupData[1])
              .enter()
              .append("text")
              .attr("x", (d,i)=>100 )
              .attr("y", (d,i)=>20*i + 20)
              .text((d,i) => d);
