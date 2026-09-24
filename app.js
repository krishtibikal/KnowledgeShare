const visualById = {
  api: ["art-api", '<div class="mini-flow"><b>request</b><i></i><b>service</b><i></i><b>truth</b></div>'],
  "prompt-systems": ["art-loop", '<div class="loop-ring"><span>prompt</span><span>harness</span><span>loop</span></div>'],
  "math-probability": ["art-linear", '<div class="axis"></div><div class="matrix"><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b></div>'],
  "machine-learning": ["art-neural", '<div class="neural"><div><i></i><i></i><i></i></div><div><i></i><i></i><i></i></div><div><i></i><i></i><i></i></div></div>'],
  "python-data": ["art-grid", '<div class="ref-grid"><b>data</b><b>clean</b><b>plot</b><b>query</b><b>model</b><b>share</b><b>load</b><b>shape</b><b>learn</b></div>'],
  "data-systems": ["art-rag", '<div class="rag-lines"><div><i></i><i></i><i></i></div><span>→</span><div><i></i><i></i><i></i></div></div>'],
  "deep-learning": ["art-neural", '<div class="neural"><div><i></i><i></i><i></i></div><div><i></i><i></i><i></i></div><div><i></i><i></i><i></i></div></div>'],
  "llm-generative-ai": ["art-llm", '<div class="llm-stack"><i></i><i></i><i></i><i></i></div>'],
  "rag-agents": ["art-rag", '<div class="rag-lines"><div><i></i><i></i><i></i></div><span>→</span><div><i></i><i></i><i></i></div></div>'],
  "computer-vision": ["art-prob", '<div class="prob-bars"><i></i><i></i><i></i><i></i><i></i></div>'],
  mlops: ["art-api", '<div class="mini-flow"><b>ship</b><i></i><b>watch</b><i></i><b>learn</b></div>'],
  "learning-paths": ["art-loop", '<div class="loop-ring"><span>learn</span><span>practice</span><span>build</span></div>']
};
const assetUrl = (file) => `assets/reference/${file}?v=20260924-clean9`;

const summaries = {
  api: ["Quality is a set of questions, not a single status code.", ["Contract and validation tests protect the boundary.", "Integration and end-to-end tests verify the system around an endpoint.", "Load, security, performance, reliability, and negative tests reveal operational risk."]],
  "prompt-systems": ["A prompt is one layer in a complete AI workflow.", ["Prompt defines intent, constraints, and output shape.", "Context supplies the useful information and examples.", "Harnesses and loops add tools, checks, feedback, and iteration."]],
  "math-probability": ["Math gives models a language for structure, geometry, and uncertainty.", ["Vectors and matrices represent and transform information.", "Distributions describe how likely outcomes are shaped.", "Mean, spread, tails, and sampling connect formulas to decisions."]],
  "machine-learning": ["A model is a learned transformation surrounded by measurement and iteration.", ["Choose an algorithm that matches the data and task.", "Optimization changes parameters to reduce a measurable loss.", "Validation metrics tell you whether the pattern generalizes."]],
  "python-data": ["Data work becomes repeatable when exploration, transformation, and communication fit together.", ["Python libraries provide a shared vocabulary for data work.", "EDA makes quality, shape, and relationships visible.", "A good workflow leaves behind understandable, reproducible decisions."]],
  "data-systems": ["Reliable insight depends on the systems that store, move, and query data.", ["Schemas and SQL make information discoverable.", "Pipelines move data between sources, warehouses, and consumers.", "Analytics stacks balance freshness, cost, quality, and trust."]],
  "deep-learning": ["Different neural architectures make different kinds of structure easy to learn.", ["Feed-forward networks map inputs; convolution captures local patterns.", "Recurrent and attention-based models represent sequences.", "Backpropagation and representation learning connect architecture to training."]],
  "llm-generative-ai": ["Generative systems turn representations into new text, images, code, and decisions.", ["Tokenization turns language into a sequence of vectors.", "Transformer blocks mix context with attention and feed-forward layers.", "Applications add models, libraries, evaluation, and a useful task boundary."]],
  "rag-agents": ["Retrieval answers with knowledge; agents add planning, tools, and action.", ["RAG follows retrieve → augment → generate.", "Agentic systems can plan, observe, call tools, and revise.", "Use the simplest loop that solves the task reliably."]],
  "computer-vision": ["Vision systems turn pixels into features, objects, scenes, and actions.", ["Representations make visual structure computable.", "Tasks range from classification to detection and segmentation.", "Data quality and evaluation shape what a model can see."]],
  mlops: ["A model is only useful when it can be shipped, observed, and improved.", ["Package models with the data and assumptions they need.", "Monitor quality, drift, latency, and cost after release.", "Feedback from production becomes the next training decision."]],
  "learning-paths": ["A map is useful when it helps you choose the next concrete step.", ["Build fundamentals before adding framework complexity.", "Pair concepts with small, testable projects.", "Revisit the map as your questions become more specific."]]
};

