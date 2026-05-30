const choices = {
  gender: [["female", "Female"], ["male", "Male"], ["other", "Other"]],
  state: [["telangana", "Telangana"], ["andhra_pradesh", "Andhra Pradesh"], ["karnataka", "Karnataka"], ["maharashtra", "Maharashtra"], ["tamil_nadu", "Tamil Nadu"], ["delhi", "Delhi"], ["uttar_pradesh", "Uttar Pradesh"], ["west_bengal", "West Bengal"]],
  category: [["", "Any category"], ["general", "General"], ["obc", "OBC"], ["sc", "SC"], ["st", "ST"], ["ews", "EWS"], ["minority", "Minority"]],
  education: [["", "Any level"], ["class_9_10", "Class 9-10"], ["class_11_12", "Class 11-12"], ["diploma", "Diploma"], ["undergraduate", "Undergraduate"], ["postgraduate", "Postgraduate"], ["phd", "PhD"]],
  stream: [["general", "General"], ["technical", "Technical / Professional"], ["engineering", "Engineering"], ["medical", "Medical"], ["vocational", "Vocational"], ["research", "Research"]],
  residence: [["day_scholar", "Day Scholar"], ["hosteller", "Hosteller"]]
};

const schemes = [
  {
    name: "Post Matric Scholarship for SC Students",
    provider: "Ministry of Social Justice and Empowerment",
    scope: "central",
    description: "Financial assistance for Scheduled Caste students studying after Class 10.",
    benefit: "Maintenance allowance, fees, and academic support.",
    states: [],
    categories: ["sc"],
    education: ["class_11_12", "diploma", "undergraduate", "postgraduate", "phd"],
    streams: [],
    maxIncome: 250000,
    minMarks: 50,
    casteCertificate: true,
    incomeCertificate: true,
    bank: true,
    url: "https://scholarships.gov.in/"
  },
  {
    name: "AICTE Pragati Scholarship for Girl Students",
    provider: "AICTE",
    scope: "central",
    description: "Scholarship for girl students admitted to technical diploma or degree courses.",
    benefit: "Tuition fee and incidental allowance support.",
    states: [],
    categories: [],
    education: ["diploma", "undergraduate"],
    streams: ["technical", "engineering"],
    gender: ["female"],
    maxIncome: 800000,
    minMarks: 50,
    incomeCertificate: true,
    bank: true,
    url: "https://www.aicte-india.org/"
  },
  {
    name: "AICTE Saksham Scholarship",
    provider: "AICTE",
    scope: "central",
    description: "Scholarship for specially-abled students in AICTE-approved technical courses.",
    benefit: "Tuition fee and incidental allowance support.",
    states: [],
    categories: [],
    education: ["diploma", "undergraduate"],
    streams: ["technical", "engineering"],
    maxIncome: 800000,
    minMarks: 50,
    disability: true,
    disabilityCertificate: true,
    incomeCertificate: true,
    bank: true,
    url: "https://www.aicte-india.org/"
  },
  {
    name: "Telangana Post Matric Scholarship",
    provider: "Government of Telangana",
    scope: "state",
    description: "Fee reimbursement and scholarship support for eligible Telangana students.",
    benefit: "Tuition fee reimbursement and maintenance support.",
    states: ["telangana"],
    categories: ["sc", "st", "obc", "ews", "minority"],
    education: ["class_11_12", "diploma", "undergraduate", "postgraduate"],
    streams: [],
    maxIncome: 200000,
    minMarks: 50,
    maxAge: 34,
    casteCertificate: true,
    incomeCertificate: true,
    bank: true,
    url: "https://telanganaepass.cgg.gov.in/"
  },
  {
    name: "National Means-cum-Merit Scholarship",
    provider: "Department of School Education and Literacy",
    scope: "central",
    description: "Scholarship for meritorious school students from economically weaker sections.",
    benefit: "Annual scholarship support as notified by the government.",
    states: [],
    categories: [],
    education: ["class_9_10", "class_11_12"],
    streams: [],
    maxIncome: 350000,
    minMarks: 55,
    incomeCertificate: true,
    bank: true,
    url: "https://scholarships.gov.in/"
  },
  {
    name: "Central Sector Scholarship for College Students",
    provider: "Department of Higher Education",
    scope: "central",
    description: "Merit-cum-means scholarship based on Class 12 performance.",
    benefit: "Annual financial support for undergraduate and postgraduate study.",
    states: [],
    categories: [],
    education: ["undergraduate", "postgraduate"],
    streams: [],
    maxIncome: 450000,
    minMarks: 80,
    incomeCertificate: true,
    bank: true,
    url: "https://scholarships.gov.in/"
  }
];

