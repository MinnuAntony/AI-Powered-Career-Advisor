import React, { useState } from "react";

const QUIZ_DOMAINS = {
  Analytical: [
    "I enjoy solving puzzles and logical problems.",
    "I like working with numbers and patterns.",
    "I enjoy analyzing data to make decisions."
  ],
  Creative: [
    "I enjoy drawing, designing, or writing creatively.",
    "I like thinking of unique solutions to problems.",
    "I enjoy brainstorming and imagining new ideas."
  ],
  Leadership: [
    "I enjoy leading group activities or projects.",
    "I like making decisions for a team.",
    "I motivate and guide others effectively."
  ],
  Communication: [
    "I enjoy explaining ideas clearly to others.",
    "I like writing or presenting my thoughts.",
    "I can persuade or influence others easily."
  ]
};

export default function AssessmentForm({ onSubmit }) {
  const [answers, setAnswers] = useState(
    Object.fromEntries(
      Object.keys(QUIZ_DOMAINS).map((d) => [d, Array(QUIZ_DOMAINS[d].length).fill(0)])
    )
  );

  const handleChange = (domain, idx, value) => {
    const newDomainAnswers = [...answers[domain]];
    newDomainAnswers[idx] = Number(value);
    setAnswers({ ...answers, [domain]: newDomainAnswers });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // const assessment = { answers };  

    // Step 1: calculate scores
    const traits = {};
    for (const [domain, scores] of Object.entries(answers)) {
      traits[domain] = scores.reduce((a, b) => a + b, 0);
    }

    // Step 2: sort traits to find top two
    const sorted = Object.entries(traits).sort((a, b) => b[1] - a[1]);
    const primary_trait = sorted[0][0];
    const secondary_trait = sorted[1] ? sorted[1][0] : null;

    // Step 3: build payload
    const assessment = {
      personality_traits: traits,
      primary_trait,
      secondary_trait,
      suggested_careers: [] // optional, backend can fill
    };

    onSubmit(assessment);
  };

  return (
    <form className="space-y-6 p-6 bg-white shadow-md rounded-lg" onSubmit={handleSubmit}>
      <h2 className="text-2xl font-bold text-gray-800">Assessment Quiz</h2>
      {Object.entries(QUIZ_DOMAINS).map(([domain, questions]) => (
        <div key={domain} className="space-y-2">
          <h3 className="font-semibold">{domain}</h3>
          {questions.map((q, idx) => (
            <div key={idx} className="mb-3">
              <label className="block text-sm text-gray-700">{q}</label>
              <input
                type="number"
                min={0}
                max={2}
                value={answers[domain][idx]}
                onChange={(e) => handleChange(domain, idx, e.target.value)}
                className="border p-2 rounded w-full"
              />
            </div>
          ))}
        </div>
      ))}
      <button className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700">
        Submit Assessment
      </button>
    </form>
  );
}