const grid = document.querySelector("#card-grid");
const dialog = document.querySelector("#detail-dialog");
let topics = [];

const renderCards = () => {
  grid.innerHTML = topics.map((topic, index) => `<article class="topic-card" tabindex="0" data-topic="${topic.id}" data-category="${topic.category}" aria-label="Open ${topic.title} explainer">
    <div class="topic-art ${visualById[topic.id][0]}">${visualById[topic.id][1]}</div>
    <div class="topic-info"><span class="topic-number">${String(index + 1).padStart(2, "0")} / ${topic.category}</span><h3 class="topic-title">${topic.title}</h3><p class="topic-blurb">${topic.blurb}</p><span class="topic-pages">${topic.pages.length} reference pages</span><span class="topic-arrow" aria-hidden="true">↗</span></div>
  </article>`).join("");
};

const openTopic = (id) => {
  const topic = topics.find(item => item.id === id);
  if (!topic) return;
  const [summary, points] = summaries[topic.id];
  document.querySelector("#dialog-category").textContent = `${topic.category} · ${topic.pages.length} pages`;
  document.querySelector("#dialog-title").textContent = topic.title;
  document.querySelector("#dialog-summary").textContent = summary;
  document.querySelector("#dialog-art").className = `dialog-art ${visualById[topic.id][0]}`;
  document.querySelector("#dialog-art").innerHTML = visualById[topic.id][1];
  document.querySelector("#dialog-points").innerHTML = points.map((point, i) => `<div class="key-point"><b>0${i + 1}</b><span>${point}</span></div>`).join("");
  document.querySelector("#dialog-pdf").href = assetUrl(topic.pdf);
  document.querySelector("#dialog-pages").innerHTML = topic.pages.map((page, i) => `<figure><img src="${assetUrl(page.image)}" alt="${page.title} reference sheet" loading="${i ? "lazy" : "eager"}"><figcaption>${String(i + 1).padStart(2, "0")} · ${page.title}</figcaption></figure>`).join("");
  dialog.showModal();
};

const setFilters = () => {
  const counts = topics.reduce((result, topic) => {
    result[topic.category] = (result[topic.category] || 0) + 1;
    return result;
  }, {});
  const filters = document.querySelector("#filters");
  filters.innerHTML = `<button class="filter active" type="button" data-filter="all">All topics <span>${topics.length}</span></button>${Object.entries(counts).map(([category, count]) => `<button class="filter" type="button" data-filter="${category}">${category} <span>${count}</span></button>`).join("")}`;
  filters.querySelectorAll(".filter").forEach(button => button.addEventListener("click", () => {
    filters.querySelectorAll(".filter").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    document.querySelectorAll(".topic-card").forEach(card => { card.dataset.hidden = button.dataset.filter !== "all" && card.dataset.category !== button.dataset.filter; });
  }));
};

fetch(assetUrl("catalog.json"))
  .then(response => response.json())
  .then(catalog => {
    topics = catalog;
    renderCards();
    setFilters();
  });

grid.addEventListener("click", event => { const card = event.target.closest(".topic-card"); if (card) openTopic(card.dataset.topic); });
grid.addEventListener("keydown", event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); openTopic(event.target.dataset.topic); } });
document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });
document.querySelectorAll("[data-scroll]").forEach(button => button.addEventListener("click", () => document.querySelector(button.dataset.scroll).scrollIntoView()));