const demoProfile = {
  fullName: "Demo Student",
  dob: "2005-06-15",
  gender: "female",
  state: "telangana",
  category: "sc",
  income: 180000,
  education: "undergraduate",
  stream: "engineering",
  marks: 82,
  residence: "day_scholar",
  bank: true,
  aadhaarBank: true,
  incomeCertificate: true,
  casteCertificate: true,
  disability: false,
  disabilityCertificate: false,
  bpl: true,
  previousPassed: true
};

const labels = Object.fromEntries(Object.values(choices).flat().filter(([value]) => value).map(([value, label]) => [value, label]));

function fillSelect(name, values, includeBlank = false) {
  document.querySelectorAll(`select[name="${name}"]`).forEach((select) => {
    select.innerHTML = values
      .filter(([value]) => includeBlank || value)
      .map(([value, label]) => `<option value="${value}">${label}</option>`)
      .join("");
  });
}

function ageFromDob(dob) {
  const birth = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const beforeBirthday = today.getMonth() < birth.getMonth() || (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate());
  return beforeBirthday ? age - 1 : age;
}

function profileFromForm() {
  const form = document.querySelector("#profileForm");
  const data = Object.fromEntries(new FormData(form).entries());
  ["bank", "aadhaarBank", "incomeCertificate", "casteCertificate", "disability", "disabilityCertificate", "bpl", "previousPassed"].forEach((key) => {
    data[key] = form.elements[key].checked;
  });
  data.income = Number(data.income || 0);
  data.marks = Number(data.marks || 0);
  data.age = ageFromDob(data.dob);
  return data;
}

function setProfile(profile) {
  const form = document.querySelector("#profileForm");
  Object.entries(profile).forEach(([key, value]) => {
    const field = form.elements[key];
    if (!field) return;
    if (field.type === "checkbox") field.checked = Boolean(value);
    else field.value = value;
  });
}

function listCheck(value, allowed, label, matched, missing) {
  if (!allowed || allowed.length === 0 || allowed.includes(value)) matched.push(label);
  else missing.push(label);
}

function boolCheck(required, value, label, matched, missing) {
  if (!required || value) matched.push(label);
  else missing.push(label);
}

function evaluate(profile, scheme) {
  const matched = [];
  const missing = [];
  listCheck(profile.state, scheme.states, "Domicile/state requirement", matched, missing);
  listCheck(profile.category, scheme.categories, "Category requirement", matched, missing);
  listCheck(profile.education, scheme.education, "Education level requirement", matched, missing);
  listCheck(profile.stream, scheme.streams, "Course stream requirement", matched, missing);
  listCheck(profile.gender, scheme.gender || [], "Gender requirement", matched, missing);
  if (!scheme.maxIncome || profile.income <= scheme.maxIncome) matched.push("Family income limit");
  else missing.push("Family income limit");
  if (!scheme.minMarks || profile.marks >= scheme.minMarks) matched.push("Minimum marks requirement");
  else missing.push("Minimum marks requirement");
  if (!scheme.maxAge || profile.age <= scheme.maxAge) matched.push("Age requirement");
  else missing.push("Age requirement");
  boolCheck(scheme.bank, profile.bank, "Bank account requirement", matched, missing);
  boolCheck(scheme.incomeCertificate, profile.incomeCertificate, "Income certificate requirement", matched, missing);
  boolCheck(scheme.casteCertificate, profile.casteCertificate, "Caste/category certificate requirement", matched, missing);
  boolCheck(scheme.disability, profile.disability, "Disability condition", matched, missing);
  boolCheck(scheme.disabilityCertificate, profile.disabilityCertificate, "Disability certificate requirement", matched, missing);
  const score = Math.round((matched.length / (matched.length + missing.length)) * 100);
  return { scheme, matched, missing, score, status: missing.length === 0 ? "Eligible" : score >= 75 ? "Almost eligible" : "Not eligible" };
}

