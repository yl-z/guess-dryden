const eng = english;
const lat = latin;
let LANGUAGES = ["lat","eng"];

function get_col(data, col){
  let arr = [];
  for (row in data){
    arr.push(data[row][col]);
  }
  return arr;
}

const engText = get_col(eng, "line");
const latText = get_col(lat, "line");

const latOrigDiv = document.querySelector(".latin");
const engOrigDiv = document.querySelector(".english");
const connectionsFromEng = get_col(eng, "linksToLines");
const connectionsFromLat = get_col(lat, "linksToLines");

populate(latOrigDiv, latText, LANGUAGES[0]);
populate(engOrigDiv, engText, LANGUAGES[1]);


function populate(parentContainer, textArray, language) {
  for (i=0; i<=textArray.length;i++) {
    //using this two layer structure for now to make it easier to append more visuals 
    //to individual lines or to break into words
    const lineContainer = document.createElement("div");
    lineContainer.setAttribute("data-linenum", `${i}`);
    lineContainer.setAttribute("language", language);
    lineContainer.setAttribute("keepState", 0);
    lineContainer.className = "line";
    lineContainer.addEventListener("mouseover", highlightGroup);
    //lineContainer.addEventListener("click", keepView);
    lineContainer.addEventListener("mouseout", removeHighlight);
  
    const line = document.createElement("span");
    line.setAttribute("id",`${language}Line${i+1}`);
    line.textContent = textArray[i];

    lineContainer.appendChild(line);
    parentContainer.appendChild(lineContainer);
  }
}

function selectCorrespondingLineNums(srcLineNum, div) {
  if(div.classList.contains("eng")){
    return connectionsFromEng[srcLineNum].length;
  } else {
    return connectionsFromLat[srcLineNum].length;
  }
}

function highlightGroup(event) {
  this.style = "color: rgba(0,100,0, 0.5);";
  
  let numCorrespLines = selectCorrespondingLineNums(this.dataset.linenum, this);
  let language = LANGUAGES[1];
  if (this.dataset.language==LANGUAGES[1]) {
    language = LANGUAGES[0];
  }

  for (let i=0; i<numCorrespLines; i++) {
    let absLineRef = i + +this.dataset.linenum - Math.round(numCorrespLines/2);

    if (absLineRef > 0) { //this should be better with an actual key-reference array
      const highlight = document.querySelector(`#${language}Line${absLineRef+1}`);
      
      let confidence = 1 - 1/(1+Math.exp(-30*(connectionsFromLat[this.dataset.linenum][i]-0.5)));
      //pass through sigmoid function for mapping Move this to the Python!!

      highlight.classList.add("spotlight");
      highlight.style = `color: rgba(0,100,0,${confidence}`;
      //highlight.setAttribute("keepState", 0);
    } 
  }
}

/*
function keepView(event) {
  this.setAttribute("keepState", 1);
  console.log(this);
  
  let numCorrespLines = selectCorrespondingLineNums(this.dataset.linenum, this);
  let language = LANGUAGES[1];
  if (this.dataset.language==LANGUAGES[1]) {
    language = LANGUAGES[0];
  }

  for (let i=0; i<numCorrespLines; i++) {
    let absLineRef = i + +this.dataset.linenum - Math.round(numCorrespLines/2);

    if (absLineRef > 0) { //this should be better with an actual key-reference array
      const highlight = document.querySelector(`#${language}Line${absLineRef+1}`);
      highlight.setAttribute("keepState", 1);
    } 
  }
}
*/

function removeHighlight(event) {
  this.style = "color: black;";

  let numCorrespLines = selectCorrespondingLineNums(this.dataset.linenum, this);
  let language = LANGUAGES[1];
  if (this.classList.contains(LANGUAGES[1])) {
    language = LANGUAGES[0];
  }

  for (let i=0; i<numCorrespLines; i++) {
    let absLineRef = i + +this.dataset.linenum - Math.floor(numCorrespLines/2);
    
    if (absLineRef > 0) {
      const highlight = document.querySelector(`#${language}Line${absLineRef+1}`);
      highlight.classList.remove("spotlight");
      highlight.style = "color: black;";
    }
  }
}



/* bar graphs etc.
      const translationLine = document.createElement("p");
      translationLine.textContent = gtransToLat[i];
      translationLine.setAttribute("data-linenum", `${i}`);
      translationLine.setAttribute("id",`engToLat${i+1}`);
      gtransToLatDiv.appendChild(translationLine);

      const translationLine = document.createElement("p");
      translationLine.textContent = gtransToEng[i];
      translationLine.setAttribute("data-linenum", `${i}`);
      translationLine.setAttribute("id", `latToEng${i+1}`);
      gtransToEngDiv.appendChild(translationLine);

      const rightBar = document.createElement("span");
      rightBar.classList.add("dataBar");
      rightBar.style.width = `${confidence*10}px;`;
      rightBar.id = `${this.dataset.linenum}-${i}`;
      rightBar.textContent = "------";
      highlight.appendChild(rightBar);
      console.log(rightBar);

      const rightBar = document.querySelector(`[id = "${this.dataset.linenum}-${i}"]`);
      rightBar.remove();
*/