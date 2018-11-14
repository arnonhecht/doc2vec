// const getTodosEndPoint = "http://0.0.0.0:5001/";
const getTodosEndPoint =
  "https://0zblxdjtm3.execute-api.eu-central-1.amazonaws.com/production/";
window.oracol = { questions: [] };

window.onload = function() {
  getQuestions();
};

function displayQuestions(todos) {
  console.log("todos");
  console.log(todos);
  const $todosElement = $(".todo-list");
  $todosElement.empty();
  todos.forEach(td => {
    $todosElement.append(`
      <div class="todo display-flex-space-between">
        <div>${td.question} (${td.tag})</div>
        <button onclick="removeQuestion('${td.question}')">X</button>
      </div>
    `);
  });
}

function setQuestions(questions) {
  window.oracol.questions = questions;
  displayQuestions(questions);
}

function addQuestion() {
  const $question = $(".new-question");
  const $label = $(".new-label");
  const val = $question.val();
  const label = $label.val();
  if (val && val.length > 0 && label && label.length > 0) {
    const newQuestion = { question: val, tag: label };
    postQuestions(window.oracol.questions.concat([newQuestion]));
    $question.val("");
    $label.val("");
  }
}

function removeQuestion(question) {
  window.oracol.questions = window.oracol.questions.filter(
    q => q.question !== question
  );
  postQuestions(window.oracol.questions);
}

function toggleInputsDisabled(bool) {}

// API

function getQuestions() {
  return $.ajax({
    url: getTodosEndPoint,
    type: "GET",
    crossDomain: true,
    dataType: "jsonp",
    success: function(data) {
      setQuestions(data);
      return data;
    },
    error: function(a) {
      console.error("Failed getQuestions!");
    },
    beforeSend: setHeader
  });
}

// function postQuestions(data) {
//   return $.ajax({
//     url: getTodosEndPoint,
//     type: "GET",
//     data: "questions_arr=" + JSON.stringify(data),
//     // contentTypez: "application/json; charset=UTF-8",
//     crossDomain: true,
//     dataType: "jsonp",
//     success: getQuestions,
//     error: function(a) {
//       console.error("Failed postQuestions!");
//     },
//     beforeSend: setHeader
//   });
// }
function postQuestions(data) {
  return $.ajax({
    url: getTodosEndPoint + "update_questions",
    type: "POST",
    // data: JSON.stringify(data),
    // data: { questions_arr: data },
    data: JSON.stringify({ questions_arr: data }),
    success: getQuestions,
    // dataType: "json",
    contentType: "application/json",
    error: function(a) {
      console.error("Failed postQuestions!");
    },
    beforeSend: setHeader
  });
}

function setHeader(xhr) {
  xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
  xhr.setRequestHeader("contentType", "application/json");
}
