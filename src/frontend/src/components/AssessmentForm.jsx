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
      Object.keys(QUIZ_DOMAINS).map((d) => [
        d,
        Array(QUIZ_DOMAINS[d].length).fill(0)
      ])
    )
  );
  const [loading, setLoading] = useState(false);

  const handleChange = (domain, idx, value) => {
    const newDomainAnswers = [...answers[domain]];
    newDomainAnswers[idx] = Number(value);
    setAnswers({ ...answers, [domain]: newDomainAnswers });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Step 1: calculate scores
    const traits = {};
    for (const [domain, scores] of Object.entries(answers)) {
      traits[domain] = scores.reduce((a, b) => a + b, 0);
    }

    // Step 2: sort traits
    const sorted = Object.entries(traits).sort((a, b) => b[1] - a[1]);
    const primary_trait = sorted[0][0];
    const secondary_trait = sorted[1] ? sorted[1][0] : null;

    // Step 3: build payload
    const assessment = {
      personality_traits: traits,
      primary_trait,
      secondary_trait,
      suggested_careers: []
    };

    try {
      await onSubmit(assessment); // wait for backend response
    } finally {
      setLoading(false); // stop loading whether success or error
    }
  };

  return (
    <form
      className="space-y-6 p-6 bg-white shadow-md rounded-lg"
      onSubmit={handleSubmit}
    >
      <h2 className="text-2xl font-bold text-gray-800">Assessment Quiz </h2>
      {/* Rules Section */}
      <div className="bg-gray-100 p-4 rounded-md text-sm text-gray-700">
        <p className="font-semibold mb-2">How to answer:</p>
        <ul className="list-disc list-inside space-y-1">
          <li><strong>0</strong> → Never / Not true for me</li>
          <li><strong>1</strong> → Sometimes / Somewhat true</li>
          <li><strong>2</strong> → Often / True for me</li>
        </ul>
      </div>
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
      <button
        type="submit"
        disabled={loading}
        className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Assessment"}
      </button>

      {loading && (
        <p className="text-gray-600 mt-2">Please wait, generating recommendations...</p>
      )}
    </form>
  );
}


