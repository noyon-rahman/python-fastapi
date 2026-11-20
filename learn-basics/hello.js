console.log("Hello from JavaScript!");

const term = "variable";
console.log(`Today: ${term}`)

let learned = false;
let defination = null;
console.log(learned, defination);

if(learned){
  console.log("Already learned!");
}else{
  console.log("Still learning...");
}

if(term === "variable" && !learned){
  console.log("Time to learn variables!");
}

const tags = ["python", "basics"];
tags.push("api");
console.log(tags.length);
console.log(tags.includes("api"));

const note = { term: "variable", defination: "A name that stores a value."};
console.log(note.term)

const notes = [
  {
    id: 1,
    term: "variable",
    defination: "A name that stores a value.",
    js_equivalent: "let / const",
    tags: ["python", "basics"], 
    learned: true,
  },
  {
    id: 2,
    term: "list",
    defination: "An orderded collection of values.",
    js_equivalent: "array",
    tags: ["python", "data"], 
    learned: true,
  },
  {
    id: 3,
    term: "dictionary",
    defination: "An unordered collection of key-value pairs.",
    js_equivalent: "object",
    tags: ["python", "data"], 
    learned: false,
  },
  {
    id: 4,
    term: "function",
    defination: "A block of code that can be reused.",
    js_equivalent: "function",
    tags: ["python", "basics"], 
    learned: false,
  }
]

for (const note of notes){
  console.log(note.term);
}

const query = "LI";
for (const note of notes){
  if(note.term.toLowerCase().includes(query.toLowerCase())){
    console.log("Found:", note.term);
  }
}

function findTerm(notes, name){
  for(const note of notes){
    if(note.term === name){
      return term;
    }
  }
}

console.log(findTerm(notes, "dict"))
console.log(findTerm(notes, "class"))