function schemeCard(scheme) {
  return `<article class="scheme-card">
    <div class="card-head">
      <div>
        <p class="tag">${scheme.scope === "central" ? "Central Government" : "State Government"}</p>
        <h3>${scheme.name}</h3>
        <p class="muted">${scheme.provider}</p>
      </div>
    </div>
    <p>${scheme.description}</p>
    <p><strong>Benefit:</strong> ${scheme.benefit}</p>
    <a href="${scheme.url}" target="_blank" rel="noreferrer">Official portal</a>
  </article>`;
}

function resultCard(result) {
  const stateClass = result.status === "Eligible" ? "eligible" : result.status === "Almost eligible" ? "almost" : "not";
  return `<article class="scheme-card ${stateClass}">
    <div class="card-head">
      <div>
        <p class="tag">${result.scheme.scope === "central" ? "Central Government" : "State Government"}</p>
        <h3>${result.scheme.name}</h3>
        <p class="muted">${result.scheme.provider}</p>
      </div>
      <div class="score">${result.score}%</div>
    </div>
    <p><strong>${result.scheme.benefit}</strong></p>
    <p class="status ${stateClass}">${result.status}</p>
    <div class="criteria">
      <div><h3>Matched</h3><ul>${result.matched.map((item) => `<li>${item}</li>`).join("")}</ul></div>
      <div><h3>Missing</h3><ul>${(result.missing.length ? result.missing : ["No missing requirement"]).map((item) => `<li>${item}</li>`).join("")}</ul></div>
    </div>
    <a class="button secondary no-print" href="${result.scheme.url}" target="_blank" rel="noreferrer">Apply / verify officially</a>
  </article>`;
}

function renderSchemes(items = schemes) {
  document.querySelector("#schemeList").innerHTML = items.map(schemeCard).join("") || "<p>No schemes found.</p>";
}

function renderResults(profile) {
  const results = schemes.map((scheme) => evaluate(profile, scheme)).sort((a, b) => b.score - a.score);
  document.querySelector("#reportSummary").innerHTML = `
    <div><strong>${profile.fullName}</strong><span>Student</span></div>
    <div><strong>${labels[profile.category]}</strong><span>Category</span></div>
    <div><strong>${profile.marks}%</strong><span>Marks</span></div>
    <div><strong>${profile.age}</strong><span>Age</span></div>`;
  document.querySelector("#resultsList").innerHTML = results.map(resultCard).join("");
}

function init() {
  fillSelect("gender", choices.gender);
  fillSelect("state", choices.state);
  fillSelect("category", choices.category, true);
  fillSelect("education", choices.education, true);
  fillSelect("stream", choices.stream);
  fillSelect("residence", choices.residence);
  document.querySelector("#schemeCount").textContent = schemes.length;
  document.querySelector("#centralCount").textContent = schemes.filter((item) => item.scope === "central").length;
  document.querySelector("#stateCount").textContent = schemes.filter((item) => item.scope === "state").length;
  renderSchemes();
  const saved = localStorage.getItem("schemesetu-profile");
  setProfile(saved ? JSON.parse(saved) : demoProfile);
  renderResults(profileFromForm());
}

document.querySelector("#loadDemo").addEventListener("click", () => {
  setProfile(demoProfile);
  renderResults(profileFromForm());
});

document.querySelector("#profileForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const profile = profileFromForm();
  localStorage.setItem("schemesetu-profile", JSON.stringify(profile));
  renderResults(profile);
  location.hash = "report";
});

document.querySelector("#schemeFilters").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget).entries());
  const filtered = schemes.filter((scheme) => {
    const qMatch = !data.q || `${scheme.name} ${scheme.provider} ${scheme.description}`.toLowerCase().includes(data.q.toLowerCase());
    const scopeMatch = !data.scope || scheme.scope === data.scope;
    const categoryMatch = !data.category || scheme.categories.length === 0 || scheme.categories.includes(data.category);
    const educationMatch = !data.education || scheme.education.length === 0 || scheme.education.includes(data.education);
    return qMatch && scopeMatch && categoryMatch && educationMatch;
  });
  renderSchemes(filtered);
});

document.querySelector("#resetFilters").addEventListener("click", () => {
  document.querySelector("#schemeFilters").reset();
  renderSchemes();
});

document.querySelector("#printReport").addEventListener("click", () => window.print());

init();
