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
const engTransl = get_col(eng, "translation");
const latTransl = get_col(lat, "translation");
const simEngToLat = get_col(eng, "linksToOther");
const simLatToEng = get_col(lat, "linksToOther");
const indexEngToLat = get_col(eng, "matchIndex");
const indexLatToEng = get_col(lat, "matchIndex");

const latOrigDiv = document.querySelector(".latin");
const engOrigDiv = document.querySelector(".english");

populatePage(latOrigDiv, latText, latTransl, LANGUAGES[0]);
populatePage(engOrigDiv, engText, engTransl, LANGUAGES[1]);


function populatePage(parentContainer, textArray, translArray, language) {
  for (i=0; i<=textArray.length;i++) {
    const lineContainer = document.createElement("div");
    lineContainer.setAttribute("data-linenum", `${i}`);
    lineContainer.setAttribute("data-language", language);
    lineContainer.className = "line";
    lineContainer.classList.add(language);
    lineContainer.title = translArray[i];
    lineContainer.addEventListener("mouseover", highlightGroup);
    lineContainer.addEventListener("mouseout", removeHighlight);
  
    const line = document.createElement("span");
    line.setAttribute("id",`${language}Line${i+1}`);
    line.textContent = textArray[i];

    lineContainer.appendChild(line);
    parentContainer.appendChild(lineContainer);
  }
}

function selectCorrespondingLineRefs(srcLineNum, language) {
  if(language == LANGUAGES[1]){
    return [indexEngToLat[srcLineNum], simEngToLat[srcLineNum]];
  } else {
    return [indexLatToEng[srcLineNum], simLatToEng[srcLineNum]];
  }
}

function highlightGroup(event) {
  const self = document.querySelector(`[id="${this.dataset.language}Line${+this.dataset.linenum+1}"]`)
  self.style = "color: rgba(0, 100, 0, 0.5);"
  let correspLines = selectCorrespondingLineRefs(this.dataset.linenum, this.dataset.language);
  let absrefs = correspLines[0];
  let distance = correspLines[1];
  let otherLanguage = (this.dataset.language == LANGUAGES[0]) ? LANGUAGES[1] : LANGUAGES[0];
  for (i in absrefs) {
      const highlight = document.querySelector(`[id="${otherLanguage}Line${absrefs[i]}"]`);
      let similarity = 1 - distance[i]; //put the sigmoid here
      highlight.style = `color: rgba(0,100,0,${similarity}`;
  }
}

function removeHighlight(event) {
  const self = document.querySelector(`[id="${this.dataset.language}Line${+this.dataset.linenum+1}"]`)
  self.style = "color: black;"
  let correspLines = selectCorrespondingLineRefs(this.dataset.linenum, this.dataset.language);
  let absrefs = correspLines[0];
  let otherLanguage = (this.dataset.language == LANGUAGES[0]) ? LANGUAGES[1] : LANGUAGES[0];
  for (i in absrefs) {
      const highlight = document.querySelector(`[id="${otherLanguage}Line${absrefs[i]}"]`);
      highlight.style = "color: black;";
  }
}